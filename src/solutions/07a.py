# https://adventofcode.com/2023/day/7

# Regular imports

from __future__ import annotations
from typing import Iterable

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

STRENGTHS = 'AKQJT98765432'

# Helpers

def is_5oak(hand: str) -> bool:
    return len(set(hand)) == 1

def is_4oak(hand: str) -> bool:
    s = set(hand)
    return any(hand.count(c) == 4 for c in s)

def is_3oak(hand: str) -> bool:
    s = set(hand)
    return (len(s) == 3) and any(hand.count(c) == 3 for c in s)

def is_2pair(hand: str) -> bool:
    s = set(hand)
    return (len(s) == 3) and (sum(hand.count(c) == 2 for c in s) == 2)

def is_1pair(hand: str) -> bool:
    s = set(hand)
    return (len(s) == 4) and (sum(hand.count(c) > 1 for c in s) == 1)

def is_high(hand: str) -> bool:
    return len(set(hand)) == 5

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    pass

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
