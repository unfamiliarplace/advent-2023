# https://adventofcode.com/2023/day/1

# My naming convention...
import os
fname = os.path.basename(__file__).strip('.py')
N = int(fname[:2])
S = fname[2]

# Logic

result = 0

d = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

with open(f'src/inputs/{N:0>2}.txt', 'r') as f:
    for line in filter(None, map(str.strip, f.readlines())):

        digits = ''.join(filter(lambda c: c.isdigit(), line))

        lowest_first = -1
        highest_last = len(line)

        if digits:
            first = digits[0]
            last = digits[-1]

            lowest_first = line.find(first)
            highest_last = line.rfind(last)

        for k in d:
            lowest_i = line.find(k)
            highest_i = line.rfind(k)
            if -1 < lowest_i < lowest_first:
                lowest_first = lowest_i
                first = d[k]
            if highest_i > highest_last:
                highest_last = highest_i
                last = d[k]

        plus = int(f'{first}{last}')
        result += plus

with open(f'src/outputs/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
