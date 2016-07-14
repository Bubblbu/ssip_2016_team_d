# Slum image from Kibera, Nairobi

## Preprocessing

Extensive work was invested in preprocessing and different combinations of contrast stretching, color space convertions and histogram equalizations.
Certain combinations proved to be fitting for different purposes (e.g. structural information, rough segmentation, emphasize colors).

## Segmentation with Random Forests

Random Forest Classifier for small 160x160 patches. Labels were:

+ White buildings (20 patches)
+ Brown buildings (20 patches)
+ Gray buildiings (20 patches)
+ Vegetation/not building (20 patches)

Extracted features:

+ Mean intensity for color channels
+ Canny edges
+ Eigenvalues of the structure tensor

Results show that a rough segmentation is actually promising considering the limited amount of training data.

![Segmentation](output_images/segmentation.png)

## Streets

Pure image processing approach to emphasize and detect streets in the image.
Result could be combined with the result from the ML segmentation to obtain a possible ensuing point for a counting algorithm.

![Streets](output_images/edge_image.png)

## Outlook

+ Line detection to extract street data
+ Count buildings
