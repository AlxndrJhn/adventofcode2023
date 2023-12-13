from collections import defaultdict
import os
import re

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    # Part 1

    print(f"Part 1 {filename}: ", 0)

    # Part 2
    print(f"Part 2 {filename}: ", 0)


if __name__ == "__main__":
    assert main("input2.txt") == (42, 24)
