% Load Lena and Lena_with_glasses
lena = imread('../lena.jpg');
lena_glass = imread('../lena_glass.jpg');
lena_gray = rgb2gray(lena);

% ====== Point operators =======
% ------ Pixelweise subtraction ------
glass = lena - lena_glass;
figure, imshow(glass);

% ====== Local operators =======
% ------ Mean filter ------
h = 1/5*ones(5,1);
H = h*h';
mean_lena = filter2(H, lena_gray);
imshow(mean_lena, []);
 
% ====== Global operators ======
% ------ Fourier transformation ------
F = fft2(lena_gray);
figure, imshow(log(F +1),[]);
F_c = fftshift(F);
figure, imshow(log(F_c +1),[]);

% Apply an ideal high-pass filter in the fourier space
[M,N] = size(lena_gray);
H = ideal_highpass( M,N,60.0 );
H1 = fftshift(H);
filt_fft = F_c .* H1;
figure, imshow(log(filt_fft+1), []);
filt_ifft = ifft2( ifftshift( filt_fft ) );
figure, imshow(filt_ifft,[0 255]);