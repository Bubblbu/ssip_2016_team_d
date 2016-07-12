from skimage.io import imread
from skimage.morphology import disk
from skimage.filters.rank import mean
from skimage.color import rgb2gray

import matplotlib.pyplot as plt
import numpy as np

from scipy import fftpack

# Function for displaying an image
def show_image(img, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.colorbar()
	plt.show()

def save_image(img, filename, colormap = None):
	plt.imshow(img, cmap=colormap)
	plt.savefig(filename)

lena = imread("lena.jpg")
lena_glass = imread("lena_glass.jpg")

# Point operators - subtraction
glass = lena - lena_glass
# show_image(glass)

# Local operators - mean filter
mean_lena = mean(rgb2gray(lena), disk(5))
# show_image(mean_lena, colormap="gray")

# Global operator
F1 = fftpack.fft2(rgb2gray(lena))
 
# Now shift the quadrants around so that low spatial frequencies are in
# the center of the 2D fourier transformed image.
F2 = fftpack.fftshift( F1 )

# Calculate a 2D power spectrum
psd2D = np.abs(F2)
 
# Now plot up both
plt.imshow( np.log10( rgb2gray(lena) ), cmap="gray")
plt.figure()
plt.imshow( np.log10( psd2D ), cmap="gray")


size = F2.shape[0]
middle = size/2
offset = 150

# psd2D[middle-offset:middle+offset,middle-offset:middle+offset] = 1
# F2[middle-offset:middle+offset,middle-offset:middle+offset] = 0

F2[0:offset,:] = 0
F2[size-offset:size,:] = 0
F2[:,0:offset] = 0
F2[:,size-offset:size] = 0

psd2D[0:offset,:] = 1
psd2D[size-offset:size,:] = 1
psd2D[:,0:offset] = 1
psd2D[:,size-offset:size] = 1

plt.figure()
plt.imshow( np.log10( psd2D ), cmap="gray")

temp = fftpack.ifftshift(F2)
back = fftpack.ifft2(temp)

plt.figure()
plt.imshow( np.abs(back), cmap="gray")
plt.show()