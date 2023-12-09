from collections import Counter, defaultdict
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}/input.txt", "r").read().split("\n")

# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# High card, where all cards' labels are distinct: 23456


top_to_lowest = "AKQJT98765432"


def value_of_card(card):
    return (len(top_to_lowest) - top_to_lowest.index(card)) / len(top_to_lowest)


def get_strength(hand):
    frequencies = Counter(hand)

    detectors = [
        any(x == 5 for x in frequencies.values()),
        any(x == 4 for x in frequencies.values()),
        any(x == 3 for x in frequencies.values())
        and any(x == 2 for x in frequencies.values()),
        any(x == 3 for x in frequencies.values()),
        sum(x == 2 for x in frequencies.values()) == 2,
        any(x == 2 for x in frequencies.values()),
    ]
    unique_leftover = set(hand)
    adjustments = []
    if any(x == 5 for x in frequencies.values()):
        card = next(card for card, freq in frequencies.items() if freq == 5)
        unique_leftover.remove(card)
        adjustment = value_of_card(card)
    else:
        adjustment = 0
    adjustments.append(adjustment)

    if any(x == 4 for x in frequencies.values()):
        card = next(card for card, freq in frequencies.items() if freq == 4)
        unique_leftover.remove(card)
        adjustment = value_of_card(card)
    else:
        adjustment = 0
    adjustments.append(adjustment)

    if any(x == 3 for x in frequencies.values()) and any(
        x == 2 for x in frequencies.values()
    ):
        card1 = next(card for card, freq in frequencies.items() if freq == 3)
        card2 = next(card for card, freq in frequencies.items() if freq == 2)
        unique_leftover = unique_leftover - set(card1)
        unique_leftover.remove(card2)
        adjustment = (value_of_card(card1) * 10 + value_of_card(card2)) / 11
    else:
        adjustment = 0
    adjustments.append(adjustment)

    if any(x == 3 for x in frequencies.values()):
        card1 = next(card for card, freq in frequencies.items() if freq == 3)
        unique_leftover = unique_leftover - set(card1)
        adjustment = value_of_card(card1)
    else:
        adjustment = 0
    adjustments.append(adjustment)

    if sum(x == 2 for x in frequencies.values()) == 2:
        cards = [card for card, freq in frequencies.items() if freq == 2]
        cards_sorted = sorted(cards, key=lambda card: value_of_card(card), reverse=True)
        for card in cards_sorted:
            unique_leftover = unique_leftover - set(card)
        adjustment = (
            value_of_card(cards_sorted[0]) * 10 + value_of_card(cards_sorted[1])
        ) / 11
    else:
        adjustment = 0
    adjustments.append(adjustment)

    if any(x == 2 for x in frequencies.values()):
        card2 = next(card for card, freq in frequencies.items() if freq == 2)
        adjustment = value_of_card(card2)
    else:
        adjustment = 0
    adjustments.append(adjustment)

    score = 0
    for i, card in enumerate(top_to_lowest):
        ten_power = 10 ** (len(top_to_lowest) - i)
        score += ten_power * (card in unique_leftover)
    score = score / 10 ** len(top_to_lowest)
    adjustments.append(score)

    adjustment = 0
    for i, adj in enumerate(adjustments):
        weighted = adj * pow(10, len(adjustments) - i)
        adjustment += weighted

    for i, detector in enumerate(detectors):
        if detector:
            return (len(detectors) - i) * 100 + adjustment

    return score


hand_to_strength = {}
hand_to_bid = {}
hands = set()
for line in input_data:
    hand, bid_str = line.split(" ")
    sorted_hand = "".join(sorted(hand))
    assert sorted_hand not in hands
    hands.add(sorted_hand)
    bid = int(bid_str)
    strength = get_strength(hand)
    hand_to_strength[hand] = strength
    hand_to_bid[hand] = bid

sorted_by_strength = sorted(
    hand_to_strength.items(), key=lambda item: item[1], reverse=True
)
sum = 0
for i, (hand, strength) in enumerate(sorted_by_strength):
    sum += hand_to_bid[hand] * (len(sorted_by_strength) - i - 1)
print(sum)
