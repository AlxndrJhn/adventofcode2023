from collections import Counter, defaultdict
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}/input.txt", "r").read().split("\n")


top_to_lowest = "AKQJT98765432"


def value_of_card(card):
    assert card in top_to_lowest
    return (len(top_to_lowest) - top_to_lowest.index(card)) / len(top_to_lowest)


def get_strength(hand):
    leftover = hand
    all_scores = []
    power = 6
    score = 0
    if any(x == 5 for x in Counter(leftover).values()):
        card = next(card for card, freq in Counter(leftover).items() if freq == 5)
        leftover = leftover.replace(card, "")
        score = value_of_card(card)
    else:
        score = 0
    weighted_score = score * pow(10, power)
    power -= 1
    all_scores.append(weighted_score)

    if any(x == 4 for x in Counter(leftover).values()):
        card = next(card for card, freq in Counter(leftover).items() if freq == 4)
        leftover = leftover.replace(card, "")
        score = value_of_card(card)
    else:
        score = 0
    weighted_score = score * pow(10, power)
    power -= 1
    all_scores.append(weighted_score)

    if any(x == 3 for x in Counter(leftover).values()) and any(
        x == 2 for x in Counter(leftover).values()
    ):
        card1 = next(card for card, freq in Counter(leftover).items() if freq == 3)
        card2 = next(card for card, freq in Counter(leftover).items() if freq == 2)
        leftover = leftover.replace(card1, "").replace(card2, "")
        score = (value_of_card(card1) * 10 + value_of_card(card2)) / 11
    else:
        score = 0
    weighted_score = score * pow(10, power)
    power -= 1
    all_scores.append(weighted_score)

    if any(x == 3 for x in Counter(leftover).values()):
        card1 = next(card for card, freq in Counter(leftover).items() if freq == 3)
        leftover = leftover.replace(card1, "")
        score = value_of_card(card1)
    else:
        score = 0
    weighted_score = score * pow(10, power)
    power -= 1
    all_scores.append(weighted_score)

    if sum(x == 2 for x in Counter(leftover).values()) == 2:
        cards = [card for card, freq in Counter(leftover).items() if freq == 2]
        cards_sorted = sorted(cards, key=lambda card: value_of_card(card), reverse=True)
        score = (
            value_of_card(cards_sorted[0]) * 10 + value_of_card(cards_sorted[1])
        ) / 11
        leftover = leftover.replace(cards_sorted[0], "").replace(cards_sorted[1], "")
    else:
        score = 0
    weighted_score = score * pow(10, power)
    power -= 1
    all_scores.append(weighted_score)

    if any(x == 2 for x in Counter(leftover).values()):
        card2 = next(card for card, freq in Counter(leftover).items() if freq == 2)
        score = value_of_card(card2)
        leftover = leftover.replace(card2, "")
    else:
        score = 0
    weighted_score = score * pow(10, power)
    power -= 1
    all_scores.append(weighted_score)

    score = 0
    unique_leftover = set(leftover)
    for i, card in enumerate(top_to_lowest):
        ten_power = 10 ** (len(top_to_lowest) - i)
        if card in unique_leftover:
            score += ten_power
    score = score / 10 ** len(top_to_lowest)
    assert power == 0
    weighted_score = score * pow(10, power)
    all_scores.append(weighted_score)

    return sum(all_scores)


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
    sum += hand_to_bid[hand] * (len(sorted_by_strength) - i)
print(sum)
