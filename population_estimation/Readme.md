# Population estimation
## Preprocessing
The input image seemed fairly easy to be solved, as the buildings can be separated from the environment based on their intensity values.
Studying the histogram of the grayscale image, we can say that the buildings belong to the brightest part of the picture.
Blurring the image and subtracting it from the original one result in the removing of the clouds and it emphasises the black border, the houses also remain with brighter colour compared to the other parts of the picture. 
![Subtracted image](../houseness.jpg)
Using thresholds on the original picture and the subtracted, finally using a logical AND operation between them, we get an approximation of where the buildings should be. However, there are some artifacts left, so by using morphological opening, we try to solve this issue.
(here an image of the result img)
## Estimating the population
Using given numbers by the UNICEF (average 6 people per household in Somalia) and studying the pixel size of a normal building of the picture, we can estimate the population by using
ppl_in_image = total_living_pixel * ppl_per_household / avg_pixel_per_household;

## Refugee camp Ifo 2 Dabaaab
