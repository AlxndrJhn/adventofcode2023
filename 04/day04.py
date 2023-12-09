from collections import defaultdict
import re


input_data = open("04/input.txt", "r").read().split("\n")

# Part 1
_sum = 0
for line in input_data:
    # get all \d+ from line.split("|")[0].split(":")[1]
    winning_nums_str = line.split("|")[0].split(":")[1]
    pattern = r"\d+"
    winning_nums = [int(x) for x in re.findall(pattern, winning_nums_str)]
    my_nums_str = line.split("|")[1]
    my_nums = [int(x) for x in re.findall(pattern, my_nums_str)]

    count_matches = [my in winning_nums for my in my_nums].count(True)
    if count_matches == 0:
        continue
    _sum += pow(2, count_matches - 1)
print(_sum)

# Part 2
_sum = 0
copies = defaultdict(int)
for line in input_data:
    winning_nums_str, my_nums_str = line.split("|")
    card_num_str, winning_nums_str = winning_nums_str.split(":")
    card_num = int(card_num_str.split(" ")[-1])
    copies[card_num] += 1
    pattern = r"\d+"
    winning_nums = [int(x) for x in re.findall(pattern, winning_nums_str)]
    my_nums = [int(x) for x in re.findall(pattern, my_nums_str)]

    count_matches = [my in winning_nums for my in my_nums].count(True)
    _sum += copies[card_num]
    for i in range(count_matches):
        copies[card_num + i + 1] += copies[card_num]
print(_sum)
