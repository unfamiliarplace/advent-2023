# https://adventofcode.com/2023/day/5

# Regular imports
from typing import Iterable
import re

# My naming convention...
import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Utilities

def stripped_lines(f) -> Iterable:
    return filter(None, map(str.strip, f.readlines()))

# Constants

RE_NUM = r'(\d+)'

# Helpers

def parse(f) -> None:
    state = 0
    step = -1

    for line in stripped_lines(f):

        if state == 0:
            for m in re.finditer(RE_NUM, line):
                seed = int(m.group(1))
                seed_to_location[seed] = None
            state = 1
        
        elif state == 1:
            if 'map' in line:
                step += 1
                steps.append([])
            
            else:
                dest_start, src_start, length = (int(m.group(1)) for m in re.finditer(RE_NUM, line))
                steps[step].append((dest_start, src_start, length))

def get_next(src: int, rules: list[tuple[int]]) -> int:
    for rule in rules:
        dest_start, src_start, length = rule
        if src_start <= src < (src_start + length):
            return dest_start + (src - src_start)
    return src

def get_location(seed: int) -> int:
    src = seed
    for step in steps:
        src = get_next(src, step)
    return src

# Logic

seed_to_location = {}
steps = []

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    parse(f)
    for seed in seed_to_location:
        seed_to_location[seed] = get_location(seed)

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    result = min(seed_to_location.values())
    f.write(f'{result}')
