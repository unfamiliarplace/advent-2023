# https://adventofcode.com/2023/day/4

# Regular imports
from typing import Iterable

# My naming convention...
import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Utilities

def stripped_lines(f) -> Iterable:
    return filter(None, map(str.strip, f.readlines()))

# Constants



# Helpers



# Logic

result = 0

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        _, line = line.split(':')
        winning, having = line.split('|')
        winning = set(int(n) for n in winning.strip().split())
        having = set(int(n) for n in having.strip().split())

        both = having.intersection(winning)
        if both:
            result += 2 ** (len(both) - 1)

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
