from skimage.io import imread
from skimage import exposure

import matplotlib.pyplot as plt
import numpy as np

# Function for displaying an image
def show_image(img, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.colorbar()
	plt.show()

def save_image(img, filename, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.savefig(filename)

lena = imread("lena.jpg")
red_lena = lena[:,:,0]

# calculate histogram
exposure.histogram(red_lena, nbins=10)

# plot histogram
plt.hist(red_lena.ravel(), bins=100)

# Manually "equalize" exposure
plt.figure()
plt.imshow(red_lena, clim=(150.0, 250.0), cmap="gray")

plt.figure()
plt.imshow(red_lena, cmap="gray")
plt.show()

# Automatic exposure equalization
equal_lena = exposure.equalize_hist(lena, nbins=256)
show_image(lena, colormap="gray")
show_image(equal_lena, colormap="gray")

