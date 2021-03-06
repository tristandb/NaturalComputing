import random
import operator
import csv
import itertools
import math

import matplotlib.pyplot as plt

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


def evalfitness(individual, verbose=False):
	data = zip([x/10.0 for x in range(-10, 11, 1)], \
		[0.0000, -0.1629, -0.2624, -0.3129, -0.3264, \
		-0.3125, -0.2784, -0.2289, 	-0.1664, -0.0909, \
		0.0, 0.1111, 0.2496, 0.4251, 0.6496, 0.9375, \
		1.3056, 1.7731, 2.3616, 3.0951, 4.000])
	if verbose:
		print('Input\tTarget\tActual\tAbsolute Difference')

	func = toolbox.compile(expr=individual)

	score = 0
	for inp, out in data:
		try:
			if verbose:
				print('{}\t{}\t{}\t{}'.format(inp, round(func(inp), 3), out, round(abs(func(inp)-out), 3)))

			score += abs(func(inp) - out)
		except OverflowError:
			score += 10**8
	return score,

def safeDiv(left, right):
	try:
		return left / right
	except ZeroDivisionError:
		return 0

def safeLog(x):
	try:
		return math.log(x)
	except ValueError:
		return 0


pset = gp.PrimitiveSet("MAIN", 1)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(safeDiv, 2)
pset.addPrimitive(operator.neg, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
pset.addPrimitive(safeLog, 1)
pset.addPrimitive(math.exp, 1)
pset.addEphemeralConstant('constant', lambda: random.uniform(-1, 1))
pset.renameArguments(ARG0="x")

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=2, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
toolbox.register("evaluate", evalfitness)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


def main():
	pop = toolbox.population(n=1000)
	hof = tools.HallOfFame(1)
	stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
	stats_size = tools.Statistics(key=len)
	stats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)
	stats.register("size", numpy.size)

	pop, logbook = algorithms.eaSimple(pop, toolbox, 0.7, 0.0, 50, stats, halloffame=hof)


	logbook.header = "gen", "evals", "fitness", "size"
	logbook.chapters["fitness"].header = "min", "avg", "max"
	logbook.chapters["size"].header = "min", "avg", "max"

	gen = logbook.select("gen")
	fit_mins = logbook.chapters["fitness"].select("min")
	fit_avgs = logbook.chapters["fitness"].select("avg")
	size_avgs = logbook.chapters["size"].select("avg")
	size_mins = logbook.chapters["size"].select("min")

	fig, ax1 = plt.subplots()
	line1 = ax1.plot(gen, fit_mins, "b-", label="Minimum Fitness")
	ax1.set_xlabel("Generation")
	ax1.set_ylabel("Fitness", color="b")
	for tl in ax1.get_yticklabels():
		tl.set_color("b")

	ax2 = ax1.twinx()
	line2 = ax2.plot(gen, size_mins, "r-", label="Minimum Size")
	ax2.set_ylabel("Size", color="r")
	for tl in ax2.get_yticklabels():
		tl.set_color("r")

	lns = line1 + line2
	labs = [l.get_label() for l in lns]
	ax1.legend(lns, labs, loc="center right")

	plt.show()

	return pop, stats, hof



if __name__ == "__main__":
	main()