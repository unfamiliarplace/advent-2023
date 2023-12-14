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

TESTING = True
INPUTS = 'inputs' if not TESTING else 'test_inputs'
OUTPUTS = 'outputs' if not TESTING else 'test_outputs'

# Utilities

def stripped_lines(f) -> Iterable[str]:
    return filter(None, map(str.strip, f.readlines()))

# Constants



# Helpers

def get_start_and_end(s: str, n: int) -> tuple[int]|None:
    """For short-circuiting."""
    start = None
    end = None

    s = s[:-(n-1)] if n > 1 else s # overall possible chunk

    for i in range(len(s)):
        if slots[i] in {'#', '?'}:
            start = i
            break
    else:
        return None, None
    
    for i in range(len(s), 0, -1):
        if s[i - 1] in {'#', '?'}:
            end = i
            break
    else:
        return None, None
    
    return start, end

def get_placements(s: str, n: int) -> list[str]:

    # short-circuiting
    start, end = get_start_and_end(s, n)
    if start == None:
        return []
    
    placements = []

    for i in range(start, end):

        block = s[i:i + n]
        if '.' not in block and 'X' not in block:
            arr = list(s)

            if i > 0:
                if arr[i - 1] in ('#', 'X'):
                    continue
                else:
                    arr[i - 1] = '.'
            
            if (i + n) < len(s):
                if arr[i + n] in ('#', 'X'):
                    continue
                else:
                    arr[i + n] = '.'

            arr = arr[:i] + ['X' * n] + arr[i+n:]
            placements.append(''.join(arr))

    return placements


def find_arrangements(slots: str, runs: list[int]) -> int:
    arrangements = set()

    def _make_arrangements(_slots: str, _runs: list[int]) -> None:
        if not _runs:
            arrangements.add(_slots.replace('?', '.'))
        else:
            placements = get_placements(_slots, _runs[0])
            rest = _runs[1:]
            
            for p in placements:
                _make_arrangements(p, rest)

    _make_arrangements(slots, runs)
    return arrangements, len(arrangements)

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        slots, runs = line.split()
        runs = [int(r) for r in runs.split(',')]
        arrangements, n_arrangements = find_arrangements(slots, runs)
        print(line, n_arrangements)
        print()

        result += n_arrangements
        # break

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
