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

ways = []

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    durations = [int(m.group(1)) for m in re.finditer(RE_NUM, f.readline())]
    records = [int(m.group(1)) for m in re.finditer(RE_NUM, f.readline())]

    for (duration, record) in zip(durations, records):
        n = 0

        for ms in range(1, duration):
            remaining = duration - ms
            distance = ms * remaining
            if distance > record:
                n += 1
        
        ways.append(n)

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    result = math.prod(ways)
    f.write(f'{result}')
