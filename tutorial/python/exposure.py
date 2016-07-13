# -*- coding: utf-8 -*-
""" exposure.py

Basic functions in scikit-image and matplotlib
"""

from skimage.io import imread
from skimage import exposure
import numpy as np
import matplotlib.pyplot as plt

from helpers import show_image, save_image

# Load Lena
lena = imread("../lena.jpg")

# Red channel
red_lena = lena[:,:,0]

# Plot histogram and choose 
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(13.5,6))
ax0.hist(red_lena.ravel(), bins=100)
ax1.imshow(red_lena, cmap="gray", clim=(60.0, 240.0))
plt.show()

# Automatic exposure equalization
equal_lena = exposure.equalize_hist(red_lena, nbins=256)
show_image(equal_lena, colormap="gray")
