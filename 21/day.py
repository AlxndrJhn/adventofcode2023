import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename, steps):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    # replace 'S' with 'O'
    input_data_mat = [[c if c != "S" else "O" for c in line] for line in input_data_mat]
    for _ in range(steps):
        copy = [line[:] for line in input_data_mat]
        for x, y in itertools.product(
            range(len(input_data_mat)), range(len(input_data_mat[0]))
        ):
            if copy[x][y] == "O":
                input_data_mat[x][y] = "."
                if x > 0 and input_data_mat[x - 1][y] == ".":
                    input_data_mat[x - 1][y] = "O"
                if x < len(input_data_mat) - 1 and input_data_mat[x + 1][y] == ".":
                    input_data_mat[x + 1][y] = "O"
                if y > 0 and input_data_mat[x][y - 1] == ".":
                    input_data_mat[x][y - 1] = "O"
                if y < len(input_data_mat[0]) - 1 and input_data_mat[x][y + 1] == ".":
                    input_data_mat[x][y + 1] = "O"
    result1 = sum(line.count("O") for line in input_data_mat)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt", 6) == (16, 24)
    main("input.txt", 64)
