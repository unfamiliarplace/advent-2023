# https://adventofcode.com/2023/day/5

# Regular imports
from __future__ import annotations
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

class Rule:
    d: int
    s: int
    n: int
    d_end: int
    s_end: int

    def __init__(self: Rule, d: int, s: int, n: int) -> None:
        self.d, self.s, self.n = d, s, n
        self.d_end = self.d + n
        self.s_end = self.s + n

def get_sorted_rules(rules: list[Rule]) -> list[Rule]:
    rules = sorted(rules, key=lambda r: r.s)

    last_upper = 0

    twixts = []
    for r in rules:
        twixt = Rule(last_upper, last_upper, r.s - last_upper)
        if twixt.n > 0:
            twixts.append(twixt)
        last_upper = r.s_end
    
    rules.extend(twixts)
    return sorted(rules, key=lambda r: r.d)

def parse(f) -> None:
    state = 0
    step = -1

    for line in stripped_lines(f):

        if state == 0:
            ranges = (int(m.group(1)) for m in re.finditer(RE_NUM, line))
            i = iter(ranges)
            for (start, stop) in zip(i, i):
                seed_ranges.append(range(start, stop))
            state = 1
        
        elif state == 1:
            if 'map' in line:
                step += 1
                steps.append([])
            
            else:
                dest_start, src_start, length = (int(m.group(1)) for m in re.finditer(RE_NUM, line))
                steps[step].append(Rule(dest_start, src_start, length))
                
    for i in range(len(steps)):
        steps[i] = get_sorted_rules(steps[i])

def get_range_overlap(a: range, b: range) -> range:
    """
    a and b are ranges of (lower_bound, upper_bound)..
    Return the overlapping portion, if any.
    """
    lower = max((a.start, b.start))
    upper = min((a.stop, b.stop))

    if upper >= lower:
        return range(lower, upper)
    else:
        return None

def get_overlaps_for_range(one: range, others: list[range]):
    """
    Given a range one and a list of ranges others, return a list of portions
    of others that overlap with one.
    """
    overlaps = []
    for other in others:
        overlap = get_range_overlap(one, other)
        if overlap is not None:
            overlaps.append(overlap)

    return overlaps

def get_all_overlaps(ones: list[range], others: list[range]) -> list[range]:
    """
    Given a list of ranges ones and another list of ranges others, return a list
    of portions of others that overlap with any portions of ones.
    """
    overlaps = []
    for one in ones:
        some = get_overlaps_for_range(one, others)
        overlaps.extend(some)
    return overlaps

def rules_to_source_ranges(rules: list[Rule]) -> list[range]:
    ranges = []
    for r in rules:
        ranges.append(range(r.s, r.s_end))
    return ranges

def rules_to_dest_ranges(rules: list[Rule]) -> list[range]:
    ranges = []
    for r in rules:
        ranges.append(range(r.d, r.d_end))
    return ranges

def translate_src_to_dest(src_ranges: list[range], rules: list[Rule]) -> list[range]:
    pass

def get_lowest_possible_location_rule() -> tuple[int]:

    these = seed_ranges
    others = rules_to_source_ranges(steps[0])
    first_round = get_all_overlaps(these, others)

    print(first_round)

    return 'hi'

# Logic

seed_ranges = []
steps = []
location = None

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    parse(f)
    location = get_lowest_possible_location_rule()

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    result = 1 # TODO
    f.write(f'{result}')
