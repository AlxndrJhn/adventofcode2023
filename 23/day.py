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
SLOPE_UP = "^"


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
        return copied_grid

    def get_neighbors(occupied_grid, row, col, ignore_slopes):
        neighbors = []
        ALLOWED_RIGHT = [EMPTY, SLOPE_RIGHT, SLOPE_DOWN, SLOPE_UP]
        ALLOWED_LEFT = [EMPTY, SLOPE_LEFT, SLOPE_DOWN, SLOPE_UP]
        ALLOWED_DOWN = [EMPTY, SLOPE_DOWN, SLOPE_LEFT, SLOPE_RIGHT]
        ALLOWED_UP = [EMPTY, SLOPE_LEFT, SLOPE_RIGHT]
        if ignore_slopes:
            ALLOWED_LEFT += [SLOPE_RIGHT]
            ALLOWED_RIGHT += [SLOPE_LEFT]
            ALLOWED_UP += [SLOPE_DOWN]
            ALLOWED_DOWN += [SLOPE_UP]

        # I am on a slope
        if not ignore_slopes:
            if input_data_mat[row][col] == SLOPE_RIGHT:
                if (
                    col < len(input_data_mat[0]) - 1
                    and occupied_grid[row][col + 1] in ALLOWED_RIGHT
                ):
                    return [(RIGHT, row, col + 1)]
                return []
            if input_data_mat[row][col] == SLOPE_LEFT:
                if col > 0 and occupied_grid[row][col - 1] in ALLOWED_LEFT:
                    return [(LEFT, row, col - 1)]
                return []
            if input_data_mat[row][col] == SLOPE_DOWN:
                if (
                    row < len(input_data_mat) - 1
                    and occupied_grid[row + 1][col] in ALLOWED_DOWN
                ):
                    return [(DOWN, row + 1, col)]
                return []
            if input_data_mat[row][col] == SLOPE_UP:
                raise NotImplementedError()

        if row > 0 and occupied_grid[row - 1][col] in ALLOWED_UP:
            neighbors.append((UP, row - 1, col))
        if row < len(occupied_grid) - 1 and occupied_grid[row + 1][col] in ALLOWED_DOWN:
            neighbors.append((DOWN, row + 1, col))
        if col > 0 and occupied_grid[row][col - 1] in ALLOWED_LEFT:
            neighbors.append((LEFT, row, col - 1))
        if (
            col < len(occupied_grid[0]) - 1
            and occupied_grid[row][col + 1] in ALLOWED_RIGHT
        ):
            neighbors.append((RIGHT, row, col + 1))
        return neighbors

    goal_row = len(input_data_mat) - 1
    goal_col = next(idx for idx, val in enumerate(input_data_mat[-1]) if val == EMPTY)

    def processing(queue, copied_grid, ignore_slopes):
        while True:
            if not queue:
                break
            row, col, moves = queue.pop(0)
            occupied_grid = get_pos(moves)
            for move, new_row, new_col in get_neighbors(
                occupied_grid, row, col, ignore_slopes=ignore_slopes
            ):
                new_moves = moves + (move,)
                if copied_grid[new_row][new_col] < len(new_moves):
                    copied_grid[new_row][new_col] = len(new_moves)
                    queue.append((new_row, new_col, new_moves))

    copied_grid = [[0] * len(line) for line in input_data_mat]
    queue = [(start_row, start_col, ())]

    processing(queue, copied_grid, ignore_slopes=False)
    result1 = copied_grid[goal_row][goal_col]
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    # map all slopes to empty in input_data_mat
    for row in range(len(input_data_mat)):
        for col in range(len(input_data_mat[0])):
            if input_data_mat[row][col] in [
                SLOPE_RIGHT,
                SLOPE_LEFT,
                SLOPE_DOWN,
                SLOPE_UP,
            ]:
                input_data_mat[row][col] = EMPTY
    copied_grid2 = [[0] * len(line) for line in input_data_mat]
    queue2 = [(start_row, start_col, ())]
    processing(queue2, copied_grid2, ignore_slopes=True)
    result2 = copied_grid2[goal_row][goal_col]
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (94, 154)
    main("input.txt")
