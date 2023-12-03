# https://adventofcode.com/2023/day/3

# Regular imports
from typing import Iterable
import re

# My naming convention...
import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Utilities

def stripped_lines(f) -> Iterable:
    return filter(None, map(str.strip, f.readlines()))

# Constants

RE_DIGITS = r'(\d+)'

# Helpers

def is_symbol(s: str) -> bool:
    return s in '!@#$%^&*-=_+[]{};:,<>/?\\|\'\"~`'

def is_adjacent_to_symbol(i_row: int, start: int, end: int) -> bool:
    for i_g_row in range(max(0, i_row - 1), min(len(grid), i_row + 2)):
        g_row = grid[i_g_row]
        adj_start = max(0, start - 1)
        adj_end = min(len(g_row), end + 1)
        adj_space = g_row[adj_start:adj_end]
        if any(is_symbol(c) for c in adj_space):
            return True
    return False

# Logic

result = 0
grid = []

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    grid = [line for line in stripped_lines(f)]
    for (i_row, line) in enumerate(grid):
        for m in re.finditer(RE_DIGITS, line):
            start, end = m.start(), m.end()
            n = int(m.group())

            if is_adjacent_to_symbol(i_row, start, end):
                result += n

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
