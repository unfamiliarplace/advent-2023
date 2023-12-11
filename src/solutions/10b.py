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
    'F' : ((0, 1), (1, 0))
}

DIRECTION_TO_SYMBOLS = {
    (0, -1): set('S|7F'),
    (0, 1): set('S|LJ'),
    (-1, 0): set('S-LF'),
    (1, 0): set('S-J7'),
}

# Helpers

class App:
    grid: list[list[Space]]
    original_grid: list[list[Space]]
    current_path: set[Space]
    known_edges: set[Space]
    known_blocks: set[Space]

    def __init__(self: App) -> None:
        self.grid = []
        self.original_grid = []
        self.current_path = set()
        self.known_edges = set()
        self.known_blocks = set()

class Space:
    next_id: int=0
    id: int
    symbol: str
    x: int
    y: int
    exits: set[Space]
    in_loop: bool
    expanded_only: bool
    searched_path_to_exit: bool
    has_path_to_exit: bool
    checked_enclosure: bool
    is_enclosed: bool

    def __init__(self: Space, symbol: str, x: int, y: int) -> None:
        self.id = Space.next_id
        Space.next_id += 1

        self.symbol = symbol
        self.x, self.y = x, y
        self.exits = set()

        self.in_loop = False
        self.expanded_only = False

        self.searched_path_to_exit = False
        self.has_path_to_exit = False

        self.checked_enclosure = False
        self.is_enclosed = False

    def add_exits(self: Space) -> None:
        possibles = SYMBOL_TO_DIRECTIONS.get(self.symbol)

        if possibles is None:
            return
        
        for (dx, dy) in possibles:
            other = self.space_from(dx, dy)
            if other:
                if other.symbol in DIRECTION_TO_SYMBOLS[(dx, dy)]:
                    self.exits.add(other)

                    if other.symbol == 'S':
                        start_exits.add(self)

    def next_exit(self: Space, prev: Space) -> Space:
        for space in self.exits:
            if space != prev:
                return space

    def space_from(self: Space, dx: int, dy: int) -> Space|None:
        nx, ny = self.x + dx, self.y + dy
        if (-1 < nx < len(app.grid[0])) and (-1 < ny < len(app.grid)):
            return app.grid[ny][nx]

    def surrounding(self: Space) -> set[Space]:
        surr = set()
        for (dx, dy) in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            other = self.space_from(dx, dy)

            if (other is not None) and (other not in app.current_path) and (other not in app.known_blocks):
                surr.add(other)
        
        return surr
    
    def on_edge(self: Space) -> bool:
        return any((
            self.x == 0,
            self.y == 0,
            self.x == (len(app.grid[0]) - 1),
            self.y == (len(app.grid) - 1)
        ))
    
    def search_path_to_exit(self: Space, heading: tuple[int]=None) -> bool:
        if not self.searched_path_to_exit:

            self.has_path_to_exit = self._search_path_to_exit(heading)
            self.searched_path_to_exit = True

            if self.has_path_to_exit:
                for space in app.current_path:
                    space.has_path_to_exit = True
                    space.searched_path_to_exit = True
                    app.known_edges.add(space)
                    app.current_path = set()
            else:
                app.known_blocks.add(self)
            
            # print()
        
        return self.has_path_to_exit
    
    def _search_path_to_exit(self: Space, heading: tuple[int]=None) -> bool:
        
        # Loop can't be an exit
        if self.in_loop:
            return False
            
        # If not surrounded by 4 cardinals, we're on an edge
        if self.on_edge():
            return True
        
        # Can our surrounding ones lead to exits? 
        app.current_path.add(self)
        eligible = self.surrounding()

        if eligible.intersection(app.known_edges):
            return True
        
        eligible = sorted(eligible, key=lambda s: (s.x - self.x, s.y - self.y) == heading, reverse=True)
        
        for adj in eligible:
            new_heading = (adj.x - self.x, adj.y - self.y)
            if adj.search_path_to_exit(new_heading):
                return True
                    
        # No way out
        return False
    
    def is_enclosed_in_main_loop(self: Space) -> bool:
        if not self.checked_enclosure:
            app.current_path = set()
            self.is_enclosed = self._is_enclosed_in_main_loop()
            self.checked_enclosure = True
        
        return self.is_enclosed

    def _is_enclosed_in_main_loop(self: Space) -> bool:
        if self.expanded_only:
            return False
        
        if self.in_loop:
            return False
        
        if self.on_edge():
            return False

        if self.search_path_to_exit():
            return False
        
        return True
    
    def connected(self: Space, other: Space) -> bool:
        return self in other.exits
    
    def __hash__(self: Space) -> int:
        return hash(self.id)
            
    def __eq__ (self: Space, other: object) -> bool:
        if not isinstance(other, Space):
            return False
        
        return self.id == other.id
    
    def __str__(self: Space) -> str:
        return self.symbol
    
    def __repr__(self: Space) -> str:
        s = f'{self.id:>3}: {self.symbol} ([{self.y}][{self.x}])'
        if self.expanded_only:
            s += ' [e]'
        else:
            s += '    '
        return s

def expand_grid() -> list[list[Space]]:

    def _create_link(prev: Space, curr: Space, connector: str) -> Space:
        if prev.connected(curr):
            insert = Space(connector, i_col, i_row)
            insert.in_loop = prev.in_loop

            prev.exits.remove(curr)
            curr.exits.remove(prev)

            prev.exits.add(insert)
            curr.exits.add(insert)

            insert.exits.add(prev)
            insert.exits.add(curr)

        else:
            insert = Space('.', i_col, i_row)
        
        insert.expanded_only = True
        return insert

    # Expand horizontally
    expanded = []
    for (i_row, row) in enumerate(app.grid):
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

    return expanded2

def traverse_loop(start: Space) -> int:
    """Returns the length of the loop, with S counted twice."""
    prev = start
    curr = list(start.exits)[0] # Arbitrary
    n = 1
    while curr != start:
        curr.in_loop = True
        _ = curr
        curr = curr.next_exit(prev)
        prev = _
        n += 1
    
    return n

def count_enclosed() -> int:
    n = 0
    for row in app.grid:
        for space in row:
            n += space.is_enclosed_in_main_loop()
    return n

def print_enclosure(_grid: list[list[Space]]) -> None:
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

# Logic

app = App()
result = 0
start_exits: set[Space] = set()
start: Space

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for (y, line) in enumerate(stripped_lines(f)):
        row = []
        for (x, c) in enumerate(line):
            row.append(Space(c, x, y))
        app.grid.append(row)

    start = None
    for line in app.grid:
        for space in line:
            if space.symbol == 'S':
                start = space
                start.in_loop = True
            else:
                space.add_exits()
    
    start.exits = start_exits
    traverse_loop(start) # Required to update in_loop
    app.original_grid = [row[:] for row in app.grid]
    app.grid = expand_grid()

    result = count_enclosed()
    # print(result)

    # print_enclosure(app.original_grid)
    # print()
    # print_enclosure(app.grid)
    
with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
