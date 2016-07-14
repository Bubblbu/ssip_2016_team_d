
% Load Lena
lena = imread('../lena.jpg');

% Save the red channel
red_lena = lena(:,:,1);
lena_1 = red_lena;

% set values < mean intensity to 0
mean_intensity = mean(red_lena(:));
lena_1(red_lena< mean_intensity) = 0;

figure, imshow(lena_1);

% Thresholding with Otsu's method (not implemented in matlab by default)
thresh = otsu(red_lena, 2);
figure, imshow(thresh, []); % second parameter to scale the pixel values