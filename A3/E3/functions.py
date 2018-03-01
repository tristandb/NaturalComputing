from sklearn import datasets
import pandas as pd
import numpy as np


def distance(point, centroid):
	"""
	Returns Euclidean distance from a point to a centroid.
	:param point:
	:param centroid:
	:return:
	"""
	return np.linalg.norm(point - centroid)

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