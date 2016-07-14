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
from skimage.morphology import disk, diamond, square
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.filters.rank import bottomhat, median, mean
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage.transform import resize

from scipy.cluster.vq import kmeans,vq
from sklearn.ensemble import RandomForestClassifier

from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

from preprocessing import Preprocessor

def show_image(img, cmap=None):
	plt.figure()
	plt.imshow(img, cmap=cmap)
	plt.show(block=False)

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

def plot_comparison(original, filtered, filter_name):

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True, sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.set_title('original')
    ax1.axis('off')
    ax1.set_adjustable('box-forced')
    ax2.imshow(filtered, cmap=plt.cm.gray)
    ax2.set_title(filter_name)
    ax2.axis('off')
    ax2.set_adjustable('box-forced')

if __name__ == "__main__":
	# Settings
	box_size = 80
	scale_factor = 0.8
	mask_scale = 0.2
	plot = False

	box_size *= scale_factor
	
	# Load Preprocessor
	print("Preprocessing")
	p = Preprocessor("../images/slum_image.jpg")
	p.scale_image(scale_factor)
	p.exposure_equalization(method="equal")
	p.convert_color("RGB","HSV")
	p.save_current_as("structure")

	p.reset()
	p.scale_image(mask_scale)
	p.exposure_equalization(method="equal")
	p.convert_color("RGB","HSV")
	p.save_current_as("mask")

	# Load images for mask and structure information
	img2 = p.get_version("mask")[:,:,0]
	img = p.get_version("structure")[:,:,2]

	print("Masking")
	med_img = median(img2, disk(50*mask_scale))
	mask = np.zeros(img2.shape)

	mask[med_img>np.mean(med_img)] = 1
	mask_c = closing(mask, disk(100*mask_scale))
	# plot_comparison(mask, mask_c, 'closing')
	# plot_comparison(mask_c, mean(mask_c, disk(20)), 'mean')
	
	masked = np.copy(img)
	# masked = img * resize(mask_c, img.shape)

	# plot_comparison(img, masked, "masked")

	print("bottomhatting")
	streets_2 = bottomhat(masked, disk(20*scale_factor))
	# streets_3 = bottomhat(masked, disk(6))

	# plot_comparison(streets_2, streets_3, "bottomhat")
	global_thresh = threshold_otsu(streets_2)
	binary_global = streets_2 > global_thresh

	block_size = 71
	binary_adaptive = threshold_adaptive(streets_2, block_size)

	plot_comparison(binary_global, binary_adaptive, "bi")

	combined= binary_global*binary_adaptive

	closed = closing(opening(combined, square(2*scale_factor)), square(2*scale_factor))
	plot_comparison(combined,  closed, "opening")

	show_image(closed, cmap="gray")

	plt.show()
