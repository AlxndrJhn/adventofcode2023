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


classifier = [
    lambda f: any(x == 5 for x in f.values()),
    lambda f: any(x == 4 for x in f.values()),
    lambda f: any(x == 3 for x in f.values()) and any(x == 2 for x in f.values()),
    lambda f: any(x == 3 for x in f.values()),
    lambda f: sum(x == 2 for x in f.values()) == 2,
    lambda f: any(x == 2 for x in f.values()),
]


def get_type(hand):
    frequencies = Counter(hand)

    for i, is_type in enumerate(classifier):
        if is_type(frequencies):
            return i
    return len(classifier)


hand_to_type = {}
hand_to_bid = {}
hands = []
for line in input_data:
    hand, bid_str = line.split(" ")
    hands.append(hand)
    bid = int(bid_str)
    hand_to_type[hand] = get_type(hand)
    hand_to_bid[hand] = bid


hand_length = len(hands[0])


def get_sorted_hands(index, hands):
    if len(hands) == 1:
        return hands
    sorted_hands = []
    for letter in top_to_lowest:
        if not hands:
            break
        with_this_letter = [hand for hand in hands if hand[index] == letter]
        if not with_this_letter:
            continue
        if len(with_this_letter) == 1:
            sorted_hands.append(with_this_letter[0])
            hands.remove(with_this_letter[0])
            continue
        elif len(with_this_letter) > 1:
            sorted_options = get_sorted_hands(index + 1, with_this_letter)
            sorted_hands.extend(sorted_options)
            hands = [hand for hand in hands if hand not in sorted_options]
            continue
    return sorted_hands


sorted_hands = []
for type_fo_sort in range(len(classifier) + 1):
    all_hands = [hand for hand in hands if hand_to_type[hand] == type_fo_sort]
    if not all_hands:
        continue
    sorted_hands_type = get_sorted_hands(0, all_hands)
    sorted_hands.extend(sorted_hands_type)

sum = 0
for i, hand in enumerate(sorted_hands):
    rank = len(sorted_hands) - i
    sum += hand_to_bid[hand] * rank
print(sum)
