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

def max_discrete_blocks(offset: int, s: str) -> int:
    """
    Return the maximum number of discrete blocks that could be formed
    in the given string starting at the given offset.

    '?' and '#' can be part of a block
    '?' and '.' can separate blocks
    """
    can_start = False
    n = 0

    for c in s[offset:]:
        if can_start:
            if c in '#?':
                n += 1
                can_start = False
        else:
            if c in '.?':
                can_start = True
    
    return n

def get_start_and_end(s: str, n: int) -> tuple[int|None]:
    """
    For short-circuiting. Find the first and last positions
    where it would make sense to start searching.
    """

    # Reduce the scope to the last place that has a chunk large enough
    # to hold a block of size n
    s = s[:-(n-1)] if n > 1 else s

    # Start = first instance of '#' or '?'
    for i in range(len(s)):
        if s[i] in {'#', '?'}:
            start = i
            break
    else:
        return None, None
    
    # End = last instance of '#' or '?'
    for i in range(len(s), 0, -1):
        if s[i - 1] in {'#', '?'}:
            end = i
            break
    else:
        return None, None
    
    return start, end

def get_placements(offset: int, s: str, n: int) -> Iterable[tuple[int, str]]:
    """
    Given a string of slots, a block of size n, and an offset to start looking,
    yield tuples of the form (i, placed) where placed is a valid placement
    of the block in s and i is the new offset following said block.
    """

    # Narrow the scope
    start, end = get_start_and_end(s[offset:], n)
    if start == None:
        return
    
    # Correct offset (above function only considered s[offset:])
    start, end = start + offset, end + offset

    # Check each valid chunk start location
    for i in range(start, end):

        chunk = s[i:i + n]
        if '.' not in chunk:
            p = list(s)

            # Ensure this chunk wasn't preceded or followed by '#',
            # which would make it longer than intended.
            # If valid, force a separation from the following block.

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

            # Place chunk (eliminating future uses of it) and yield
            p = ''.join(p[:i] + ['X' * n] + p[i+n:])
            yield (i + n, p)

            # Short-circuit
            # If the block was entirely '#' it was the only possible placement
            if chunk == ('#' * 9):
                break

def count_arrangements(slots: str, runs: list[int]) -> int:
    """
    Return the number of possible arrangements for the given slots and runs.
    Uses an efficient algorithm.
    """
    n_arrangements = [0]

    def _make_arrangements(offset: int, _slots: str, _runs: list[int]) -> None:

        # Base case: no more runs to check
        if not _runs:
            # Must have used all '#'
            if '#' not in _slots:
                n_arrangements[0] += 1

        else:
            # Get all possible placements of the next run
            placements = get_placements(offset, _slots, _runs[0])
            rest = _runs[1:]
            
            # Filter: enough possible blocks left for remaining runs?
            placements = filter(lambda p: max_discrete_blocks(*p) >= len(rest), placements)

            # Try each placement with remaining runs
            for (updated_offset, p) in placements:
                _make_arrangements(updated_offset, p, rest)

    _make_arrangements(0, slots, runs)
    return n_arrangements[0]

# Bruteforce version

def get_all_variants(slots: str) -> Iterable[str]:
    """
    Yield all possible variants for the given string of slots.
    The number of variants is 2**n where n is the number of '?'
    """

    if '?' not in slots:
        yield slots
    else:
        i = slots.find('?')
        for v in get_all_variants(slots[i+1:]):
            yield slots[:i] + '.' + v
            yield slots[:i] + '#' + v

def is_valid(variant: str, runs: list[int]) -> bool:
    """
    Return True iff the given variant matches the given list of runs.
    """
    groups = list(filter(None, variant.split('.')))
    if len(groups) != len(runs):
        return False

    for (i, group) in enumerate(groups):
        if len(group) != runs[i]:
            return False
        
    return True

def bf_count_arrangements(slots: str, runs: list[int]) -> int:
    """
    Return the number of possible arrangements for the given slots and runs.
    Uses an inefficient algorithm: creates every possible variant and tallies
    the valid ones.
    """
    n = 0

    for v in get_all_variants(slots):
        if is_valid(v, runs):
            n += 1

    return n

# Logic

result = 0

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    i = 0
    for line in stripped_lines(f):
        slots, runs = line.split()
        runs = [int(r) for r in runs.split(',')]

        # TODO Need a different approach.
        # Fail fast will never be enough;
        # some lines have hundreds of thousands of variations.

        slots = '?'.join([slots] * 5)
        runs *= 5

        n_arrangements = count_arrangements(slots, runs)
        result += n_arrangements

        print(i, n_arrangements)
        i += 1

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
