from collections import defaultdict
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}/input.txt", "r").read().split("\n")

# Part 1

# get row,col for character "S"
start = (0, 0)
for row in range(len(input_data)):
    for col in range(len(input_data[row])):
        if input_data[row][col] == "S":
            start = (row, col)
            break
    if start != (0, 0):
        break


def get_adjacent(row, col):
    adjacent = []
    if row > 0:
        adjacent.append((-1, 0))
    if row < len(input_data) - 1:
        adjacent.append((+1, 0))
    if col > 0:
        adjacent.append((0, -1))
    if col < len(input_data[row]) - 1:
        adjacent.append((0, +1))
    move_and_content = [
        (move, input_data[row + move[0]][col + move[1]]) for move in adjacent
    ]
    return move_and_content


S = "S"
h = "-"
v = "|"
L = "L"
J = "J"
_7 = "7"
F = "F"
dot = "."

M_left = (0, -1)
M_right = (0, 1)
M_up = (-1, 0)
M_down = (1, 0)

val_moves = {
    (v, M_down): {v, L, J},
    (v, M_up): {v, _7, F},
    (h, M_left): {h, L, F},
    (h, M_right): {h, _7, J},
    (L, M_up): {v, _7, F},
    (L, M_right): {h, _7, J},
    (J, M_up): {v, _7, F},
    (J, M_left): {h, L, F},
    (_7, M_down): {v, L, J},
    (_7, M_left): {h, L, F},
    (F, M_right): {h, _7, J},
    (F, M_down): {v, L, J},
}

S_can_be = {h, v, L, J, _7, F}

lowest = float("inf")
input_data_copy = [row[:] for row in input_data]
for S_is in S_can_be:
    matrix = [[-1] * len(input_data[0]) for _ in range(len(input_data))]
    matrix[start[0]][start[1]] = 0
    queue = [start]
    while queue:
        row, col = queue.pop(0)
        this_field = S_is if (row, col) == start else input_data[row][col]
        for move, content in get_adjacent(row, col):
            is_valid = (this_field, move) in val_moves and content in val_moves[
                (this_field, move)
            ]
            if is_valid and matrix[row + move[0]][col + move[1]] == -1:
                matrix[row + move[0]][col + move[1]] = matrix[row][col] + 1
                queue.append((row + move[0], col + move[1]))
    max_in_matrix = max([max(row) for row in matrix])
    col_max = -1
    row_max = -1
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == max_in_matrix:
                col_max = col
                row_max = row
    valid_moves = 0
    for move, content in get_adjacent(row_max, col_max):
        is_valid = (this_field, move) in val_moves and content in val_moves[
            (this_field, move)
        ]
        if is_valid:
            valid_moves += 1
    # the maximum must have two valid adjacent fields

    if valid_moves == 2 and max_in_matrix < lowest:
        lowest = max_in_matrix
        lowest_matrix = [row[:] for row in matrix]
        lowest_input_data = [row[:] for row in input_data]
        lowest_input_data[start[0]] = (
            lowest_input_data[start[0]][: start[1]]
            + S_is
            + lowest_input_data[start[0]][start[1] + 1 :]
        )
print(lowest)


def vertical_changes(cells, vals):
    cells_used = [cells[i] for i in range(len(cells)) if vals[i] > -1]
    cells_str = "".join(cells_used)
    cells_str = cells_str.replace(h, "")
    count_changes = 0
    vert_changes = [v, F + J, L + _7]
    for vert in vert_changes:
        count_changes += cells_str.count(vert)
    return count_changes


def horizontal_changes(cells, vals):
    cells_used = [cells[i] for i in range(len(cells)) if vals[i] > -1]
    cells_str = "".join(cells_used)
    cells_str = cells_str.replace(v, "")
    count_changes = 0
    vert_changes = [h, _7 + L, F + J]
    for vert in vert_changes:
        count_changes += cells_str.count(vert)
    return count_changes


mat = lowest_matrix
encapsulated = 0
mat_copy = [[" "] * len(mat[0]) for _ in range(len(mat))]
for row in range(len(mat)):
    for col in range(len(mat[row])):
        if mat[row][col] == -1:
            cells_left = mat[row][:col]
            cells_left_fields = lowest_input_data[row][:col]
            left_changes = vertical_changes(cells_left_fields, cells_left)

            cells_right = mat[row][col + 1 :]
            cells_right_fields = lowest_input_data[row][col + 1 :]
            right_changes = vertical_changes(cells_right_fields, cells_right)

            cells_up = [mat[i][col] for i in range(row)]
            cells_up_fields = [lowest_input_data[i][col] for i in range(row)]
            up_changes = horizontal_changes(cells_up_fields, cells_up)

            cells_down = [mat[i][col] for i in range(row + 1, len(mat))]
            cells_down_fields = [
                lowest_input_data[i][col] for i in range(row + 1, len(mat))
            ]
            down_changes = horizontal_changes(cells_down_fields, cells_down)

            # count tha number of cells that are >0
            odd_count = 0
            for c in [left_changes, right_changes, up_changes, down_changes]:
                if c % 2 == 1:
                    odd_count += 1
            if odd_count >= 4:
                encapsulated += 1
                mat_copy[row][col] = "I"
            else:
                mat_copy[row][col] = "X"

for row in mat_copy:
    print("".join(row))
print(encapsulated)
