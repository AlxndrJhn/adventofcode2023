from collections import defaultdict
import re
import itertools
from functools import lru_cache

this_folder = "\\".join(__file__.split("\\")[:-1])

Q = "?"
OPTIONS = [".", "#"]


def count_arrangements(row, index, current_group_size, group_idx, groups, memo):
    if group_idx == len(groups):
        if current_group_size == 0:
            return 1
        else:
            return 0
    if current_group_size > groups[group_idx]:
        return 0
    if index == len(row):
        if current_group_size == groups[group_idx] and group_idx == len(groups) - 1:
            return 1
        else:
            return 0

    if (index, current_group_size, group_idx) in memo:
        return memo[(index, current_group_size, group_idx)]

    current_char = row[index]
    _sum = 0
    if current_char == "?":
        # .
        if current_group_size:
            if current_group_size == groups[group_idx]:
                _sum += count_arrangements(
                    row, index + 1, 0, group_idx + 1, groups, memo
                )
        else:
            _sum += count_arrangements(row, index + 1, 0, group_idx, groups, memo)
        # #
        _sum += count_arrangements(
            row, index + 1, current_group_size + 1, group_idx, groups, memo
        )
    elif current_char == ".":
        if current_group_size:
            if current_group_size == groups[group_idx]:
                _sum += count_arrangements(
                    row, index + 1, 0, group_idx + 1, groups, memo
                )
        else:
            _sum += count_arrangements(row, index + 1, 0, group_idx, groups, memo)
    elif current_char == "#":
        if current_group_size < groups[group_idx]:
            _sum += count_arrangements(
                row, index + 1, current_group_size + 1, group_idx, groups, memo
            )
    else:
        raise ValueError("Invalid character")
    memo[(index, current_group_size, group_idx)] = _sum
    return _sum


def main(filename):
    # part 1
    input_data = [
        line
        for line in open(f"{this_folder}/{filename}", "r").read().split("\n")
        if line
    ]
    sum1 = 0
    for line in input_data:
        seq, groups_str_before = line.split(" ")
        row, group_str = line.split()
        groups = list(map(int, group_str.split(",")))
        memo = {}
        arrangements = count_arrangements(row, 0, 0, 0, tuple(groups), memo)
        sum1 += arrangements
    print(f"Part 1 {filename}: ", sum1)

    # part 2
    sum2 = 0
    for line in input_data:
        seq_before, groups_str_before = line.split(" ")
        len_of_groups_before = [int(x) for x in re.findall(r"\d+", groups_str_before)]
        seq = Q.join([seq_before] * 5)
        len_of_groups = len_of_groups_before * 5
        memo = {}
        arrangements = count_arrangements(seq, 0, 0, 0, tuple(len_of_groups), memo)
        sum2 += arrangements
    print(f"Part 2 {filename}: ", sum2)
    return sum1, sum2


if __name__ == "__main__":
    assert main("input2.txt") == (21, 525152)
    main("input.txt")
