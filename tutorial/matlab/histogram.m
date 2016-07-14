
% Load Lena
lena = imread('../lena.jpg');

% Red channel
red_lena = lena(:,:,1);

% Plot histogram and image on the same figure
figure, subplot(1,2,1), imshow(red_lena), subplot(1,2,2), imhist(red_lena);

% Histogram equalization
equal_lena = histeq(red_lena);
figure, subplot(1,2,1), imshow(equal_lena), subplot(1,2,2), imhist(equal_lena);