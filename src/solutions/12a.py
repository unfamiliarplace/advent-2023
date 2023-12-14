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

def max_discrete_blocks(s: str) -> int:
    can_start = False
    n = 0

    for c in s:
        if can_start:
            if c in '#?':
                n += 1
                can_start = False
        else:
            if c in '?.':
                can_start = True
    
    return n
            

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
        if '.' not in block:
            p = list(s)

            if i > 0:
                if p[i - 1] == '#':
                    continue
            
            if (i + n) < len(s):
                if p[i + n] == '#':
                    continue
                else:
                    p[i + n] = '.'

            p = ''.join(p[i+n:])
            placements.append(p)

    return placements

# TODO
# I suspect it being too high has to do with duplicate
# endpoints for the same starting point... not sure.
# Can't just use set the way I was doing because it
# eliminates same answers. Can I somehow both keep track
# of what's been done so far and also truncate?


def count_arrangements(slots: str, runs: list[int]) -> int:
    arrangements = [0]

    def _make_arrangements(_slots: str, _runs: list[int]) -> None:
        if not _runs:
            arrangements[0] += 1
        else:
            placements = get_placements(_slots, _runs[0])
            rest = _runs[1:]
            
            placements = filter(lambda p: max_discrete_blocks(p) >= len(rest), placements)
            placements = list(placements) # debugging

            for p in placements:
                _make_arrangements(p, rest)

    _make_arrangements(slots, runs)
    return arrangements[0]

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        slots, runs = line.split()
        runs = [int(r) for r in runs.split(',')]
        n_arrangements = count_arrangements(slots, runs)
        # print(f'{n_arrangements:>3} | {line}')
        # print()

        result += n_arrangements
        # break

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
