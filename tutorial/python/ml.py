import numpy as np
import scipy.io
import matplotlib.pyplot as plt

from sklearn import svm

# Load matlab data
data = scipy.io.loadmat('../vl_demo_svm_data.mat')

# Save training data and class labels
y = data['y'][0]
X = data['X']

# Replace class label -1 with 0
y[y < 0] = 0

print(X.shape, y.shape)

# Load Support Vector Classifier
clf = svm.SVC(kernel="linear")
# # Fit the training data
clf.fit(X.T, y)

w = clf.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(-1, 1)
yy = a * xx - (clf.intercept_[0]) / w[1]


plt.scatter(X[0], X[1], marker='x', c=y)
plt.ylim((-1.1,1.1))



new_points = np.array([
				[-.4,-.7],
				[-.7,.5],
			  	[.5,-.5],
			  	[.3,.15],
			  	[-.9,-.65],
			  	])

predictions = clf.predict(new_points)

plt.scatter(new_points.T[0], new_points.T[1], c=predictions, s=100)
plt.plot(xx, yy, 'g-', lw=3)
plt.axes().set_aspect('equal', 'datalim')
plt.show()


