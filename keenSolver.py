from itertools import product
import random, sys
from collections import deque, defaultdict
from copy import deepcopy
from NonogramSolver import NonogramSolver

# one big dict for everything!
# grid has tuple keys to point objects
# grid has -int keys to row tuple
# grid has +int keys to col tuple
# r/c tuple is (clue list, point list)
# everything is change-in-place

class Point(object):
    "0: unknown, 1: filled, -1: empty"
    # using an object for free updates across references
    def __init__(self):
        self.i = 0
    def __repr__(self):
        chars = {0:'~', -1:' ', 1:'O'}
        return chars[self.i]

def load_grid(rows,cols):
    height = len(rows)
    width  = len(cols)
    grid = defaultdict(Point)
    # points get implicitly inserted
    # link rows and cols to points
    # add one to stuff because you can't have row +0 and col -0
    for x,clue in enumerate(cols):
        x += 1
        grid[x] = (clue, [grid[(x,y+1)] for y in range(height)])
    for y,clue in enumerate(rows):
        y += 1
        grid[-y]  = (clue, [grid[(x+1,y)] for x in range(width)])
    return grid

def finished(grid):
    return not any(k for k,v in list(grid.items()) if type(k)==tuple and v.i==0)

def map2d(fn, grid):
    "apply fn to row, cols in both directions"
    kset = set(k for k in grid if type(k) == int)
    changed = False
    for k in kset:
        pi1 = ''.join(repr(p) for p in grid[k][1])
        c1 = deepcopy(grid[k][0])
        fn(*grid[k])
        grid[k][0].reverse()  # clue
        grid[k][1].reverse()  # points
        clean(grid)
        if k in grid:
            fn(*grid[k])
        clean(grid)
        # perfectly okay to leave it backwards though
        if k in grid:
            grid[k][0].reverse()  # clue
            grid[k][1].reverse()  # points
            pi2 = ''.join(repr(p) for p in grid[k][1])
            c2 = grid[k][0]
        else:
            pi2,c2 = '',[]
        if pi1 != pi2 or len(c1) != len(c2):
            changed = True 
    return changed

def clean(grid):
    to_pop = []
    for k,v in grid.items():
        if type(k) != int:
            continue
        clue,points = v
        empty(clue, points)
        clean_points(clue, points)
        if not (clue and points):
            to_pop.append(k)
    for k in to_pop:
        grid.pop(k)

def empty(clue, points):
    "no clue, all empty"
    if len(clue) != 0:
        return
    for i,p in enumerate(points):
        if p.i == 0:
            points[i].i = -1

def clean_points(clue, points):
    "remove solved empties from edge"
    while points and points[0].i == -1:
        points.pop(0)

def blank(clue, points):
    if len(clue) != 1 or clue[0] != 0:
        return
    for p in points:
        assert p.i != 1
        p.i = -1

def center(clue, points):
    "mark self overlapping midsection"
    l = len(points) - (sum(clue[1:]) + len(clue) - 1)
    pi = [p.i for p in points[:l]]
    c = clue[0]
    if -1 in pi and 1 in pi and pi.index(1) < pi.index(-1):
        l = min(l, pi.index(-1))
    if 1 in pi[:c]:
        l = min(l, pi.index(1) + c)
    assert l>=c
    if l//2 >= c:
        return
    for i in range(l-c, c):
        assert points[i].i != -1
        points[i].i = 1

def edge(clue, points):
    "fill out leading edge, remove clue"
    if not points or points[0].i != 1:
        return
    c = clue[0]
    for p in points[:c]:
        assert p.i != -1
        p.i = 1
    if c < len(points):
        assert points[c].i != 1
        points[c].i = -1
    for i in range(min(c+1, len(points))):
        points.pop(0)
    clue.pop(0)

def edge_dot(clue, points):
    "blank before a dot"
    if clue[0] != 1:
        return
    pi = [p.i for p in points[0:2]]
    if pi != [0,1]:
        return
    points[0].i = -1

def unique(clue, points):
    "add empty space before unique"
    c = clue[0]
    if max(clue) != c:
        return
    if sum(c1==c for c1 in clue) != 1:
        return
    for i in range(len(points) + 1 - c):
        if not all(p.i==1 for p in points[i:i+c]):
            continue
        for j in range(i):
            assert points[j].i != 1
            points[j].i = -1
        break

def cant_fit(clue, points):
    "blank out small holes"
    if points[0].i != 0:
        return
    c = clue[0]
    pl = [p.i for p in points]
    if -1 not in pl[:c]:
        return
    pe = pl.index(-1)
    for i in range(pe):
        assert points[i].i != 1
        points[i].i = -1

def cant_reach(clue, points):
    "blank distant edges"
    # changes the FAR edge
    if len(clue) != 1:
        return
    c = clue[0]
    pi = [p.i for p in points]
    if 1 not in pi:
        return
    for i in range(pi.index(1) + c, len(pi)):
        assert points[i].i != 1
        points[i].i = -1


def bad_guess(grid):
    if finished(grid):
        raise
    ks = [k for k,v in list(grid.items()) if type(k)==tuple and v.i==0]
    if not ks:
        raise
    return min(ks), 1

def solve(rows,cols):
    r = deepcopy(rows)
    c = deepcopy(cols)
    grid = load_grid(r,c)
    guess_hist = []
    grid_hist = []
    axioms = [blank, center, edge, unique, cant_fit, cant_reach, edge_dot]
    while not finished(grid):
        changed = False
        try:
            for axiom in axioms:
                changed += map2d(axiom, grid)
        except AssertionError:  # bad guess
            k,v = guess_hist.pop()
            grid = grid_hist.pop()
            if v == 1:
                v = -1
                grid[k].i = v
            changed = True
        if changed:
            continue
        grid_hist.append(deepcopy(grid))
        k,v = bad_guess(grid)
        guess_hist.append((k,v))
        grid[k].i = v
    return grid

def show(grid,row,col):
    height = len(row)
    width  = len(col)
    for y,x in product(list(range(height)), list(range(width))):
        print(grid[(x+1,y+1)], end=' ')
        if x == width-1:
            print()