"""
Ground truth of IRIS-dataset

"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from A3.E3.functions import import_dataset


def statistics(x, y):
	"""
	Generates statistics for the clustering.
	:param x:
	:param y:
	:param assigned:
	:return:
	"""

	fig = plt.figure(1, figsize=(4, 3))
	ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
	ax.scatter(x.loc[:, 'Petal_Width'], x.loc[:, 'Sepal_Length'], x.loc[:, 'Petal_Length'],
			   c=y.loc[:, 'Targets'].astype(np.float), edgecolor='k')
	ax.w_xaxis.set_ticklabels([])
	ax.w_yaxis.set_ticklabels([])
	ax.w_zaxis.set_ticklabels([])
	ax.set_xlabel('Petal width')
	ax.set_ylabel('Sepal length')
	ax.set_zlabel('Petal length')
	ax.set_title('Ground Truth')
	ax.dist = 12

	plt.show()


def main():
	# Import dataset
	x, y = import_dataset()
	statistics(x, y)


if __name__ == '__main__':
	main()
