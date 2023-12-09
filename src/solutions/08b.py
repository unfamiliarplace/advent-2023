# https://adventofcode.com/2023/day/8

# Regular imports

from __future__ import annotations
from typing import Iterable
import re
import math
import itertools

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

RE_RULE = r'(.{3}) = \((.{3}), (.{3})\)'
START = 'A'
STOP = 'Z'

# Helpers

class Rule:
    key: str
    left: str
    right: str

    def __init__(self: Rule, key: str, left: str, right: str) -> None:
        self.key, self.left, self.right = key, left, right

def parse_rules(lines: Iterable[str]) -> None:
    for line in lines:
        r = Rule(*re.match(RE_RULE, line).groups())
        rules[r.key] = r

def next_key(key: str, i: int) -> str:
    if instructions[i % len(instructions)] == 'L':
        return rules[key].left
    else:
       return rules[key].right

def get_start_keys() -> list[str]:
    return list(filter(lambda k: k[2] == START, rules.keys()))

def get_stops(key: str) -> set[int]:
    """
    Return a set of indices (number of steps) on which the given start key
    would land on a stop key.    
    """

    stops = set()
    i = 0
    last_n = 0

    # Search exhaustively without risking an infinite loop.
    # A loop is defined as arriving at the same key at the same
    # position in the instruction list (because then you would
    # repeat steps already carried out and end up here again).
    seen = set()
    seen.add((key, i % len(instructions)))

    while len(seen) > last_n:
        last_n = len(seen)
        
        key = next_key(key, i)
        i += 1

        seen.add((key, i % len(instructions)))

        # Simultaneously keep track of stop key indices
        if key[2] == STOP:
            stops.add(i)

    return stops

def follow_sequence() -> int:
    """
    Return the minimum number of steps required for all start keys
    to simultaneously be on a stop key.
    """

    # For each start key, find its set of stop indices
    sets_of_stops = []
    for key in get_start_keys():
        sets_of_stops.append((get_stops(key)))
    
    # Find all combinations of stop indices across all keys.
    # Each of these combinations would be a possible time they
    # can all be on a stop key.
    lcms = set(math.lcm(*p) for p in itertools.product(*sets_of_stops))

    # The least common multiple is the first such time!
    return min(lcms)

# Logic

instructions = ''
rules: dict[str, Rule] = {}

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    instructions = f.readline().strip()
    f.readline()
    parse_rules(stripped_lines(f))

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    result = follow_sequence()
    f.write(f'{result}')
