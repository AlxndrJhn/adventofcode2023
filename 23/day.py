import functools
import itertools
import os
import re
from collections import defaultdict
import sys


this_folder = "\\".join(__file__.split("\\")[:-1])

DOWN = "↓"
UP = "↑"
LEFT = "←"
RIGHT = "→"
EMPTY = "."
WALL = "#"
SLOPE_RIGHT = ">"
SLOPE_LEFT = "<"
SLOPE_DOWN = "v"


def print_grid(occupied_grid):
    [print("".join(line)) for line in occupied_grid]
    print()


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [list(line) for line in input_data]

    # Part 1
    start_row = 0
    start_col = next(idx for idx, val in enumerate(input_data_mat[0]) if val == ".")

    def get_pos(moves_so_far):
        copied_grid = [list(line) for line in input_data_mat]
        row, col = start_row, start_col
        copied_grid[row][col] = "#"
        for move in moves_so_far:
            if move == UP:
                row -= 1
            elif move == DOWN:
                row += 1
            elif move == LEFT:
                col -= 1
            elif move == RIGHT:
                col += 1
            copied_grid[row][col] = "O"
        copied_grid[row][col] = "X"
        return row, col, copied_grid

    def get_neighbors(occupied_grid, row, col, ignore_slopes):
        neighbors = []
        if input_data_mat[row][col] == SLOPE_RIGHT and not ignore_slopes:
            if (
                col < len(input_data_mat[0]) - 1
                and occupied_grid[row][col + 1] == EMPTY
            ):
                return [(RIGHT, row, col + 1)]
            return []
        if input_data_mat[row][col] == SLOPE_LEFT and not ignore_slopes:
            if col > 0 and occupied_grid[row][col - 1] == EMPTY:
                return [(LEFT, row, col - 1)]
            return []
        if input_data_mat[row][col] == SLOPE_DOWN and not ignore_slopes:
            if row < len(input_data_mat) - 1 and occupied_grid[row + 1][col] == EMPTY:
                return [(DOWN, row + 1, col)]
            return []
        if row > 0 and occupied_grid[row - 1][col] in [EMPTY, SLOPE_DOWN]:
            neighbors.append((UP, row - 1, col))
        if row < len(occupied_grid) - 1 and occupied_grid[row + 1][col] in [
            EMPTY,
            SLOPE_DOWN,
        ]:
            neighbors.append((DOWN, row + 1, col))
        if col > 0 and occupied_grid[row][col - 1] in [EMPTY, SLOPE_LEFT]:
            neighbors.append((LEFT, row, col - 1))
        if col < len(occupied_grid[0]) - 1 and occupied_grid[row][col + 1] in [
            EMPTY,
            SLOPE_RIGHT,
        ]:
            neighbors.append((RIGHT, row, col + 1))
        return neighbors

    goal_row = len(input_data_mat) - 1
    goal_col = next(idx for idx, val in enumerate(input_data_mat[-1]) if val == EMPTY)

    def get_longest_path(moves_so_far, ignore_slopes):
        row, col, occupied_grid = get_pos(moves_so_far)
        if row == goal_row and col == goal_col:
            return len(moves_so_far), moves_so_far
        # if only one move available, take it until it splits
        while (
            len(get_neighbors(occupied_grid, row, col, ignore_slopes=ignore_slopes))
            == 1
        ):
            move, n_row, n_col = get_neighbors(
                occupied_grid, row, col, ignore_slopes=ignore_slopes
            )[0]
            moves_so_far += (move,)
            row, col, occupied_grid = get_pos(moves_so_far)
            if row == goal_row and col == goal_col:
                return len(moves_so_far), moves_so_far
        lengths, paths = [], []
        for move, n_row, n_col in get_neighbors(
            occupied_grid, row, col, ignore_slopes=ignore_slopes
        ):
            length, path = get_longest_path(
                moves_so_far + (move,), ignore_slopes=ignore_slopes
            )
            lengths.append(length)
            paths.append(path)
        if not lengths:
            return 0, []
        longest = max(lengths)
        return longest, paths[lengths.index(longest)]

    result1, path = get_longest_path((), ignore_slopes=False)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2, path = get_longest_path((), ignore_slopes=True)
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (94, 154)
    main("input.txt")
