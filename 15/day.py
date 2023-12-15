from collections import defaultdict
import os
import re

this_folder = "\\".join(__file__.split("\\")[:-1])


def get_hash(string):
    current_value = 0
    for char in string:
        ascii_value = ord(char)
        current_value += ascii_value
        current_value *= 17
        current_value %= 256
    return current_value


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split(",")
    # Part 1
    sum1 = 0
    for piece in input_data:
        sum1 += get_hash(piece)
    print(f"Part 1 {filename}: ", sum1)

    # Part 2
    print(f"Part 2 {filename}: ", 0)
    return sum1, 24


if __name__ == "__main__":
    assert get_hash("HASH") == 52
    assert main("input2.txt") == (1320, 24)
    main("input.txt")