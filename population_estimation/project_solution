%% preprocessing steps
% images
im1 = imread('images/ref_camp.jpg');

%work with the first one
imgray = rgb2gray(im1);
% histogram : you can see that the most frequent values are completely out
% of the range of houses
% imhist(imgray);
imthresh1 = imgray > 180;

imblurred = imgaussfilt(imgray, 5);
houseness = imgray-imblurred;
% imhist(houseness);
% the darkest regions don't matter
imthresh2 = houseness > 10;
% use the combination of the two thresholds
imresthresh = imthresh1 & imthresh2;
%open the image to remove small artifacts
se = strel('rectangle', [4,4]);
imresult = imopen(imresthresh, se);
% figure, imshow(imgray);
% figure,imshow(imresult);

%% labeling and counting data

obj_tents = bwlabel(imresult);
numobj = numel(unique(obj_tents));

s = regionprops(imresult);
%put the areas into an array
for i=1:numel(s)
    results(i) = s(i).Area;
end

% find the objects that belong to the "typical house" size
indices = find(results>150);
% total number of pixels where people are living
total_living_pixel = sum(results(indices));

ppl_per_household = 6; % UNICEF estimate

avg_pixel_per_household = mean(results(indices));
ppl_in_image = total_living_pixel * ppl_per_household / avg_pixel_per_household;
final_result = 6*ppl_in_image;

fprintf('Estimated number of people living in the given area: %d\n ----\n Estimated number of people living in the refugee camp: %d\n', ppl_in_image, final_result);
