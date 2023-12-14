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

def max_discrete_blocks(offset: int, s: str) -> int:
    can_start = False
    n = 0

    for c in s[offset:]:
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

def get_placements(offset: int, s: str, n: int) -> list[tuple[int, str]]:

    # short-circuiting
    start, end = get_start_and_end(s[offset:], n)
    if start == None:
        return []
    
    start, end = start + offset, end + offset
    
    placements = []

    for i in range(start, end):

        block = s[i:i + n]
        if '.' not in block:
            p = list(s)

            if i > 0:
                if p[i - 1] == '#':
                    continue
                else:
                    p[i - 1] = '.'
            
            if (i + n) < len(s):
                if p[i + n] == '#':
                    continue
                else:
                    p[i + n] = '.'

            p = ''.join(p[:i] + ['X' * n] + p[i+n:])
            placements.append((i + n, p))

    return placements

def count_arrangements(slots: str, runs: list[int]) -> tuple[set[str], int]:
    arrangements = set()

    def _make_arrangements(offset: int, _slots: str, _runs: list[int]) -> None:
        if not _runs:
            # Must have used all '#'
            if '#' not in _slots:
                arrangements.add(_slots)
        else:
            placements = get_placements(offset, _slots, _runs[0])
            rest = _runs[1:]
            
            placements = filter(lambda p: max_discrete_blocks(*p) >= len(rest), placements)
            placements = list(placements) # debugging

            for (o, p) in placements:
                _make_arrangements(o, p, rest)

    _make_arrangements(0, slots, runs)
    return arrangements, len(arrangements)

# Bruteforce version

def get_all_variants(slots: str) -> Iterable[str]:
    if '?' not in slots:
        yield slots
    else:
        i = slots.find('?')
        for v in get_all_variants(slots[i+1:]):
            yield slots[:i] + '.' + v
            yield slots[:i] + '#' + v

def is_valid(variant: str, runs: list[int]) -> bool:
    groups = list(filter(None, variant.split('.')))
    if len(groups) != len(runs):
        return False

    for (i, group) in enumerate(groups):
        if len(group) != runs[i]:
            return False
    return True

def bf_count_arrangements(slots: str, runs: list[int]) -> int:
    return sum(is_valid(v, runs) for v in get_all_variants(slots))

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        slots, runs = line.split()
        runs = [int(r) for r in runs.split(',')]

        n_arrangements = bf_count_arrangements(slots, runs)

        # arrangements, n_arrangements = count_arrangements(slots, runs)
        # print(f'{n_arrangements:>3} | {line}')
        # print()

        result += n_arrangements

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
