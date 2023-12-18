import itertools
import os
import re
from collections import defaultdict
from matplotlib import path

this_folder = "\\".join(__file__.split("\\")[:-1])

UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"
LR = "LR"
LL = "LL"
UR = "UR"
UL = "UL"


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
    polygon = [(0, 0)]
    x, y = 0, 0
    perimeter = 0
    dirs = []
    dir_map = {"U": 3, "D": 1, "L": 2, "R": 0}
    for line in input_data_mat:
        direction, distance, rgb = line
        rgb = rgb[2:-1]
        distance = int(distance)
        direction = dir_map[direction]
        distance = int(rgb[:5], 16)
        direction = int(rgb[5])
        perimeter += distance
        if direction == 3:
            x -= distance
            dirs.append(UP)
        elif direction == 1:
            x += distance
            dirs.append(DOWN)
        elif direction == 2:
            y -= distance
            dirs.append(LEFT)
        elif direction == 0:
            y += distance
            dirs.append(RIGHT)
        polygon.append((x, y))
    polygon = polygon[:-1]
    # put last element to the beginning
    dirs = [dirs[-1]] + dirs[:-1]

    mapping = {
        (RIGHT, DOWN): LL,
        (RIGHT, UP): LR,
        (RIGHT, RIGHT): LR,
        (DOWN, LEFT): UL,
        (DOWN, RIGHT): LL,
        (DOWN, DOWN): UL,
        (LEFT, UP): UR,
        (LEFT, DOWN): UL,
        (LEFT, LEFT): UR,
        (UP, RIGHT): LR,
        (UP, LEFT): UR,
        (UP, UP): UR,
    }
    inner = []
    OFFSET = 0.5
    shifted = itertools.cycle(dirs)
    next(shifted)
    for dir1, dir2, node in zip(itertools.cycle(dirs), shifted, polygon):
        x, y = node
        corner = mapping[(dir1, dir2)]
        if corner == LL:
            x += OFFSET
            y -= OFFSET
        elif corner == LR:
            x += OFFSET
            y += OFFSET
        elif corner == UL:
            x -= OFFSET
            y -= OFFSET
        elif corner == UR:
            x -= OFFSET
            y += OFFSET
        inner.append((x, y))

    polygon = polygon[::-1]
    xs, ys = zip(*polygon)

    def area(p):
        return 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments(p)))

    def segments(p):
        return zip(p, p[1:] + [p[0]])

    result2 = int(area(inner[::-1]) + perimeter)
    print(f"Part 2 {filename}: ", result2)
    return 62, result2


if __name__ == "__main__":
    assert main("input2.txt") == (62, 952408144115)
    main("input.txt")
