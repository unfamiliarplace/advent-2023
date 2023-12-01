# https://adventofcode.com/2023/day/1

# My naming convention...
import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Logic

result = 0

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    for line in filter(None, map(str.strip, f.readlines())):
        digits = ''.join(filter(lambda c: c.isdigit(), line))

        first = digits[0]
        last = digits[-1]

        result += int(f'{first}{last}')

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
