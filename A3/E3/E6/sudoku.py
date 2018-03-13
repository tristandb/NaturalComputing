import numpy as np
from os import getcwd
from collections import Counter
Q = 1.0
P = 0.2

class ACO:
	def __init__(self, puzzle):
		self.sudoku = np.ones((81, 9), np.float)
		self.init_puzzle = np.copy(puzzle.flatten())
		self.iterations = 50000

		self.valid_solutions = [[x for x in range(1, 10)] if cell == 0. else [int(cell)] for cell in sudoku.flatten()]
		self.initial_value = 1
		self.pheromones = []
		for i in range(len(self.valid_solutions)):
			if i == 0:
				self.pheromones.append(np.multiply(self.initial_value, np.ones((1, len(self.valid_solutions[i])))))
			else:
				self.pheromones.append(np.multiply(self.initial_value, np.ones((len(self.valid_solutions[i-1]), len(self.valid_solutions[i])))))

		self.emptymatrix = []
		for i in range(len(self.valid_solutions)):
			if i == 0:
				self.emptymatrix.append(np.zeros((1, len(self.valid_solutions[i]))))
			else:
				self.emptymatrix.append(np.zeros((len(self.valid_solutions[i-1]), len(self.valid_solutions[i]))))

	def get_matrix(self):
		return self.emptymatrix

	def duplicates(self, array):
		counts = Counter(array)
		return sum(counts.values()) - len(counts.values())

	def fitness(self):
		"""
		Returns fitness of the sudoku
		:return:
		"""

		# Calculate duplicates for rows
		duplicates_rows = np.sum([self.duplicates(row) for row in self.puzzle])

		# Calculate duplicates for columns
		duplicates_columns = np.sum([self.duplicates(self.puzzle[:, i]) for i in range(0, len(self.puzzle))])

		# Calculate duplicates for subblocks
		grid = np.vsplit(self.puzzle, 3)
		grid = np.array([np.hsplit(split,3) for split in grid]).reshape(9, 3, 3)

		duplicates_blocks = sum([self.duplicates(g.flatten()) for g in grid])

		return (duplicates_blocks + duplicates_rows + duplicates_columns + 1) ** 0.5

	def update_pheromone(self, fitness, puzzle):
		empty_pheromone_matrix = self.get_matrix()
		for i, digit in enumerate(puzzle.flatten()):
			sol = self.valid_solutions[i].index(digit)
			for a in empty_pheromone_matrix[i]:
				a[sol] = Q/fitness
		self.pheromones = np.multiply(self.pheromones, 1 - P) + empty_pheromone_matrix

	def construct_solution(self):
		picked = 0
		self.puzzle = np.copy(self.init_puzzle)

		for i in range(81):
			aa = self.pheromones[i][picked]
			distribution = (aa/ np.sum(aa))

			picked = np.random.choice(len(distribution), replace=True, p=distribution)

			# Only change 0's.
			if self.puzzle[i] == 0.:
				# Choose one of the solutions
				self.puzzle[i] = self.valid_solutions[i][picked]

		self.puzzle = self.puzzle.reshape(9, 9)
		return self.puzzle

	def solve(self):
		"""
		Tries to solve the sudoku
		:return:
		"""

		for i in range(self.iterations):
			fitnesses = []
			puzzles = []
			for j in range(40):
				# Construct solution
				puzzles.append(self.construct_solution())

				# Calculate fitness
				fitnesses.append(self.fitness())

			# Update pheromones
			fitmaxindex = np.argmin(fitnesses)
			print(i, fitnesses[fitmaxindex])
			self.update_pheromone(fitnesses[fitmaxindex], puzzles[fitmaxindex])



if __name__ == '__main__':
	sudoku = np.loadtxt(getcwd() + '/puzzles/s10a.txt').reshape(81, 1)
	aco = ACO(puzzle=sudoku)
	aco.solve()