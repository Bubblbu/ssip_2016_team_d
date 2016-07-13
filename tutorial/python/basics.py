# -*- coding: utf-8 -*-
"""	basics.py

Basic functions in scikit-image
"""

from skimage.io import imread
from skimage.color import convert_colorspace, rgb2gray
from helpers import show_image, save_image

# Load image
lena = imread("../lena.jpg")

# Draw and display an image
plt.imshow(lena)
plt.show()

# Matrix indices are [rows, columns]
# Extract the rows 100 to 200 & all columns
sub_lena = lena[100:200 , 0:-1]
show_image(sub_lena)

# Accessing color channels: third index -> [rows, cols, channel]
red_lena = lena[:,:,0]
show_image(red_lena, cmap="gray")

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