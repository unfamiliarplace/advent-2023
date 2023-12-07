# https://adventofcode.com/2023/day/7

# Regular imports

from __future__ import annotations
from typing import Iterable
from functools import total_ordering

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

# Helpers

@total_ordering
class Hand:
    """
    Note that Hand sorting will place better hands greater, so at the end.
    """
    STRENGTHS: str = 'AKQJT98765432'[::-1]
    cards: str
    bid: int

    def __init__(self: Hand, cards: str, bid: int) -> None:
        self.cards = cards
        self.bid = bid

    def is_5oak(self: Hand) -> bool:
        return len(set(self.cards)) == 1

    def is_4oak(self: Hand) -> bool:
        s = set(self.cards)
        return any(self.cards.count(c) == 4 for c in s)

    def is_full(self: Hand) -> bool:
        s = set(self.cards)
        return (len(s) == 2) and any(self.cards.count(c) == 3 for c in s)

    def is_3oak(self: Hand) -> bool:
        s = set(self.cards)
        return (len(s) == 3) and any(self.cards.count(c) == 3 for c in s)

    def is_2pair(self: Hand) -> bool:
        s = set(self.cards)
        return (len(s) == 3) and (sum(self.cards.count(c) == 2 for c in s) == 2)

    def is_1pair(self: Hand) -> bool:
        s = set(self.cards)
        return (len(s) == 4) and (sum(self.cards.count(c) > 1 for c in s) == 1)

    def is_high(self: Hand) -> bool:
        return len(set(self.cards)) == 5
    
    def get_type_rank(self: Hand) -> list[int]:
        checkers = [
            Hand.is_5oak,
            Hand.is_4oak,
            Hand.is_full,
            Hand.is_3oak,
            Hand.is_2pair,
            Hand.is_1pair,
            Hand.is_high
        ]
        return [int(c(self)) for c in checkers]
    
    def get_card_rank(self: Hand) -> list[int]:
        return [Hand.STRENGTHS.index(c) for c in self.cards]
    
    def get_cmp_factors (self: Hand) -> tuple[list[int]]:
        return (self.get_type_rank(), self.get_card_rank())
    
    def __eq__(self: Hand, other: object) -> bool:
        if not isinstance(other, Hand):
            return False
        
        return self.get_cmp_factors() == other.get_cmp_factors()
    
    def __lt__(self: Hand, other: Hand) -> bool:
        if not isinstance(other, Hand):
            raise TypeError(f"Cannot compare types: Hand and {type(other)}")
        
        return self.get_cmp_factors() < other.get_cmp_factors()
    
    def __repr__(self: Hand) -> str:
        return self.cards

# Logic

result: int = 0
hands: list[Hand] = []

with open(f'src/{INPUTS}/{N:0>2}.txt', 'r') as f:
    for line in stripped_lines(f):
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid)))
    
    hands.sort()
    
    for (i, hand) in enumerate(hands):
        result += (i + 1) * hand.bid

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
