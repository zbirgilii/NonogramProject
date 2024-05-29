import os, time, random, sys
from itertools import combinations
from collections import deque, defaultdict
from copy import deepcopy
import numpy as np 
import matplotlib.pyplot as plt
from NonogramSolver import NonogramSolver
import keenSolver

row = [
    [9,5],
    [3,6,6],
    [3,7,6],
    [3,3,10],
    [4,3,4],
    [5,2],
    [7,1],
    [9,2],
    [2,1,2],
    [2,2,3],
    [2,6],
    [1,3,1,3,1],
    [5,4,3],
    [4,1,1,2],
    [4,5,4],
    [3,6,1,1],
    [1,1,2,1],
    [1,1,1],
    [1,1,6],
    [4,2,7]
]

col = [
    [2,1,5],
    [3,1,4],
    [4,2,4,1],
    [2,10,2],
    [1,6,1,1],
    [2,4,1,1],
    [8,2],
    [8,2,3],
    [5,10,1],
    [3,3,6],
    [4,7],
    [6,1,1],
    [4,5,1,2],
    [2,2,2],
    [3,1,4,2],
    [4,9],
    [5,2,1,2],
    [5,1,3],
    [5,1,1],
    [5]
]

if __name__ == "__main__":
    # keenSolver
    keenSolver.show(keenSolver.solve(row,col),row,col)

    # Nonogram Solver
    NonogramSolver(row,col).display_board()