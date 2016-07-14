# -*- coding: utf-8 -*-
"""Preprocessing module.

Use the class Preprocessor to load an image and apply different preprocessing steps.
Relies on scikit-image.

Implemented:
	* Color space convertion (RGB, HSV, RGB CIE, XYZ)
	* Histogram Equalization (Adaptive, Non-adaptive, Contrast stretching)
"""

import numpy as np
import matplotlib.pyplot as plt
from math import pi
import random

from skimage.feature import greycomatrix, greycoprops, canny, structure_tensor, structure_tensor_eigvals, hessian_matrix
from skimage.feature import ORB
from scipy.cluster.vq import kmeans,vq
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from preprocessing import Preprocessor

def plot_bounding_box(ax, x, y, r, c):
	box = np.array([[x-r,y-r],
		[x-r,y+r],
		[x+r,y+r],
		[x+r,y-r],
		[x-r,y-r]])

	ax.plot(box.T[0], box.T[1], c=c)


def quantize_colors(patch):
	pixel = np.reshape(patch, (patch.shape[0]*patch.shape[1], 1))
	# performing the clustering
	centroids,_ = kmeans(pixel,6) # six colors will be found
	# quantization
	qnt,_ = vq(pixel,centroids)

	# reshaping the result of the quantization
	centers_idx = np.reshape(qnt,(patch.shape[0],patch.shape[1]))
	clustered = centroids[centers_idx]
	return np.flipud(clustered)[:,:,0]


def create_features(p, x, y, r):
	"""Create feature for patch

	Tested features:

	+ Mean intensity of RGB CIE[:,:,0]
	+ Mean intensity of RGB CIE[:,:,1]
	+ Mean intensity of RGB CIE[:,:,2]
	+ Mean intensity of HSV[:,:,0]
	+ Canny edge image
	+ Eigenvalues from structure tensor
	"""

	features = []

	# Get patch/patches
	structure_img = p.get_version("structure")[:,:,2]
	structure_patch = structure_img[int(y-r):int(y+r), int(x-r):int(x+r)]

	rgb_img = p.get_version("contrast_rgb_cie")
	rgb_patch = rgb_img[int(y-r):int(y+r), int(x-r):int(x+r)]

	# Color quantization with k_means
	# patch = quantize_colors(patch)

	# ==== FEATURES =======

	# Median values of the individual color channels
	features.append(np.median(rgb_patch[:,:,0]))
	features.append(np.median(rgb_patch[:,:,1]))
	features.append(np.median(rgb_patch[:,:,2]))

	# Edges
	edges = canny(structure_patch)
	features += edges.astype(float).ravel().tolist()

	# Structure Tensor
	Axx, Axy, Ayy = structure_tensor(structure_patch)
	l1, l2 = structure_tensor_eigvals(Axx, Axy, Ayy)

	features += l1.ravel().tolist()
	features += l2.ravel().tolist()

	return features


if __name__ == "__main__":
	# Settings
	box_size = 80
	scale_factor = 0.4
	plot = False

	# Init variables
	print("Init all variables")
	coords = np.loadtxt("patch_coordinates.txt", delimiter="\t", skiprows=1)
	coords = np.multiply(coords, scale_factor)
	patches = {'white':coords[:,0:2],
		   	   'brown':coords[:,2:4],
		   	   'gray':coords[:,4:6],
		       'green':coords[:,6:8]}

	box_size *= scale_factor
	
	# Load Preprocessor
	print("Preprocessing")
	p = Preprocessor("../images/original/slum_image.png")
	p.scale_image(scale_factor)
	p.save_current_as("normal")

	p.exposure_equalization(method="contrast")
	p.convert_color("RGB","RGB CIE")
	p.save_current_as("contrast_rgb_cie")

	p.reset()
	p.scale_image(scale_factor)
	p.exposure_equalization(method="equal")
	p.convert_color("RGB","HSV")
	p.save_current_as("structure")

	# ========== Plot img & patches =========
	if plot:
		plt.figure()
		ax = plt.gca()
		img = p.get_version('structure')[:,:,1]
		plt.imshow(img)

		# Plot patch centers
		for name, coords in patches.items():
			plt.scatter(coords.T[0], coords.T[1], c=name, s=100*scale_factor)

		# Plot patch bounding boxes
		for name, coords in patches.items():
			for row in coords:
				plot_bounding_box(ax, row[0], row[1], box_size, name)

		plt.xlim((0,img.shape[1]))
		plt.ylim((img.shape[0],0))
		plt.show(block=False)

	# ========== Create features =========
	print("Creating features")
	Y = []
	X = []
	for name, coords in patches.items():
		# Prepare labels
		if name == "white":
			Y += [0]*20
		elif name == "brown":
			Y += [1]*20
		elif name == "gray":
			Y += [2]*20
		else:
			Y += [3]*20

		# Create training data
		for row in coords:
			X.append(create_features(p, row[0], row[1], box_size))

	# ========== Train model =========
	print("Training Random Forest")
	clf = RandomForestClassifier(n_estimators=500)
	# clf = SVC()
	clf = clf.fit(X, Y)

	# ========== Test model =========
	print("Predicting")

	# Initilize dict for prediction results
	preds = {'white':np.empty((1,2)),
		   	   'brown':np.empty((1,2)),
		       'gray':np.empty((1,2)),
		       'green':np.empty((1,2))}

	probas = []
	features = []
	for y in xrange(200, 2500, 60):
		row = []
		y *= scale_factor
		for x in xrange(200, 4600, 60):
			x *= scale_factor

			pred = clf.predict(create_features(p, x, y, box_size))[0]

			if pred == 0:
				preds['white'] = np.vstack((preds['white'], [x,y]))
			elif pred == 1:
				preds['brown'] = np.vstack((preds['brown'], [x,y]))
			elif pred == 2:
				preds['gray'] = np.vstack((preds['brown'], [x,y]))
			elif pred == 3:
				preds['green'] = np.vstack((preds['green'], [x,y]))

		# probas.append(row)
		print("Row {} done".format(y))

	plt.figure()
	ax = plt.gca()
	img = p.get_version('normal')
	plt.imshow(img)

	# Plot patch centers
	for name, coords in preds.items():
		plt.scatter(coords.T[0], coords.T[1], c=name, s=100*scale_factor)

	# # Plot patch bounding boxes
	# # for name, coords in preds.items():
	# # 	for row in coords:
	# # 		plot_bounding_box(ax, row[0], row[1], box_size, name)

	plt.xlim((0,img.shape[1]))
	plt.ylim((img.shape[0],0))
	plt.imsave("test.png")
	plt.show()