# https://adventofcode.com/2023/day/9

# Regular imports

from __future__ import annotations
from typing import Iterable
import numpy

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



# Helpers

def predict_next_in_sequence(sequence: list[int]) -> int:
    to_come = 0
    diffs = sequence

    while set(diffs) != {0}:
        to_come += diffs[-1]
        diffs = list(numpy.diff(diffs))
        
    return to_come

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        sequence = list(int(n) for n in line.split())
        result += predict_next_in_sequence(sequence)

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
