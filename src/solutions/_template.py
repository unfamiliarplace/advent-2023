# https://adventofcode.com/2022/day/1

# My naming convention...
import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Logic

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    pass

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    pass
