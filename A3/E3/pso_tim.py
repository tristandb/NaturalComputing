import random
import numpy as np
from A3.E3.functions import import_dataset

Nd = 3  #Number of dimensions
Nc = 10 #Number of clusters
Np = 50 #Number of particles

w = 0.2	 #Inertia weight
c1 = 0.4 #Acceleration constant 1
c2 = 0.4 #Acceleration constant 2

maxiter = 1000 #Number of iterations

def euclid_distance(a, b):
	return np.linalg.norm(a - b)

class Particle:
	def __init__(self, Nd, Nc, data):
		'''
		Create new particle
		:param Nd: Number of dimensions
		:param Nc: Number of clusters
		:param data: Data
		'''
		self.Nd = Nd
		self.Nc = Nc
		self.data = data

		self.x = [[random.uniform(-1, 1) for _ in range(Nd)] for _ in range(Nc)] #Current position
		self.v = [[random.uniform(-1, 1) for _ in range(Nd)] for _ in range(Nc)] #Current velocity
		self.y = self.x #Personal best position

	def fitness(self, position):
		return 1
		return sum([sum([]) for j in range(self.Nc)]) / self.Nc

	def update(self, global_y):
		#Update v
		self.v = [[w*self.v[j][k] + \
			c1*random.random()*(self.y[j][k] - self.x[j][k]) + \
			c2*random.random()*(global_y[j][k] - self.x[j][k]) for k in range(Nd)] for j in range(Nc)]

		#Update x
		self.x = [[self.x[j][k] + self.v[j][k] for k in range(Nd)] for j in range(Nc)]

		#Update personal best position
		self.y = self.x if self.fitness(self.x) < self.fitness(self.y) else self.y

if __name__ == '__main__':
	particles = [Particle(Nd, Nc, []) for _ in range(Np)]
	print(particles)
	data = []
	for t in range(maxiter):
		for particle in particles:
			for z in data:
				pass
			particle.update(particles[0].y)