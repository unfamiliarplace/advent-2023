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

def get_placements(s: str, n: int) -> list[str]:
    placements = []

    for i in range(len(s) + 1 - n):

        block = s[i:i + n]
        if '.' not in block and '?' in block:
            arr = list(s)

            if i > 0:
                if arr[i - 1] == '#':
                    continue
                else:
                    arr[i - 1] = '.'
            
            if (i + n) < len(s):
                if arr[i + n] == '#':
                    continue
                else:
                    arr[i + n] = '.'

            arr = arr[:i] + ['#' * n] + arr[i+n:]
            placements.append(''.join(arr))

    return placements


def find_arrangements(slots: str, runs: list[int]) -> int:
    arrangements = set()

    def _make_arrangements(_slots: str, rest: list[int]) -> None:
        if not rest:
            arrangements.add(_slots.replace('?', '.'))
        else:
            for placed_slots in get_placements(_slots, rest[0]):

                # short-circuit
                if '?' in placed_slots:
                    _make_arrangements(placed_slots, rest[1:])

    _make_arrangements(slots, sorted(runs, reverse=True))
    return arrangements, len(arrangements)

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        slots, runs = line.split()
        runs = [int(r) for r in runs.split(',')]
        arrangements, n_arrangements = find_arrangements(slots, runs)
        print(line)
        print(arrangements, n_arrangements)
        print()

        result += n_arrangements
        break

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
