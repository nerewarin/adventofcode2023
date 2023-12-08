"""
--- Day 7: Camel Cards ---
https://adventofcode.com/2023/day/7
"""
import math
from collections import Counter

from utils.test_and_run import run, test
from functools import reduce


# def print(*_):
#     pass

class CamelCards:
    def __init__(self, inp):
        self._inp = inp

    @classmethod
    def _parse_line(cls, line):
        raw_hand, bid = line.split()
        hand = [
            cls.get_card_power(card) for card in raw_hand
        ]
        return hand, int(bid)

    @staticmethod
    def get_card_power(card: str):
        cards = "AKQJT"
        if card in cards:
            value = 9 + len(cards) - cards.index(card)
        else:
            value = int(card)

        return value

    @staticmethod
    def get_hand_power(hand):
        c = Counter(hand)

        max_of_a_kind = max(c.values())
        kinds = len(c)

        combo = 0
        match kinds:
            case 1:
                # Five of a kind
                assert max_of_a_kind == 5
                combo = 70
            case 2:
                if max_of_a_kind == 4:
                    # Four of a kind
                    combo = 60
                else:
                    # Full house,
                    assert max_of_a_kind == 3
                    combo = 50

        if not combo:
            match max_of_a_kind:
                case 3:
                    # Three of a kind
                    assert kinds == 3
                    combo = 40
                case 2:
                    if kinds == 3:
                        # Two pair
                        combo = 30
                    else:
                        # One pair
                        assert kinds == 4
                        combo = 20

        if not combo:
            # High card
            assert kinds == 5
            # combo = max(hand)  # here's an error

        return combo

    def get_total_winnings(self):
        ranking = []
        rank2hand = {}
        for line in self._inp:
            hand, bid = self._parse_line(line)
            assert len(hand) == 5

            power = self.get_hand_power(hand)

            rank = tuple([power] + hand + [bid])
            ranking.append(
                rank
            )
            raw_hand = line.split()[0]
            rank2hand[rank] = raw_hand

        def custom_sort(item):
            return item[:-1]  # Exclude the last element for sorting

        sorted_data = sorted(ranking, key=custom_sort)

        # Raise an error if there are duplicates in the sorted result
        for i in range(len(sorted_data) - 1):
            if sorted_data[i][:-1] == sorted_data[i + 1][:-1]:
                raise ValueError("Duplicate entries found!")

        print(sorted_data)
        winnings = 0
        for i, hand_bid in enumerate(sorted_data):
            rank = i + 1
            bid = hand_bid[-1]
            winning = rank * bid
            hand = rank2hand[hand_bid]
            print(f"{hand=} bid={bid} * {rank=} = {winning}")
            winnings += winning
        return winnings


def canel_cards(inp, part=1):
    cards = CamelCards(inp)
    return cards.get_total_winnings()


def _parse_input_test():
    cards = "A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")
    for i, card in enumerate(cards):
        assert CamelCards.get_card_power(card.strip()) == len(cards) - cards.index(card) - 1 + 2


if __name__ == "__main__":
    _parse_input_test()
    assert canel_cards(["33332 1", "2AAAA 7"]) == 9
    assert canel_cards(["32222 1", "23333 7"]) == 9

    test(canel_cards, expected=6440)
    assert run(canel_cards) < 250703596
