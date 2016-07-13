# -*- coding: utf-8 -*-
"""	operators.py

Point, local and global operators
"""

import matplotlib.pyplot as plt
import numpy as np

from skimage.io import imread
from skimage.morphology import disk
from skimage.filters.rank import mean
from skimage.color import rgb2gray

from scipy import fftpack

from helpers import show_image, save_image

# Load Lena and Lena_with_glasses
lena = imread("../lena.jpg")
lena_glass = imread("../lena_glass.jpg")

# ====== Point operators =======
# ------ Pixelweise subtraction ------
glass = lena - lena_glass
show_image(glass)

# ====== Local operators =======
# ------ Mean filter ------
mean_lena = mean(rgb2gray(lena), disk(5))
show_image(mean_lena, colormap="gray")

# ====== Global operators ======
# ------ Fourier transformation ------
F1 = fftpack.fft2(rgb2gray(lena))
F2 = fftpack.fftshift(F1)
F2_copy = np.copy(F2)

# Calculate a 2D power spectrum
psd2D = np.abs(F2)
 
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(13.5,6), sharey=True)
ax0.imshow( np.log10(rgb2gray(lena)), cmap="gray")
ax1.imshow(np.log10(psd2D), cmap="gray")
plt.show()

size = F2.shape[0]
middle = size/2
offset = 220

# -------- Remove low frequency information
F2[0:offset,:] = 0
F2[size-offset:size,:] = 0
F2[:,0:offset] = 0
F2[:,size-offset:size] = 0

F1_back = fftpack.ifftshift(F2)
Lena_back = fftpack.ifft2(F1_back)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(13.5,6), sharey=True)
ax0.imshow(np.log10(np.abs(F2)), cmap="gray")
ax1.imshow(np.abs(Lena_back), cmap="gray")
plt.show()

# -------- Remove high frequency information
offset = 15
F2 = F2_copy

F2[middle-offset:middle+offset,middle-offset:middle+offset] = 0

F1_back = fftpack.ifftshift(F2)
Lena_back = fftpack.ifft2(F1_back)

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(13.5,6), sharey=True)
ax0.imshow(np.log10(np.abs(F2)), cmap="gray")
ax1.imshow(np.abs(Lena_back), cmap="gray")
plt.show()