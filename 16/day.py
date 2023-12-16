from collections import defaultdict
import itertools
import os
import re

this_folder = "\\".join(__file__.split("\\")[:-1])


class Direction:
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


EMPTY = "."
MIRRORSLASH = "/"
MIRRORBACKSLASH = "\\"
VERTSPLIT = "|"
HORSPLIT = "-"

DIR_TO_COORD_CHANGE = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}

DIR_MIRROR_CHANGE = {
    (Direction.UP, MIRRORSLASH): Direction.RIGHT,
    (Direction.DOWN, MIRRORSLASH): Direction.LEFT,
    (Direction.LEFT, MIRRORSLASH): Direction.DOWN,
    (Direction.RIGHT, MIRRORSLASH): Direction.UP,
    (Direction.UP, MIRRORBACKSLASH): Direction.LEFT,
    (Direction.DOWN, MIRRORBACKSLASH): Direction.RIGHT,
    (Direction.LEFT, MIRRORBACKSLASH): Direction.UP,
    (Direction.RIGHT, MIRRORBACKSLASH): Direction.DOWN,
}

DIR_SPLIT_CHANGE = {
    (Direction.UP, VERTSPLIT): [Direction.UP],
    (Direction.DOWN, VERTSPLIT): [Direction.DOWN],
    (Direction.LEFT, VERTSPLIT): [Direction.UP, Direction.DOWN],
    (Direction.RIGHT, VERTSPLIT): [Direction.UP, Direction.DOWN],
    (Direction.LEFT, HORSPLIT): [Direction.LEFT],
    (Direction.RIGHT, HORSPLIT): [Direction.RIGHT],
    (Direction.UP, HORSPLIT): [Direction.LEFT, Direction.RIGHT],
    (Direction.DOWN, HORSPLIT): [Direction.LEFT, Direction.RIGHT],
}


class Ray:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __str__(self):
        return f"Ray({self.x}, {self.y}, {self.direction})"

    def isInBounds(self, input_data):
        return 0 <= self.x < len(input_data[0]) and 0 <= self.y < len(input_data)


def solve(start, input_data):
    energized_mat = [[EMPTY for _ in range(len(input_data[0]))] for _ in input_data]
    list_of_rays = [start]
    known_rays = set()
    while len(list_of_rays) > 0:
        ray = list_of_rays.pop()
        if str(ray) in known_rays:
            continue
        if not ray.isInBounds(input_data):
            continue
        energized_mat[ray.x][ray.y] = "#"
        this_field = input_data[ray.x][ray.y]
        if this_field == EMPTY:
            move = DIR_TO_COORD_CHANGE[ray.direction]
            new_ray = Ray(ray.x + move[0], ray.y + move[1], ray.direction)
            list_of_rays.append(new_ray)
        elif this_field == MIRRORSLASH or this_field == MIRRORBACKSLASH:
            dir = DIR_MIRROR_CHANGE[(ray.direction, this_field)]
            move = DIR_TO_COORD_CHANGE[dir]
            new_ray = Ray(ray.x + move[0], ray.y + move[1], dir)
            list_of_rays.append(new_ray)
        elif this_field == VERTSPLIT or this_field == HORSPLIT:
            moves = DIR_SPLIT_CHANGE[(ray.direction, this_field)]
            for dir in moves:
                move = DIR_TO_COORD_CHANGE[dir]
                new_ray = Ray(ray.x + move[0], ray.y + move[1], dir)
                list_of_rays.append(new_ray)
        else:
            raise Exception("Unknown field type")
        known_rays.add(str(ray))

    # for row in energized_mat:
    #     print("".join(row))

    energized_fields = sum([row.count("#") for row in energized_mat])
    return energized_fields


def main(filename):
    input_data = [
        list(line) for line in open(f"{this_folder}/{filename}", "r").read().split("\n")
    ]
    # Part 1
    result1 = solve(Ray(0, 0, Direction.RIGHT), input_data)

    print(f"Part 1 {filename}: ", result1)

    # Part 2
    _max = 0
    start_and_dir = []
    # top
    x = 0
    for y in range(len(input_data[0])):
        start_and_dir.append((x, y, Direction.DOWN))
    x = len(input_data) - 1
    for y in range(len(input_data[0])):
        start_and_dir.append((x, y, Direction.UP))
    y = 0
    for x in range(len(input_data)):
        start_and_dir.append((x, y, Direction.RIGHT))
    y = len(input_data[0]) - 1
    for x in range(len(input_data)):
        start_and_dir.append((x, y, Direction.LEFT))

    for x, y, dir in start_and_dir:
        result = solve(Ray(x, y, dir), input_data)
        if result > _max:
            _max = result

    result2 = _max
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (46, 51)
    main("input.txt")
