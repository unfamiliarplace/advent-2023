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

RE_RULE = r'(\w{3}) = \((\w{3}), (\w{3})\)'
START = 'AAA'
STOP = 'ZZZ'

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


def follow_sequence() -> int:
    i = 0
    key = START
    while key != STOP:
        key = next_key(key, i)
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
