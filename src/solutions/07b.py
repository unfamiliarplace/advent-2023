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

R_5OAK = 7
R_4OAK = 6
R_FULL = 5
R_3OAK = 4
R_2PAIR = 3
R_1PAIR = 2
R_HIGH = 1
R_NONE = 0

# Helpers

@total_ordering
class Hand:
    """
    Note that Hand sorting will place better hands greater, so at the end.
    """
    STRENGTHS: str = 'AKQT98765432J'[::-1]
    cards: str
    bid: int

    def __init__(self: Hand, cards: str, bid: int) -> None:
        self.cards = cards
        self.bid = bid

    @staticmethod
    def is_5oak(cards: str) -> bool:
        return len(set(cards)) == 1

    @staticmethod
    def is_4oak(cards: str) -> bool:
        s = set(cards)
        return (len(s) == 2) and any(cards.count(c) == 4 for c in s)

    @staticmethod
    def is_full(cards: str) -> bool:
        s = set(cards)
        return (len(s) == 2) and any(cards.count(c) == 3 for c in s)

    @staticmethod
    def is_3oak(cards: str) -> bool:
        s = set(cards)
        return (len(s) == 3) and any(cards.count(c) == 3 for c in s)

    @staticmethod
    def is_2pair(cards: str) -> bool:
        s = set(cards)
        return (len(s) == 3) and not any(cards.count(c) == 3 for c in s)

    @staticmethod
    def is_1pair(cards: str) -> bool:
        return len(set(cards)) == 4

    @staticmethod
    def is_high(cards: str) -> bool:
        return len(set(cards)) == 5
    
    @staticmethod
    def jokerize(cards: str) -> int|None:
        n_Js = cards.count('J')
        n_diff = len(set(cards))

        if n_Js > 3:
            return R_5OAK
        
        elif n_Js == 3:
            if n_diff == 2:
                return R_5OAK
            elif n_diff == 3:
                return R_4OAK
            
        elif n_Js == 2:
            if n_diff == 2:
                return R_5OAK
            elif n_diff == 3:
                return R_4OAK
            elif n_diff == 4:
                return R_FULL
            
        elif n_Js == 1:
            if n_diff == 2:
                return R_5OAK
            elif n_diff == 3:
                return R_4OAK
            elif n_diff == 4:
                return R_3OAK
            elif n_diff == 5:
                return R_1PAIR
        
        else:
            return None
    
    def get_type_rank(self: Hand) -> int:
        jokerized = Hand.jokerize(self.cards)
        if jokerized is not None:
            return jokerized

        if Hand.is_5oak(self.cards):
            return R_5OAK
        elif Hand.is_4oak(self.cards):
            return R_4OAK
        elif Hand.is_full(self.cards):
            return R_FULL
        elif Hand.is_3oak(self.cards):
            return R_3OAK
        elif Hand.is_2pair(self.cards):
            return R_2PAIR
        elif Hand.is_1pair(self.cards):
            return R_1PAIR
        elif Hand.is_high(self.cards):
            return R_HIGH

    def get_card_rank(self: Hand) -> list[int]:
        return [Hand.STRENGTHS.index(c) for c in self.cards]
    
    def get_cmp_factors (self: Hand) -> tuple[int, list[int]]:
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
        # if hand.cards.count('J') == 2:
        #     print(hand.get_type_rank())

        result += (i + 1) * hand.bid

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
