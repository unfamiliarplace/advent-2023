# https://adventofcode.com/2023/day/4

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

RE_CARD = r'Card +(\d+)'

# Helpers



# Logic

result = 0
copies = {}

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        card, line = line.split(':')
        this_card_n = int(re.findall(RE_CARD, card)[0])

        if this_card_n not in copies:
            copies[this_card_n] = 1

        for _ in range(copies[this_card_n]):
            winning, having = line.split('|')
            winning = set(int(n) for n in winning.strip().split())
            having = set(int(n) for n in having.strip().split())

            both = having.intersection(winning)
            
            # Add new cards
            for i in range(len(both)):
                next_card_n = this_card_n + i + 1
                copies[next_card_n] = copies.get(next_card_n, 1) + 1
            
            # Tally number of cards done
            result += 1

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
