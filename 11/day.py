from collections import defaultdict
import itertools
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}/input.txt", "r").read().split("\n")

# Part 1
EMPTY = "."
# expansion
matrix = [[x for x in line] for line in input_data]
WIDTH = len(matrix[0])
HEIGHT = len(matrix)
empty_cols = [
    i for i in range(WIDTH) if all([matrix[j][i] == EMPTY for j in range(HEIGHT)])
]
empty_rows = [
    i for i in range(HEIGHT) if all([matrix[i][j] == EMPTY for j in range(WIDTH)])
]

expanded_matrix = []
WIDTH += len(empty_cols)
HEIGHT += len(empty_rows)
for i, row in enumerate(matrix):
    if i in empty_rows:
        expanded_matrix.append([EMPTY for _ in range(WIDTH)])

    new_row = row.copy()
    for i in empty_cols[::-1]:
        new_row.insert(i, EMPTY)
    expanded_matrix.append(new_row)

galaxy_locations = []
for i, row in enumerate(expanded_matrix):
    for j, col in enumerate(row):
        if col == "#":
            galaxy_locations.append((i, j))

_sum = 0
combinations = list(itertools.combinations(range(len(galaxy_locations)), 2))

for i, j in combinations:
    x1, y1 = galaxy_locations[i]
    x2, y2 = galaxy_locations[j]
    L1_dist = abs(x1 - x2) + abs(y1 - y2)
    _sum += L1_dist
print(_sum)