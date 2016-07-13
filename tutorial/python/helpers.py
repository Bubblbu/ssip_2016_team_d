# -*- coding: utf-8 -*-
""" helpers.py
Helper functions
"""

import matplotlib.pyplot as plt

# Function for displaying an image
def show_image(img, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.colorbar()
	plt.show()

# Wrapper for saving images
def save_image(img, filename, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.savefig(filename)