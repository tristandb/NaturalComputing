#    This file is part of EAP.
#
#    EAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    EAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with EAP. If not, see <http://www.gnu.org/licenses/>.

import random
import operator
import csv
import itertools

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# Read the spam list features and put it in a list of lists.
# The dataset is from http://archive.ics.uci.edu/ml/datasets/Spambase
# This example is a copy of the OpenBEAGLE example :
# http://beagle.gel.ulaval.ca/refmanual/beagle/html/d2/dbe/group__Spambase.html
with open("numberbase.csv") as numberbase:
	numberReader = csv.reader(numberbase)
	numbers = list(list(float(elem) for elem in row) for row in numberReader)

print(numbers)

# defined a new primitive set for strongly typed GP
pset = gp.PrimitiveSetTyped("MAIN", itertools.repeat(float, 57), float, "IN")

# Define a protected division function
def protectedDiv(left, right):
	try:
		return left / right
	except ZeroDivisionError:
		return 1

pset.addPrimitive(lambda x: numpy.math.log(x), [float], float, name="log")
pset.addPrimitive(lambda x: numpy.math.exp(x), [float], float, name="exp")
pset.addPrimitive(lambda x: numpy.math.sin(x), [float], float, name="sin")
pset.addPrimitive(lambda x: numpy.math.cos(x), [float], float, name="cos")

pset.addPrimitive(operator.add, [float, float], float)
pset.addPrimitive(operator.sub, [float, float], float)
pset.addPrimitive(operator.mul, [float, float], float)
pset.addPrimitive(protectedDiv, [float, float], float)

pset.addTerminal("x", float)

def fitness(individual):
    data = zip([x/10.0 for x in range(-10, 11, 1)], \
        [0.0000, -0.1629, -0.2624, -0.3129, \
        -0.3264, -0.3125, -0.2784, -0.2289, \
        -0.1664, -0.0909, 0.0, 0.1111, \
        0.2496, 0.4251, 0.6496, 0.9375, \
        1.3056, 1.7731, 2.3616, 3.0951, \
        4.000])

    score = 0
    for inp, out in data:
        score += (individual(inp) - out)**2
    return score

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


def evalSpambase(individual):
	# Transform the tree expression in a callable function
	func = toolbox.compile(expr=individual)
	# Randomly sample 400 mails in the spam database
	spam_samp = random.sample(numbers, 400)
	# Evaluate the sum of correctly identified mail as spam
	result = sum(bool(func(*mail[:57])) is bool(mail[57]) for mail in spam_samp)
	return result,


toolbox.register("evaluate", evalSpambase)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)


def main():
	pop = toolbox.population(n=1000)
	hof = tools.HallOfFame(1)
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", numpy.mean)
	stats.register("std", numpy.std)
	stats.register("min", numpy.min)
	stats.register("max", numpy.max)

	algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 1, stats, halloffame=hof)

	return pop, stats, hof


if __name__ == "__main__":
	main()