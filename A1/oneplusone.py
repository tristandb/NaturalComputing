import numpy as np
import matplotlib.pyplot as plt
from random import randint
from random import random as rand

def new_individual(length):
    return [randint(0, 1) for _ in range(length)]

def fitness(individual):
    return np.sum(individual)

def flip(individual, p):
    return [int(not bit) if rand() < p else bit for bit in individual]

def genetic_algorithm(fitness, length, max_gen):
    p = 1 / length
    individual = new_individual(length)
    history = [fitness(individual)]

    for _ in range(max_gen - 1):
        x_m = flip(individual, p)
        if fitness(x_m) > fitness(individual):
            individual = x_m
        history += [fitness(individual)]

    print("Best individual: ", individual)
    print("Fitness: ", fitness(individual))
    plt.xlabel("Iterations")
    plt.ylabel("Fitness")
    plt.plot(range(0, max_gen), history)
    #plt.show()

def main():
    genetic_algorithm(fitness, 100, 1500)

if __name__ == "__main__":
    for _ in range(10):
        main()
