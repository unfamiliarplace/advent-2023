# https://adventofcode.com/2023/day/8

# Regular imports

from __future__ import annotations
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

def next_keys(keys: Iterable[str], i: int) -> Iterable[str]:
    if instructions[i % len(instructions)] == 'L':
        for key in keys:
            yield rules[key].left
    else:
        for key in keys:
            yield rules[key].right

def get_start_keys() -> Iterable[str]:
    for key in rules:
        if key[2] == START:
            yield key

def n_stop_keys(keys: Iterable[str]) -> int:
    n = 0
    for key in keys:
        n += key[2] == STOP
    return n
            
def follow_sequence() -> int:
    i = 0
    keys = list(get_start_keys())
    n_keys = len(keys)
    while n_stop_keys(keys) != n_keys:
        keys = list(next_keys(keys, i))
        i += 1
    return i

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
