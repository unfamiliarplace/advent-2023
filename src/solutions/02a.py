# https://adventofcode.com/2023/day/2

# My naming convention...
import os
import re
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Logic

limits = {
    'red': 12,
    'green': 13,
    'blue': 14
}

result = 0

RE_GAME = r'Game (\d+):'
RE_BALLS = r'(\d+) (green|blue|red)'

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    for line in filter(None, map(str.strip, f.readlines())):

        game = re.search(RE_GAME, line)[1]

        okay = True
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
            
            if not all(current[k] <= limits[k] for k in current):
                okay = False

        if okay:
            result += int(game)

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
