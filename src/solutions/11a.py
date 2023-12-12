# https://adventofcode.com/2023/day/11

# Regular imports

from __future__ import annotations
from typing import Iterable
from termcolor import cprint

# My naming convention...

import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Mode

TESTING = True
INPUTS = 'inputs' if not TESTING else 'test_inputs'
OUTPUTS = 'outputs' if not TESTING else 'test_outputs'

# Utilities

def stripped_lines(f) -> Iterable[str]:
    return filter(None, map(str.strip, f.readlines()))

# Constants

# Helpers

# class Space:
#     next_id: int=0
#     id: int
#     symbol: str
#     x: int
#     y: int

#     def __init__(self: Space, symbol: str, x: int, y: int) -> None:
#         self.id = Space.next_id
#         Space.next_id += 1

#         self.symbol = symbol
#         self.x, self.y = x, y
#         self.exits = set()

#     def space_from(self: Space, dx: int, dy: int) -> Space|None:
#         nx, ny = self.x + dx, self.y + dy
#         if (-1 < nx < len(app.grid[0])) and (-1 < ny < len(app.grid)):
#             return app.grid[ny][nx]

#     def surrounding(self: Space) -> set[Space]:
#         surr = set()
#         for (dx, dy) in ((-1, 0), (0, -1), (1, 0), (0, 1)):
#             other = self.space_from(dx, dy)

#             if (other is not None):
#                 surr.add(other)
        
#         return surr
    
#     def is_galaxy(self: Space) -> bool:
#         return self.symbol == '#'

#     def on_edge(self: Space) -> bool:
#         return any((
#             self.x == 0,
#             self.y == 0,
#             self.x == (len(app.grid[0]) - 1),
#             self.y == (len(app.grid) - 1)
#         ))
    
#     def __hash__(self: Space) -> int:
#         return hash(self.id)
            
#     def __eq__ (self: Space, other: object) -> bool:
#         if not isinstance(other, Space):
#             return False
        
#         return self.id == other.id
    
#     def __str__(self: Space) -> str:
#         return self.symbol
    
#     def __repr__(self: Space) -> str:
#         s = f'{self.id:>3}: {self.symbol} ([{self.y}][{self.x}])'
#         return s

def expand_grid() -> None:

    # Expand horizontally
    expanded = []
    for (i_row, row) in enumerate(grid):
        expanded_row = ''

        for (i_col, space) in enumerate(row[1:]):
            prev, curr = row[i_col], space
            expanded_row += prev

            if i_col in expand_cols:
                expanded_row += '.'

        expanded_row += curr
        expanded.append(expanded_row)

    # Expand vertically
    expanded2 = [expanded[0]]
    for (i_row, row) in enumerate(expanded[1:]):

        if i_row in expand_rows:
            expanded2.append('.' * len(row))
        
        expanded2.append(row)

    # Update grid
    grid[:] = expanded2

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

# Logic

grid: list[str] = []
galaxies: set[tuple[int]] = set()
expand_rows = set()
expand_cols = set()
result: int = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for (i_row, line) in enumerate(stripped_lines(f)):
        grid.append(line)
        for (i_col, cell) in enumerate(line):
            if cell == '#':
                galaxies.add((i_row, i_col))
                
    find_expandables()
    expand_grid()
    
with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
