from collections import Counter

import numpy as np
from os import getcwd
from tqdm import tqdm, trange

Q = 1.0
P = 0.025

num_ants = 100

class ACO:
	def __init__(self, puzzle):
		self.sudoku = np.ones((9, 9, 9), np.float)
		self.init_puzzle = np.copy(puzzle)
		self.iterations = 50000

		self.pheromones = np.ones((81, 9, 81, 9))

		# Set diagonal to -1
		for i in range(len(self.pheromones)):
			self.pheromones[i, :, i, :] = 0.


		# Set solutions that are already filled to 0
		for i, value in enumerate(puzzle.flatten()):
			if int(value) is not 0:
				for j in range(-1, 10):
					if int(value) == j:
						print(int(value), j, i)
						self.pheromones[:, :, i, j-1] = 100000000000.
		return

	def solve(self):
		"""
		Tries to solve the Sudoku
		:return:
		"""
		t = trange(self.iterations)
		self.pheromones
		for i in t:
			fitnesses = []
			puzzles = []
			ant_paths = []
			for i in range(num_ants):
				# Construct a solution
				solution, ant_path = self.construct_solution()
				puzzles.append(solution)
				ant_paths.append(ant_path)

				# Calculate fitness
				fitness = self.calculate_fitness(solution)

				fitnesses.append(fitness)

			# Update pheromones
			best_index = int(np.argmin(fitnesses))
			t.set_postfix({"fitness" : str(fitnesses[best_index])})
			t.update()
			self.update_pheromone(fitnesses[best_index], puzzles[best_index], ant_paths[best_index])

	def calculate_fitness(self, solution):
		"""
		Returns the fitness of the solution
		:param solution:
		:return:
		"""

		# Calculate duplicates for rows
		duplicate_rows = np.sum([self.duplicates(row) for row in solution])

		# Calculate duplicates for columns
		duplicate_cols = np.sum([self.duplicates(solution[:, i]) for i in range(0, len(solution))])

		# Calculate duplicates for subblocks
		grid = np.vsplit(solution, 3)
		grid = np.array([np.hsplit(split, 3) for split in grid]).reshape(9, 3, 3)

		duplicate_blocks = np.sum([self.duplicates(block.flatten()) for block in grid])

		return (duplicate_blocks + duplicate_cols + duplicate_rows + 1) ** 0.5

	def duplicates(self, row):
		return len(row) - len(np.unique(row))

	def construct_solution(self):
		# Select random location
		# TODO: select random location where a value is already set.
		start = np.random.randint(9, size=(3))
		start = [6, 6, 5]
		solution = np.zeros((9, 9))

		solution[start[1], start[0]] = start[2]
		ant_path = []
		current_pheromones = self.pheromones.copy()
		for i in range(80):
			current_position = start[0] + start[1] * 9

			# Current position set pheromones 0
			current_pheromones[:, :, current_position, :] = -0.

			distribution = current_pheromones[current_position, start[2] - 1].flatten()

			probability = distribution/np.sum(distribution)
			picked_move = np.random.choice(len(probability), p=probability)

			current_start = start.copy()
			next_position = picked_move // 9

			start = [next_position % 9, next_position // 9, (picked_move % 9) + 1]
			ant_path.append((current_start, start))
			solution[start[1], start[0]] = start[2]

		return solution, ant_path

	def update_pheromone(self, fitness, solution, path):
		for start, next in path:
			self.pheromones[start[0] + start[1] * 9, start[2] - 1, next[0] + next[1] * 9, next[2] - 1] = (1 - P) * self.pheromones[start[0] + start[1] * 9, start[2] - 1, next[0] + next[1] * 9, next[2] - 1]

		update = np.zeros((81, 9, 81, 9))
		for start, next in path:
			update[start[0] + start[1] * 9, start[2] - 1, next[0] + next[1] * 9, next[2] - 1] = Q/fitness

		self.pheromones += np.multiply(P, update)

if __name__ == '__main__':
	sudoku = np.loadtxt(getcwd() + '/s10a.txt')
	aco = ACO(puzzle=sudoku)
	aco.solve()
