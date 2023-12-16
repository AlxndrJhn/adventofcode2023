from collections import defaultdict
import re
import itertools
from functools import lru_cache

this_folder = "\\".join(__file__.split("\\")[:-1])

Q = "?"
D = "."
H = "#"


@lru_cache(maxsize=None)
def count_arrangements(seq, groups):
    if len(seq) == 0:
        return 1 if len(groups) == 0 else 0
    if seq.startswith(D):
        return count_arrangements(seq[1:], groups)
    if seq.startswith(Q):
        v1 = count_arrangements(D + seq[1:], groups)
        v2 = count_arrangements(H + seq[1:], groups)
        return v1 + v2
    if seq.startswith(H):
        if len(groups) == 0:
            return 0
        expected_length = groups[0]
        chars = seq[:expected_length]
        if len(chars) != expected_length:
            return 0
        if any(c == D for c in chars):
            return 0

        if len(seq) > expected_length:
            if seq[expected_length] == H:
                return 0
            elif seq[expected_length] == Q:
                return count_arrangements(D + seq[expected_length + 1 :], groups[1:])
        groups = groups[1:]
        seq = seq[expected_length:]
        return count_arrangements(seq, groups)


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
        arrangements = count_arrangements(row, tuple(groups))
        sum1 += arrangements
    print(f"Part 1 {filename}: ", sum1)

    # part 2
    sum2 = 0
    for line in input_data:
        seq_before, groups_str_before = line.split(" ")
        len_of_groups_before = [int(x) for x in re.findall(r"\d+", groups_str_before)]
        seq = Q.join([seq_before] * 5)
        groups = len_of_groups_before * 5
        arrangements = count_arrangements(seq, tuple(groups))
        sum2 += arrangements
    print(f"Part 2 {filename}: ", sum2)
    return sum1, sum2


if __name__ == "__main__":
    assert main("input2.txt") == (21, 525152)
    main("input.txt")
