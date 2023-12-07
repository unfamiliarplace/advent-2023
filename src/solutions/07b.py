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
        return any(cards.count(c) == 4 for c in s)

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
        return (len(s) == 3) and (sum(cards.count(c) == 2 for c in s) == 2)

    @staticmethod
    def is_1pair(cards: str) -> bool:
        s = set(cards)
        return (len(s) == 4) and (sum(cards.count(c) > 1 for c in s) == 1)

    @staticmethod
    def is_high(cards: str) -> bool:
        return len(set(cards)) == 5
    
    @staticmethod
    def get_joker_variants(cards: str) -> Iterable[str]:
        nonjokers = ''.join(c for c in cards if (c != 'J'))
        jokers = ''.join(c for c in cards if (c == 'J'))

        def _mutate(_cards: str) -> str:
            for s in Hand.STRENGTHS[1:]:    # not J
                if _cards[1:]:
                    for _rest in _mutate(_cards[1:]):
                        yield s + _rest
                else:
                    yield s
        
        for variant in _mutate(jokers):
            yield variant + nonjokers

    @staticmethod
    def jokerize(variants: list[str], checker: callable) -> bool:
        return any(checker(v) for v in variants)
    
    def get_type_rank(self: Hand) -> int:
        n_Js = self.cards.count('J')

        # short-circuiting...
        # 4 or 5 Js means 5 of a kind
        if n_Js > 3:
            return 7
        
        # 3 Js means 

        variants = list(Hand.get_joker_variants(self.cards))

        if Hand.jokerize(variants, Hand.is_5oak):
            return 7
        elif Hand.jokerize(variants, Hand.is_5oak):
            return 6
        elif Hand.jokerize(variants, Hand.is_4oak):
            return 5
        elif Hand.jokerize(variants, Hand.is_3oak):
            return 4
        elif Hand.jokerize(variants, Hand.is_2pair):
            return 3
        elif Hand.jokerize(variants, Hand.is_1pair):
            return 2
        elif Hand.jokerize(variants, Hand.is_high):
            return 1
        else:
            return 0

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
