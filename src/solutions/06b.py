# https://adventofcode.com/2023/day/6

# Regular imports

from __future__ import annotations
import math
from typing import Iterable
import re

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

def stripped_lines(f) -> Iterable:
    return filter(None, map(str.strip, f.readlines()))

# Constants

RE_NUM = r'(\d+)'

# Helpers



# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    duration = int(''.join(c for c in f.readline() if c.isdigit()))
    record = int(''.join(c for c in f.readline() if c.isdigit()))
    print(duration, record)

    n = 0

    for ms in range(1, duration):
        remaining = duration - ms
        distance = ms * remaining
        if distance > record:
            result += 1

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
