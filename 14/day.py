from collections import defaultdict
import itertools
import os
import re

this_folder = "\\".join(__file__.split("\\")[:-1])

ROCK = "O"
EMPTY = "."


def main(filename):
    input_data = [
        list(line) for line in open(f"{this_folder}/{filename}", "r").read().split("\n")
    ]
    # Part 1

    # shift all O up
    while True:
        something_changed = False
        for x, y in itertools.product(
            range(1, len(input_data)), range(len(input_data[0]))
        ):
            if input_data[x][y] == ROCK and input_data[x - 1][y] == EMPTY:
                input_data[x - 1][y] = "O"
                input_data[x][y] = "."
                something_changed = True
        if not something_changed:
            break
    HEIGHT = len(input_data)
    weights = 0
    for x, y in itertools.product(range(len(input_data)), range(len(input_data[0]))):
        if input_data[x][y] == "O":
            weights += HEIGHT - x
    print(f"Part 1 {filename}: ", weights)

    # Part 2
    print(f"Part 2 {filename}: ", 0)
    return weights, 0


if __name__ == "__main__":
    assert main("input2.txt") == (136, 0)
    main("input.txt")