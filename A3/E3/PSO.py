"""
PSO
"""
import random
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import confusion_matrix

from A3.E3.functions import import_dataset

number_of_particles = 10

w = 0.4  # Inertia weight
c1 = 0.3  # Acceleration constant 1
c2 = 0.3  # Acceleration constant 2

def euclidean_distance(a, b):
	return np.linalg.norm(a - b)


class Particle:
	def __init__(self, centroids, num_dimensions):
		# Initialize each particle to contain Nc randomly selected centroids
		self.centroids = [[random.uniform(0, 4) for _ in range(num_dimensions)] for _ in range(centroids)]
		self.velocities = [[random.uniform(-1, 1) for _ in range(num_dimensions)] for _ in range(centroids)]
		self.assigned_centroids = [[] for _ in range(centroids)]
		self.fitness_local_best = np.inf
		self.centroid_local_best = None

	def get_distances(self, data):
		return [euclidean_distance(data, centroid) for centroid in self.centroids]

	def assign_centroid(self, distances):
		closest = np.argmin(distances)
		self.assigned_centroids[int(closest)].append(distances[np.argmin(distances)])
		return closest

	def fitness(self):
		return np.mean([np.mean([distance for distance in assigned_centroid]) for assigned_centroid in self.assigned_centroids if len(assigned_centroid) > 0])

	def local_best(self, fitness):
		if fitness < self.fitness_local_best:
			self.fitness_local_best = fitness
			self.centroid_local_best = self.centroids

	def update(self, global_best):
		self.velocities = np.multiply(w, self.velocities) + np.multiply(c1 * random.random(), np.subtract(self.centroid_local_best, self.centroids)) + np.multiply(c2 * random.random(), np.subtract(global_best, self.centroids))
		self.centroids = np.add(self.velocities, self.centroids)

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
	ax.set_title('PCO')
	ax.dist = 12

	plt.show()

class PSO():
	def __init__(self, data, y, centroids, particles):
		'''
		Initialize swarm
		:param data:
		'''
		self.data = data
		self.y = y
		self.centroids = centroids
		self.num_dimensions = len(data.columns)
		self.particles = [Particle(self.centroids, self.num_dimensions) for _ in range(particles)]
		self.fitness_global_best = np.inf

	def train(self, iterations):
		# For iter=1 to iterations
		global assigned, final_assigned
		for i in tqdm(range(iterations)):

			# For each particle i = (m_i1, ..., m_iNc)
			for particle in self.particles:
				assigned = []

				# For each data point z
				for i, dp in self.data.iterrows():

					# Calculate the distance of z to each m_ij (j=1,..,Nc)
					distances = particle.get_distances(dp)

					# Assign z to the cluster (centroid) with minimal distance
					ac = particle.assign_centroid(distances)
					assigned.append(ac)

				# Compute the fitness
				fitness = particle.fitness()

				# Update the local best
				particle.local_best(fitness)

				# Update global best
				if fitness < self.fitness_global_best:
					final_assigned = assigned
					self.fitness_global_best = fitness
					self.particle_global_best = particle

			# Update the cluster centroids using PSO update rules
			for particle in self.particles:
				particle.update(self.particle_global_best.centroids)

		statistics(self.data, self.y, np.array(final_assigned))



def main():
	x, y = import_dataset()
	pso = PSO(x, y, centroids=3, particles=number_of_particles)
	pso.train(1000)

if __name__ == "__main__":
	main()
