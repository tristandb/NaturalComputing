from collections import Counter
import numpy as np
import sys
import os
ALPHA = .5
BETA = 1
N_ANTS = 10
P = .025
Q = 1.0
ITERATIONS = 1000000
def calc_duplicates(r):
    # for every i in r sum(#i - 1) if #i > 0
    c = Counter(r)
    return sum(c.values()) - len(c.values())

def calc_cost(solution):
    shape = solution.shape
    # sum duplicates in rows and cols
    s_rows = sum([calc_duplicates(r) for r in solution])
    s_cols = sum([calc_duplicates(solution[:,i]) for i in range(0, shape[1])])

    # make Sodoku 3x3 sub-grid by splitting first vertically and then horizontally
    grid = np.vsplit(solution,3)
    grid = np.array([np.hsplit(s,3) for s in grid]).reshape(9, 3, 3)

    # now the array exists of the 9x 3x3 arrays
    s_grid = sum([calc_duplicates(g.flatten()) for g in grid])

    return (s_rows + s_cols + s_grid + 1) ** .5 # sum by one to prevent division by zero

def calc_costs(solutions):
    return [calc_cost(s) for s in solutions]

def generate_solution(path,index,p):
    # stop recursion when complete solution is found
    if index == 81:
        return np.array(path).reshape(9,9)

    # replace only zeros
    if path[index] == 0:
        # unnormalized probabilities for each of the 9 possible choices
        probs = np.multiply(np.power(p[index], ALPHA), np.power(float(1)/float(9), BETA))
        #normalized:
        probs = np.divide(probs, np.sum(probs))
        #choose one according to the found probability distribution
        path[index] = np.random.choice(range(1,10), 1, p=probs)
    return generate_solution(path,index+1,p)


def generate_solutions(p, sudoku):
    return [generate_solution(sudoku, 0, p) for i in range(0, N_ANTS)]

def update_pheromone(p,s,l):
    d = np.zeros((81,9),np.float)
    for k in range(0,len(l)):
        lk = l[k]
        sk = s[k]
        for pos,digit in enumerate(sk.flatten()):
            d[pos,int(digit-1)] = Q/lk

    return np.multiply(p,1-P) + d

def ACO(sudoku):
    p = np.multiply(np.ones((81, 9), np.float), float(1)/float(9))
    L = 1000000
    i = ITERATIONS
    while L > 1 and i > 0:
        path = np.copy(sudoku)
        s = generate_solutions(p, path)
        l = calc_costs(s)
        p = update_pheromone(p, s, l)
        l.append(L)
        L = min(l)
        i -= 1
        print(i,L)
    print(L)

def main(file):
    #init pheromone equally
    sudoku = np.loadtxt(os.getcwd() + '/' + file).reshape(81,1)
    ACO(sudoku)



if __name__ == '__main__':
    a = sys.argv
    if len(a) > 1:
        main(a[1])
    else:
        print("No soduku puzzle given")