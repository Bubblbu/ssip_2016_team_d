# -*- coding: utf-8 -*-
"""Preprocessing module.

Use the class Preprocessor to load an image and apply different preprocessing steps.
Relies on scikit-image.

Implemented:
	* Color space convertion (RGB, HSV, RGB CIE, XYZ)
	* Histogram Equalization (Adaptive, Non-adaptive, Contrast stretching)
"""

from skimage.transform import (hough_line, hough_line_peaks,
							   probabilistic_hough_line, resize)
from skimage.feature import canny
from skimage import exposure
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.color import convert_colorspace

import numpy as np
import matplotlib.pyplot as plt
from math import pi

from skimage.morphology import disk, diamond, square
from skimage.filters.rank import bottomhat, median, mean

class Preprocessor(object):
	"""A simple preprocesing class"""
	def __init__(self, image_path):
		self.image_path = image_path
		self.original_image = None
		self.current_image = None

		self.saved_versions = {}

		self.original_w = 0
		self.original_h = 0
		self.w = 0
		self.h = 0

		self.load_image()

	def load_image(self):
		self.original_image = imread(self.image_path)
		self.current_image = self.original_image
		self.h = self.current_image.shape[0]
		self.w = self.current_image.shape[1]
		self.original_h = self.original_image.shape[0]
		self.original_w = self.original_image.shape[1]

	def reset(self):
		self.h = self.original_h
		self.w = self.original_w
		self.current_image = self.original_image

	def save_current_as(self, name):
		self.saved_versions[name] = self.current_image

	def get_version(self, name):
		return self.saved_versions[name]

	def scale_image(self, scale_factor):
		h = int(self.h*scale_factor)
		w = int(self.w*scale_factor)
		self.current_image = resize(self.current_image, (h,w))
		self.h = h
		self.w = w

	def convert_color(self, from_cp, to_cp):
		self.current_image = convert_colorspace(self.current_image, from_cp, to_cp)
		return self.current_image

	def exposure_equalization(self, method, clip_limit=0.03):
		if method == "adapt":
			# Adaptive Histogram Equalization
			for i in range(0,self.current_image.shape[2]):
				self.current_image[:,:,i] = exposure.equalize_adapthist(self.current_image[:,:,i],
																		clip_limit=clip_limit)
		elif method == "equal":
			# Histogram Equalization
			for i in range(0,self.current_image.shape[2]):
				self.current_image[:,:,i] = exposure.equalize_hist(self.current_image[:,:,i])
		elif method == "contrast":
			# Contrast stretching
			for i in range(0,self.current_image.shape[2]):
				p2, p98 = np.percentile(self.current_image[:,:,i], (2, 98))
				self.current_image[:,:,i] = exposure.rescale_intensity(self.current_image[:,:,i], in_range=(p2, p98))
		return self.current_image

	def show_image(self, img=None, title=None):
		plt.figure()
		if img == None:
			plt.imshow(self.current_image[:,:,0], cmap="viridis")
		else:
			plt.imshow(img)
		if title != None:
			plt.title(title)
		plt.show(block=False)

	def show_images(self, image_array, title_array=None):
		if title_array != None:
			for idx, img in enumerate(image_array):
				self.show_image(img, title_array[idx])
		else:
			for idx, img in enumerate(image_array):
				self.show_image(img)
		plt.show()

	def savefig(self, filename, img=None, orig_size=None, cmap=None):
		if orig_size:
			w,h  = orig_size
			fig = plt.figure(figsize=(w/float(1000),h/float(1000)), dpi=100, frameon=False)
			fig.set_dpi(100)
		else:
			fig = plt.figure(frameon=False)

		a = fig.gca()

		if img == None:
			a.imshow(self.current_image, cmap=cmap)
		else:
			a.imshow(img, cmap=cmap)

		a.set_xticks([])
		a.set_yticks([])
		plt.axis('off')
		
		if orig_size:
			fig.savefig(filename, transparent=True, bbox_inches='tight', pad_inches=0, dpi=1000)
		else:
			fig.savefig(filename, transparent=True, bbox_inches='tight', pad_inches=0, dpi=100)


	def create_preprocessed(self, output_path):
		""" This method creates output images of all colorspace,histogram combinations"""
		orig_size = (3500, 2054)

		for hist_meth in ["adapt", "equal", "contrast"][::-1]:
			for col_space in ['HSV', 'RGB CIE', 'XYZ']:
				prep.reset()
				prep.exposure_equalization(hist_meth)
				prep.convert_color("RGB", col_space)

				prep.savefig(output_path + '/{}_{}.png'.format(hist_meth, col_space),
					orig_size=orig_size)

				# Save individual color channels
				for i in range(0, prep.current_image.shape[2]):
					prep.savefig(output_path + '/{}_{}_channel_{}.png'.format(hist_meth, col_space, col_space[i]),
						prep.current_image[:,:,i],
						orig_size=orig_size, cmap="gray")

if __name__ == "__main__":
	# Line finding using the Probabilistic Hough Transform.

	prep = Preprocessor("../images/original/ref_camp.jpg")
	prep.create_preprocessed("../images/preprocessed_ref")