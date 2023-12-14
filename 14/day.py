from collections import defaultdict
from copy import deepcopy
import itertools
import os
import re

this_folder = "\\".join(__file__.split("\\")[:-1])

ROCK = "O"
EMPTY = "."


class DIR:
    WEST = 0
    EAST = 1
    NORTH = 2
    SOUTH = 3


def tilt(dir: DIR, mat):
    offset_x = 1 if dir == DIR.NORTH else 0
    offset_x_end = 1 if dir == DIR.SOUTH else 0
    offset_y = 1 if dir == DIR.WEST else 0
    offset_y_end = 1 if dir == DIR.EAST else 0
    while True:
        something_changed = False
        for x, y in itertools.product(
            range(offset_x, len(mat) - offset_x_end),
            range(offset_y, len(mat[0]) - offset_y_end),
        ):
            # x - 1 for up, x + 1 for down, x for else
            next_x = x - 1 if dir == DIR.NORTH else x + 1 if dir == DIR.SOUTH else x
            next_y = y - 1 if dir == DIR.WEST else y + 1 if dir == DIR.EAST else y
            if mat[x][y] == ROCK and mat[next_x][next_y] == EMPTY:
                mat[next_x][next_y] = "O"
                mat[x][y] = "."
                something_changed = True
        if not something_changed:
            return mat


def calc_weight(mat):
    HEIGHT = len(mat)
    weight = 0
    for x, y in itertools.product(range(len(mat)), range(len(mat[0]))):
        if mat[x][y] == ROCK:
            weight += HEIGHT - x
    return weight


def main(filename):
    input_data = [
        list(line) for line in open(f"{this_folder}/{filename}", "r").read().split("\n")
    ]
    # Part 1

    # shift all O up
    mat = tilt(DIR.NORTH, input_data)
    weight1 = calc_weight(mat)
    print(f"Part 1 {filename}: ", weight1)

    # Part 2
    mat = deepcopy(input_data)
    hash_to_weight = {}
    seen_hashes = []
    CYCLE_COUNT = 1_000_000_000
    for cycle_idx in range(CYCLE_COUNT):
        mat = tilt(DIR.NORTH, mat)
        mat = tilt(DIR.WEST, mat)
        mat = tilt(DIR.SOUTH, mat)
        mat = tilt(DIR.EAST, mat)
        w = calc_weight(mat)
        hash_value = hash(str(mat))
        hash_to_weight[hash_value] = w
        if hash_value in seen_hashes:
            cycle_length = cycle_idx - seen_hashes.index(hash_value)
            break
        seen_hashes.append(hash_value)
    remaining_cycles = CYCLE_COUNT - cycle_idx - 1
    goal_hash_offset = remaining_cycles % cycle_length
    goal_hash_idx = cycle_idx - cycle_length + goal_hash_offset
    goal_hash = seen_hashes[goal_hash_idx]
    weight2 = hash_to_weight[goal_hash]
    print(f"Part 2 {filename}: ", weight2)
    return weight1, weight2


if __name__ == "__main__":
    assert main("input2.txt") == (136, 64)
    main("input.txt")
