# https://adventofcode.com/2023/day/00

# Regular imports

from __future__ import annotations
from typing import Iterable
from termcolor import cprint

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
    x: int
    y: int
    exits: set[Space]
    in_loop: bool
    searched_path_to_exit: bool
    has_path_to_exit: bool
    expanded_only: bool

    def __init__(self: Space, symbol: str, x: int, y: int, expanded_only: bool=False) -> None:

        self.symbol = symbol
        self.x, self.y = x, y
        self.exits = set()

        self.in_loop = self.symbol == 'S'
        self.searched_path_to_exit = False
        self.has_path_to_exit = False
        self.expanded_only = expanded_only

    def add_exits(self: Space) -> None:
        possibles = SYMBOL_TO_DIRECTIONS[self.symbol]

        # TODO
        if possibles is None:
            return
        
        for (dx, dy) in possibles:
            other = self.space_from(dx, dy)
            if other:
                if other.symbol in DIRECTION_TO_SYMBOLS[(dx, dy)]:
                    self.exits.add(other)

                    if other.symbol == 'S':
                        start_exits.add(self)

    def space_from(self: Space, dx: int, dy: int) -> Space|None:
        nx, ny = self.x + dx, self.y + dy
        if (-1 < nx < len(grid[0])) and (-1 < ny < len(grid)):
            return grid[ny][nx]

    def next_space(self: Space, prev: Space) -> Space:
        for space in self.exits:
            if space != prev:
                return space
            
    def add_to_loop(self: Space) -> None:
        self.in_loop = True

    def surrounding(self: Space, exclusions: set[Space]=set()) -> set[Space]:
        surr = set()
        for (dx, dy) in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            other = self.space_from(dx, dy)
            if (other is not None) and (other not in exclusions):
                surr.add(other)
        
        return surr

    def search_path_to_exit(self: Space, exclusions: set[Space]=set()) -> bool:
        if not self.searched_path_to_exit:
            self.has_path_to_exit = self._search_path_to_exit(exclusions)
            self.searched_path_to_exit = True
        
        return self.has_path_to_exit

    def _search_path_to_exit(self: Space, exclusions: set[Space]=set()) -> bool:
        
        # Loop can't be an exit
        if self.in_loop:
            return False
            
        # If not surrounded by 4 cardinals, we're on an edge
        if (0 in (self.x, self.y)) or ((len(grid) - 1) in (self.x, self.y)):
            return True
        
        # Can our surrounding ones lead to exits?
        exclusions = exclusions.union({self})

        # if any([adjacent.search_path_to_exit(exclusions) for adjacent in self.surrounding(exclusions)]):
        #     return True
        
        for adjacent in self.surrounding(exclusions):
            if adjacent.search_path_to_exit(exclusions):
                return True
                    
        # No way out
        return False

    def is_enclosed_in_main_loop(self: Space) -> bool:
        if self.in_loop:
            return False
        
        if self.expanded_only:
            return False

        if self.search_path_to_exit():
            return False
        
        return True
    
    def connected(self: Space, other: Space) -> bool:
        return self in other.exits
    
    def __hash__(self: Space) -> int:
        return hash((self.expanded_only, self.x, self.y))
            
    def __eq__ (self: Space, other: object) -> bool:
        if not isinstance(other, Space):
            return False
        
        return (self.x, self.y) == (other.x, other.y)
    
    def __repr__(self: Space) -> str:
        return self.symbol

def expand_grid() -> list[list[Space]]:

    def _create_link(prev: Space, curr: Space, connector: str) -> Space:
        if prev.connected(curr):
            insert = Space(connector, i_col, i_row, True)

            if prev.in_loop and curr.in_loop:
                insert.add_to_loop()

            prev.exits.remove(curr)
            curr.exits.remove(prev)
            prev.exits.add(insert)
            curr.exits.add(insert)
            insert.exits.add(prev)
            insert.exits.add(curr)

        else:
            insert = Space('.', i_col, i_row, True)
        
        return insert

    # Expand horizontally
    expanded = []
    for (i_row, row) in enumerate(grid):
        expanded_row = []

        for (i_col, space) in enumerate(row[1:]):  
            prev, curr = row[i_col], space
            expanded_row.append(prev)
            expanded_row.append(_create_link(prev, curr, '-'))

        expanded_row.append(curr)
        expanded.append(expanded_row)

    # Expand vertically
    expanded2 = [expanded[0]]
    for (i_row, row) in enumerate(expanded[1:]):
        brand_new_row = []

        for (i_col, space) in enumerate(row):  
            prev, curr = expanded[i_row][i_col], space
            brand_new_row.append(_create_link(prev, curr, '|'))
        
        expanded2.append(brand_new_row)
        expanded2.append(row)
    
    # ... Update all x, y :')
    for y in range(len(expanded2)):
        for x in range(len(expanded2[0])):
            s = expanded2[y][x]
            s.x, s.y = x, y

    grid[:] = expanded2

def traverse_loop(start: Space) -> int:
    """Returns the length of the loop, with S counted twice."""
    prev = start
    curr = list(start.exits)[0] # Arbitrary
    n = 1
    while curr != start:
        curr.add_to_loop()
        _ = curr
        curr = curr.next_space(prev)
        prev = _
        n += 1
    
    return n

def count_enclosed() -> int:
    n = 0
    rows = 0
    for row in grid:
        for space in row:
            n += space.is_enclosed_in_main_loop()
        
        rows += 1
        if rows > 2:
            break
    return n

def print_enclosure(_grid: list[list[Space]]) -> None:
    rows = 0

    for line in _grid:
        for cell in line:
            if cell.is_enclosed_in_main_loop():
                cprint(' ', 'red', 'on_red', end='')
            elif cell.in_loop:
                cprint(cell, 'dark_grey', end='')
            elif cell.search_path_to_exit():
                cprint(' ', 'green', 'on_green', end='')
            elif cell.expanded_only:
                cprint(' ', 'dark_grey', 'on_dark_grey', end='')
        print()

        rows += 1
        if rows > 2:
            break

# Logic

result = 0
grid: list[list[Space]] = []
start_exits: set[Space] = set()

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
    traverse_loop(start) # Required to update in_loop
    old_grid = list(row[:] for row in grid)
    expand_grid()

    result = count_enclosed()
    print(result)

    print_enclosure(old_grid)
    print()
    print_enclosure(grid)
    
with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
