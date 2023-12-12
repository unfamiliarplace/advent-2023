# https://adventofcode.com/2023/day/12

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

def stripped_lines(f) -> Iterable[str]:
    return filter(None, map(str.strip, f.readlines()))

# Constants



# Helpers

def try_arrangement(slots: str, runs: list[int]) -> int:
    def _placements(_s: str, _b: str) -> list[str]:
        L = []
        for i in range(len(_s)):
            _p = _s[i:i+len(_b)]
            if (len(_p) == len(_b)) and (set(_p) == {'?', '#'}):

                if ((i > 0) and (_s[i-1] == '#')) or (i < (len(_b) - 1) and (_s[i+1] == '#')):
                    continue

                arr = _b[:i] + ('#' * len(_b)) + slots[i+len(_b):]
                L.append(arr)
        return L

    for run in sorted(runs, reverse=True):
        block = '#' * run
        ps = _placements(slots, block)
        print(run, block, ps)
        break
'''
??#??????#..????? [9, 2, 1]
##########..?????
'''



def count_arrangements(slots: str, runs: list[int]) -> int:
    print(slots, runs)
    try_arrangement(slots, runs)
    return 1

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        slots, runs = line.split()
        runs = [int(r) for r in runs.split(',')]
        result += count_arrangements(slots, runs)
        break

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
