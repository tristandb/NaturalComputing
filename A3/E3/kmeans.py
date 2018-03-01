"""
K-Means Algorithm for clustering.

Often results in the following confusion matrix:

[[50  0  0]
 [ 0 48 14]
 [ 0  2 36]]
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import uniform
from sklearn import datasets
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import confusion_matrix

Nc = 3

def distance(point, centroid):
	"""
	Returns Euclidean distance from a point to a centroid.
	:param point:
	:param centroid:
	:return:
	"""
	return np.linalg.norm(point - centroid)


def move_centroids(points, closest, centroids):
	"""
	Moves centroids to the mean of all assigned data points.
	:param points:
	:param closest:
	:param centroids:
	:return:
	"""
	return np.array([points[closest == k].mean(axis=0) for k in range(len(centroids))])


def import_dataset():
	"""
	Imports the dataset
	:return: Input labels x and output (true) labels y
	"""

	# Import the IRIS dataset.
	iris = datasets.load_iris()

	# Store the inputs as a Pandas DataFrame and set the column names
	x = pd.DataFrame(iris.data)
	x.columns = ['Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width']

	y = pd.DataFrame(iris.target)
	y.columns = ['Targets']

	return x, y


def statistics(x, y, assigned):
	"""
	Generates statistics for the clustering.
	:param x:
	:param y:
	:param assigned:
	:return:
	"""
	print(confusion_matrix(assigned, y))

	fig = plt.figure(1, figsize=(4, 3))
	ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
	ax.scatter(x.loc[:, 'Petal_Width'], x.loc[:, 'Sepal_Length'], x.loc[:, 'Petal_Length'],
			   c=assigned.astype(np.float), edgecolor='k')
	ax.w_xaxis.set_ticklabels([])
	ax.w_yaxis.set_ticklabels([])
	ax.w_zaxis.set_ticklabels([])
	ax.set_xlabel('Petal width')
	ax.set_ylabel('Sepal length')
	ax.set_zlabel('Petal length')
	ax.set_title('K-Means')
	ax.dist = 12

	plt.show()


def main():
	# Import dataset
	x, y = import_dataset()

	old_centroids = []

	# Initial set centroids
	centroids = [uniform(x.min(), x.max()) for _ in range(Nc)]

	# Continue while changes are made
	while not np.array_equal(old_centroids, centroids):
		old_centroids = centroids

		# Calculate distances from points to centroids
		distances = [[distance(point, centroid) for centroid in centroids] for index, point in x.iterrows()]

		# Assign every point to its closest centroid
		assigned = np.argmin(distances, axis=1)

		# Move centroids
		centroids = move_centroids(x, assigned, centroids)

	statistics(x, y, assigned)


if __name__ == '__main__':
	main()
