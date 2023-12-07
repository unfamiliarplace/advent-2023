# https://adventofcode.com/2023/day/5

# Regular imports
from __future__ import annotations
from typing import Iterable
import re
import sys

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

    def __repr__(self: Rule) -> str:
        return f'({self.n:>10}) : {self.s}-{self.s_end} -> {self.d}-{self.d_end}'

def get_sorted_rules(rules: list[Rule]) -> list[Rule]:
    rules = sorted(rules, key=lambda r: r.s)

    last_upper = 0

    twixts = []
    for r in rules:
        twixt = Rule(last_upper, last_upper, r.s - last_upper)
        if twixt.n > 0:
            twixts.append(twixt)
        last_upper = r.s_end

    twixts.append(Rule(last_upper, last_upper, sys.maxsize))
    
    rules.extend(twixts)
    return sorted(rules, key=lambda r: r.s)

def parse(f) -> None:
    state = 0
    step = -1

    for line in stripped_lines(f):

        if state == 0:
            ranges = (int(m.group(1)) for m in re.finditer(RE_NUM, line))
            i = iter(ranges)
            for (start, stop) in zip(i, i):
                seed_ranges.append(range(start, start + stop))
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

def translate_src_to_dest(possible_src_ranges: list[range], rules: list[Rule]) -> list[range]:
    possible_dest_ranges = set()
    src_windows = rules_to_source_ranges(rules)
    dest_windows = rules_to_dest_ranges(rules)

    for possible in possible_src_ranges:
        for (src, dest) in zip(src_windows, dest_windows):
            overlap = get_range_overlap(possible, src)
            if overlap is None:
                continue

            offset_start = abs(src.start - overlap.start)
            offset_stop = abs(overlap.stop - src.stop)
            translated = range(dest.start + offset_start, dest.stop - offset_stop)
            possible_dest_ranges.add(translated)

    return sorted(possible_dest_ranges, key=lambda r: r.start)

def get_possible_location_ranges() -> list[range]:
    available = seed_ranges

    for step in steps:
        windows = rules_to_source_ranges(step)
        overlaps = get_all_overlaps(available, windows)
        available = translate_src_to_dest(overlaps, step)

    return available

# Logic

seed_ranges = []
steps = []
result = None

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    parse(f)
    dest_ranges = get_possible_location_ranges()
    result = dest_ranges[0].start

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
