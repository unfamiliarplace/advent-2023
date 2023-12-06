# https://adventofcode.com/2023/day/5

# Regular imports
from typing import Iterable
import re
import math

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

class Way:
    pass

def get_sorted_rules(rules: list[tuple[int]]) -> list[tuple[int]]:
    rules = sorted(rules, key=lambda r: r[1])

    last_upper = 0

    twixts = []
    for (d, s, n) in rules:
        twixt = (last_upper, last_upper, s - last_upper)
        if twixt[2] != 0:
            twixts.append(twixt)
        last_upper = s + n
    
    twixts.append((last_upper, last_upper, math.inf))
    
    rules.extend(twixts)
    return sorted(rules, key=lambda r: r[0])

def parse(f) -> None:
    state = 0
    step = -1

    for line in stripped_lines(f):

        if state == 0:
            seed_ranges = (int(m.group(1)) for m in re.finditer(RE_NUM, line))
            i = iter(seed_ranges)
            seed_ranges = list(zip(i, i))
            state = 1
        
        elif state == 1:
            if 'map' in line:
                step += 1
                steps.append([])
            
            else:
                dest_start, src_start, length = (int(m.group(1)) for m in re.finditer(RE_NUM, line))
                steps[step].append((dest_start, src_start, length))
                
    for i in range(len(steps)):
        steps[i] = get_sorted_rules(steps[i])

    for step in steps[::-1]:
        back_steps.append(step)

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

def can_reach(dest_start: int, dest_end: int, ways: list[tuple[int]]) -> int:
    for (src_start, _, src_length) in ways:
        src_end = src_start + src_length - 1
        if (dest_start <= src_start <= dest_end) and (src_start <= dest_end <= src_end):
            return True
    return False

def next_rule(dest_start: int, dest_end: int, rules: list[tuple[int]]) -> tuple[int]:
    for rule in rules:
        src_start, _, src_length = rule
        src_end = src_start + src_length - 1
        if (dest_start <= src_start <= dest_end) and (src_start <= dest_end <= src_end):
            return rule
    return None


def get_lowest_possible_location_rule() -> tuple[int]:

    for (location, s, n) in back_steps[0]:
            print(location)
            path = []
            
            _d = location
            _s = s
            _n = n
            path.append((_d, _s, _n))

            # Which rule in the FIRST step would be used to get here?
            for step in back_steps[1:]:
                rule = next_rule(_s, _n, step)
                if rule:
                    print('yay')
                    _d, _s, _n = rule
                else:
                    break
                path.append((_d, _s, _n))

            print(path)             
            print()

            # Is there a seed that can go into that step?
            


# Logic

seed_ranges = []
steps = []
back_steps = steps[::-1]
location = None

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    parse(f)
    location = get_lowest_possible_location_rule()

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    result = 1 # TODO
    f.write(f'{result}')
