# https://adventofcode.com/2023/day/00

# Regular imports

from __future__ import annotations
from typing import Iterable

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

def stripped_lines(f) -> Iterable[str]:
    return filter(None, map(str.strip, f.readlines()))

# Constants

SYMBOL_TO_DIRECTIONS = {
    '|' : ((0, -1), (0, 1)),
    '-' : ((-1, 0), (1, 0)),
    'L' : ((0, -1), (1, 0)),
    'J' : ((0, -1), (-1, 0)),
    '7' : ((0, 1), (-1, 0)),
    'F' : ((0, 1), (1, 0)),
    '.' : None,
    'S' : None,
}

DIRECTION_TO_SYMBOLS = {
    (0, -1): set('S|7F'),
    (0, 1): set('S|LJ'),
    (-1, 0): set('S-LF'),
    (1, 0): set('S-J7'),
}

# Helpers

class Space:
    symbol: str
    exits: list[Space]
    x: int
    y: int

    def __init__(self: Space, symbol: str, x: int, y: int) -> None:
        self.symbol = symbol
        self.x, self.y = x, y
        self.exits = []

    def add_exits(self: Space) -> None:
        possibles = SYMBOL_TO_DIRECTIONS[self.symbol]

        # TODO
        if possibles is None:
            return
        
        for (dx, dy) in possibles:
            nx, ny = self.x + dx, self.y + dy
            if (-1 < nx < len(grid[0])) and (-1 < ny < len(grid)):
                other = grid[ny][nx]
                if other.symbol in DIRECTION_TO_SYMBOLS[(dx, dy)]:
                    self.exits.append(other)

                    if other.symbol == 'S':
                        start_exits.append(self)

    def next_space(self: Space, prev: Space) -> Space:
        for space in self.exits:
            if space != prev:
                return space
            
    def __eq__ (self: Space, other: object) -> bool:
        if not isinstance(other, Space):
            return False
        
        return (self.x, self.y) == (other.x, other.y)
    
    def __repr__(self: Space) -> str:
        return self.symbol

def get_loop_length(start: Space) -> int:
    prev = start
    curr = start.exits[0]
    n = 1
    while curr != start:
        _ = curr
        curr = curr.next_space(prev)
        prev = _
        n += 1
    
    return n

# Logic

result = 0
grid: list[Space] = []
start_exits: list[Space] = []
start = None

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for (y, line) in enumerate(stripped_lines(f)):
        row = []
        for (x, c) in enumerate(line):
            row.append(Space(c, x, y))
        grid.append(row)

    start = None
    for line in grid:
        for space in line:
            if space.symbol == 'S':
                start = space
            else:
                space.add_exits()
    
    start.exits = start_exits

    result = get_loop_length(start) // 2
        

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
