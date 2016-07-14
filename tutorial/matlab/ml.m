%basic machine learning in matlab
%to use some of the functions and data, you have to download VLFeat: http://www.vlfeat.org/
%this tutorial is the same you can find on their webpage.
run('vlfeat-0.9.20/toolbox/vl_setup.m');
vl_setup demo;
load('vl_demo_svm_data.mat');

X_positive = X(:,y==1);
X_negative = X(:,y==-1);

figure
plot(X_negative(1,:),X_negative(2,:),'*r')
hold on
plot(X_positive(1,:),X_positive(2,:),'*b')
axis equal ;

lambda = 0.01 ; % Regularization parameter
maxIter = 1000 ; % Maximum number of iterations

% Train the SVM given the dataset
[w b info] = vl_svmtrain(X, y, lambda, 'MaxNumIterations', maxIter);

% Visualisation
eq = [num2str(w(1)) '*x+' num2str(w(2)) '*y+' num2str(b)];
line = ezplot(eq, [-0.9 0.9 -0.9 0.9]);
set(line, 'Color', [0 0.8 0],'linewidth', 2);