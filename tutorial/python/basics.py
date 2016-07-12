# -*- coding: utf-8 -*-
"""Basic functions in scikit-image and matplotlib


"""

from skimage.io import imread
from skimage.color import convert_colorspace, rgb2gray
import matplotlib.pyplot as plt

# Function for displaying an image
def show_image(img, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.show()

# Function to save an image
def save_image(img, filename, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.savefig(filename)

# This part of the code is run, if this file is run by its own "python basics.py"
if __name__ == "__main__":
	# Load image
	lena = imread("lena.jpg")

	# Draw and display an image
	plt.imshow(lena)
	plt.show()

	# Matrix indices are [rows, columns]
	# Extract the rows 100 to 200 & all columns
	sub_lena = lena[100:200 , 0:-1]
	show_image(sub_lena)

	# Accessing color channels: third index -> [rows, cols, channel]
	red_lena = lena[:,:,0]
	plt.imshow(red_lena, cmap="gray")

	# Convert to grayscale and use different colormap
	gray_lena = rgb2gray(lena)
	show_image(gray_lena, colormap="inferno")

	# Convert to other colorspace
	hsv_lena = convert_colorspace(lena, "RGB", "HSV")

	# Only show saturation
	sat_lena = hsv_lena[:,:,1]
	show_image(sat_lena, "gray")

	# Save image
	save_image(sat_lena, "sat_lena.jpg", "gray")