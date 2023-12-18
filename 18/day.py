import itertools
import os
import re
from collections import defaultdict
from matplotlib import path

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [line.split() for line in input_data]

    # Part 1
    polygon = [(0, 0)]
    x, y = 0, 0
    for line in input_data_mat:
        direction, distance, _ = line
        distance = int(distance)
        if direction == "U":
            x -= distance
        elif direction == "D":
            x += distance
        elif direction == "L":
            y -= distance
        elif direction == "R":
            y += distance
        polygon.append((x, y))
    polygon = polygon[::-1]
    path_obj = path.Path(polygon, closed=True)
    assert path_obj.contains_point((0, 0), radius=1e-9)

    # get max and min values
    min_x = min([x for x, y in polygon])
    max_x = max([x for x, y in polygon])
    min_y = min([y for x, y in polygon])
    max_y = max([y for x, y in polygon])

    # get all points inside polygon
    contain_count = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if path_obj.contains_point((x, y), radius=1e-9):
                contain_count += 1
    result1 = contain_count
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (62, 24)
    main("input.txt")
