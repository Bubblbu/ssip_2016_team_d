# -*- coding: utf-8 -*-
""" filters.py

Basic functions in scikit-image and matplotlib
"""

from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage import filters

import numpy as np

from helpers import show_image, save_image

# Load Lena
lena = imread("../lena.jpg")

# Save the red channel
red_lena = lena[:,:,0]
lena_1 = np.copy(red_lena)

# set values < mean intensity to 0
mean_intensity = np.mean(red_lena)
lena_1[red_lena<mean_intensity] = 250

show_image(lena_1, colormap="gray")

# Thresholding with Otsu's method
thresh = threshold_otsu(red_lena)
lena_2 = red_lena > thresh

show_image(lena_2, colormap="gray")