# https://adventofcode.com/2023/day/1

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
    pass

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
