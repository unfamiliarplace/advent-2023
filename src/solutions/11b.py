# https://adventofcode.com/2023/day/11

# Regular imports

from __future__ import annotations
from typing import Iterable
import itertools

# My naming convention...

import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Mode

TESTING = False
INPUTS = 'inputs' if not TESTING else 'test_inputs'
OUTPUTS = 'outputs' if not TESTING else 'test_outputs'

# Utilities

def stripped_lines(f) -> Iterable[str]:
    return filter(None, map(str.strip, f.readlines()))

# Constants

EXPANSION = 1_000_000

# Helpers

def get_transposed_grid() -> list[str]:
    trans = [''] * len(grid[0])
    for row in grid:
        for (col, cell) in enumerate(row):
            trans[col] = cell + trans[col] # God knoweth why
    return trans

def find_expandables() -> None:
    for (i, row) in enumerate(grid):
        if not any(c == '#' for c in row):
            expand_rows.add(i)

    for (i, row) in enumerate(get_transposed_grid()):
        if not any(c == '#' for c in row):
            expand_cols.add(i)

def shortest_pair_path(one: tuple[int], other: tuple[int]) -> int:
    n = 0
    sy, sx = one
    ty, tx = other

    while sx != tx:
        sx += (tx - sx) // abs(tx - sx)
        n += 1

        if sx in expand_cols:
            n += (EXPANSION - 1)

    while sy != ty:
        sy += (ty - sy) // abs(ty - sy)
        n += 1

        if sy in expand_rows:
            n += (EXPANSION - 1)

    return n

# Logic

grid: list[str] = []
galaxies: set[tuple[int]] = set()
expand_rows = set()
expand_cols = set()
result: int = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        grid.append(line)
                
    find_expandables()

    for (i_row, row) in enumerate(grid):
        for (i_col, col) in enumerate(row):
            if col == '#':
                galaxies.add((i_row, i_col))

    for pair in itertools.combinations(galaxies, 2):
        result += shortest_pair_path(*pair)
    
with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
