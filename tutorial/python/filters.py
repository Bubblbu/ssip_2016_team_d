from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage import filters

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

# copy of lena
red_lena = lena[:,:,0]

thresh_lena = np.copy(red_lena)

# set values < mean intensity to 0
mean_intensity = np.mean(red_lena)
thresh_lena[red_lena<mean_intensity] = 250

# show_image(thresh_lena, colormap="gray")



# Otsu's method

thresh = threshold_otsu(red_lena)
binary_lena = red_lena > thresh

# show_image(binary_lena, colormap="gray")