%% Basic functions in matlab

% Read image
lena = imread('../lena.jpg');

% Display an image
figure, title('Lena'), imshow(lena);

% Matrix indices are [rows, columns]
% Extract the rows 100 to 200 & all columns
sub_lena = lena(100:200, :, :);
figure, imshow(sub_lena);

% Accessing color channels: third index -> [rows, cols, channel]
red_lena = lena(:,:,1);
figure, imshow(red_lena);

% Convert to grayscale and use different colormap
gray_lena = rgb2gray(lena);
figure, imshow(gray_lena);

% Convert to other colorspace
hsv_lena = rgb2hsv(lena);

% Only show saturation
sat_lena = hsv_lena(:,:,2);
figure, imshow(sat_lena);

% Save image
imwrite(sat_lena, 'sat_lena.jpg');