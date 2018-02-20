import numpy as np
"""
Travelling salesman problem in an EA

"""

distances = [[0, 100, 2, 3, 4],
			[100, 0, 4, 5, 6],
			[2, 4, 0, 7, 8],
			[3, 5, 7, 0, 9],
			[4, 6, 8, 9, 0]]

def fitness(individual, distances, length):
	return np.sum([distances[individual[i]][individual[i + 1]] for i in range(length - 1)])

def swap(individual):
	first = np.random.randint(0, len(individual))
	second = np.random.randint(0, len(individual))
	while second == first:
		second = np.random.randint(0, len(individual))

	individual[first], individual[second] = individual[second], individual[first]
	return individual

def cross_over(individuals):
	return individuals

def new_individual(length):
	return np.random.permutation([i for i in range(length)])

def tsp(distances, max_gen, individual_count):
	length = len(distances)
	p = 1 / length

	individuals = [new_individual(length) for _ in range(individual_count)]
	history = [fitness(individual, distances, length) for individual in individuals]

	for _ in range(max_gen - 1):
		# Perform crossover
		individuals = cross_over(individuals)

		# Perform selection
		fitnesses = [fitness(individual, distances, length) for individual in individuals]

		proportion = np.subtract([np.max(fitnesses) for _ in range(individual_count)], fitnesses)

		proportion_list = [individuals[j] for j in range(individual_count) for _ in range(proportion[j])]

		print("proportion: {}".format(proportion))
		print("fitnesses: {}".format(fitnesses))

		individuals = [individuals[np.argmin(fitnesses)]]
		individuals += [swap(proportion_list[np.random.randint(0, np.sum(proportion))]) for _ in range(individual_count - 1)]


def main():
	tsp(distances, 10, 3)

if __name__ == "__main__":
	main()