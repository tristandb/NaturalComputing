from random import randint
import matplotlib.pyplot as plt

def fitness(individual):
	return sum(individual)

def new_individual(length):
	return [randint(0, 1) for _ in range(length)] 

def monte_carlo(fitness, length, max_gen):
	individual = new_individual(length)
	best = individual
	history = [fitness(individual)]

	for _ in range(max_gen-1):
		individual = new_individual(length)
		if fitness(individual) > fitness(best):
			best = individual
		history += [fitness(best)]

	print("Best individual: ", best)
	print("Fitness: ", fitness(best))
	plt.xlabel("Iterations")
	plt.ylabel("Fitness")
	plt.plot(range(0, max_gen), history)
	plt.show()

def main():
	monte_carlo(fitness, 100, 1500)

if __name__ == "__main__":
	main()