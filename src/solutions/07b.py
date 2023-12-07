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
        
        if not jokers:
            yield cards
        else:
            for variant in _mutate(jokers):
                yield variant + nonjokers

    @staticmethod
    def jokerize(variants: list[str], checker: callable) -> bool:
        return any(checker(v) for v in variants)

    @staticmethod
    def short_circuit(cards: str) -> int|None:
        n_Js = cards.count('J')
        n_diff = len(set(cards))

        if n_Js > 3:
            return R_5OAK
        
        elif n_Js == 3:
            if n_diff == 2:
                return R_5OAK
            elif n_diff == 3:
                return R_4OAK
    
    def get_type_rank(self: Hand) -> int:
        sc = Hand.short_circuit(self.cards)
        if sc is not None:
            return sc

        variants = list(Hand.get_joker_variants(self.cards))

        if Hand.jokerize(variants, Hand.is_5oak):
            return R_5OAK
        elif Hand.jokerize(variants, Hand.is_4oak):
            return R_4OAK
        elif Hand.jokerize(variants, Hand.is_full):
            return R_FULL
        elif Hand.jokerize(variants, Hand.is_3oak):
            return R_3OAK
        elif Hand.jokerize(variants, Hand.is_2pair):
            return R_2PAIR
        elif Hand.jokerize(variants, Hand.is_1pair):
            return R_1PAIR
        elif Hand.jokerize(variants, Hand.is_high):
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
        result += (i + 1) * hand.bid

with open(f'src/{OUTPUTS}/{N:0>2}{S}.txt', 'w') as f:
    f.write(f'{result}')
