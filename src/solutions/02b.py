# https://adventofcode.com/2023/day/2

# My naming convention...
import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Regular imports
import re
import math

# Logic

minimums = []

RE_GAME = r'Game (\d+):'
RE_BALLS = r'(\d+) (green|blue|red)'

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    for line in filter(None, map(str.strip, f.readlines())):

        game = re.search(RE_GAME, line)[1]

        minimum = {
            'red': 0,
            'green': 0,
            'blue': 0
        }

        for subset in line.split(';'):

            current = {
                'red': 0,
                'green': 0,
                'blue': 0
            }

            for m in re.findall(RE_BALLS, subset):
                n = int(m[0])
                colour = m[1]
                current[colour] += n            

            for colour in current:
                if current[colour] > minimum[colour]:
                    minimum[colour] = current[colour]

        minimums.append(minimum.values())

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    result = sum(math.prod(L) for L in minimums)
    f.write(f'{result}')
