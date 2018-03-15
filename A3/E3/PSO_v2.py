import random
import numpy as np
from A3.E3.functions import import_dataset

Nc = 100
Nd = 4
Np = 3

w = 0.2  # Inertia weight
c1 = 0.4  # Acceleration constant 1
c2 = 0.4  # Acceleration constant 2

maxiter = 1000


class Particle:
	def __init__(self, Nc, Nd, data):
		self.Nc = Nc
		self.Nd = Nd
		self.data = data

		self.centroids = [[random.uniform(-1, 1) for _ in range(Nd)] for _ in range(Nc)]
		self.velocity = [[random.uniform(-1, 1) for _ in range(Nd)] for _ in range(Nc)]
		self.best = self.centroids

	def distances(self):
		return [[np.linalg.norm(data - centroid) for index, data in self.data.iterrows()] for centroid in
				self.centroids]

	def fitness(self, assigned_cluster, centroids):
		# Mean average weighted distance from data points to assigned centroid
		return np.mean([np.linalg.norm(z - centroids[c]) for (i, z), c in zip(self.data.iterrows(), assigned_cluster)])

	def update_local_best(self, assigned_cluster):
		self.centroids = self.centroids if self.fitness(assigned_cluster, self.centroids) < self.fitness(
			assigned_cluster, self.best) else self.best

	def update(self, global_y):
		# Update velocity
		self.velocity = [[w * self.velocity[j][k] + \
				   c1 * random.random() * (self.best[j][k] - self.centroids[j][k]) + \
				   c2 * random.random() * (global_y[j][k] - self.centroids[j][k]) for k in range(Nd)] for j in
				  range(Nc)]

		# Update centroids
		self.centroids = [[self.centroids[j][k] + self.velocity[j][k] for k in range(Nd)] for j in range(Nc)]


def main():
	# Import dataset[
	data, label = import_dataset()

	# Initialize each particle to contain Nc randomly selected centroids
	particles = [Particle(Nc, Nd, data) for _ in range(Np)]

	for iter in range(100):
		fitnesses = []
		for particle in particles:
			# Calculate the distance of a data point to each centroid
			distances = particle.distances()

			# Assign z to the cluster centroid with minimal distance
			assigned_cluster = np.argmin(distances, axis=0)

			# Compute the fitness
			fitness = particle.fitness(assigned_cluster, particle.centroids)
			fitnesses.append(fitness)

			particle.update_local_best(assigned_cluster)

		global_best = np.argmin(fitnesses)

		for particle in particles:
			particle.update(particles[global_best].centroids)

		print(fitnesses)


if __name__ == '__main__':
	main()
