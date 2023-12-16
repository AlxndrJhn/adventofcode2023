from collections import defaultdict
import os
import re

this_folder = "\\".join(__file__.split("\\")[:-1])


# string enum with directions
class Direction:
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


# class with ray factory that contains width and height of the matrix
class RayFactory:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def create_ray(self, x, y, direction):
        return Ray(x, y, direction, self.width, self.height)


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
    def __init__(self, x, y, direction, width, height):
        self.x = x
        self.y = y
        self.direction = direction
        self.width = width
        self.height = height

    def __str__(self):
        return f"Ray({self.x}, {self.y}, {self.direction})"

    def isInBounds(self):
        return 0 <= self.x < self.width and 0 <= self.y < self.height


def main(filename):
    input_data = [
        list(line) for line in open(f"{this_folder}/{filename}", "r").read().split("\n")
    ]
    rayFactory = RayFactory(len(input_data[0]), len(input_data))
    # Part 1
    energized_mat = [[EMPTY for _ in range(len(input_data[0]))] for _ in input_data]

    list_of_rays = [rayFactory.create_ray(0, 0, Direction.RIGHT)]
    known_rays = set()
    while len(list_of_rays) > 0:
        ray = list_of_rays.pop()
        if str(ray) in known_rays:
            continue
        if not ray.isInBounds():
            continue
        energized_mat[ray.x][ray.y] = "#"
        this_field = input_data[ray.x][ray.y]
        if this_field == EMPTY:
            move = DIR_TO_COORD_CHANGE[ray.direction]
            new_ray = rayFactory.create_ray(
                ray.x + move[0], ray.y + move[1], ray.direction
            )
            list_of_rays.append(new_ray)
        elif this_field == MIRRORSLASH or this_field == MIRRORBACKSLASH:
            dir = DIR_MIRROR_CHANGE[(ray.direction, this_field)]
            move = DIR_TO_COORD_CHANGE[dir]
            new_ray = rayFactory.create_ray(ray.x + move[0], ray.y + move[1], dir)
            list_of_rays.append(new_ray)
        elif this_field == VERTSPLIT or this_field == HORSPLIT:
            moves = DIR_SPLIT_CHANGE[(ray.direction, this_field)]
            for dir in moves:
                move = DIR_TO_COORD_CHANGE[dir]
                new_ray = rayFactory.create_ray(ray.x + move[0], ray.y + move[1], dir)
                list_of_rays.append(new_ray)
        else:
            raise Exception("Unknown field type")
        known_rays.add(str(ray))

    # for row in energized_mat:
    #     print("".join(row))

    energized_fields = sum([row.count("#") for row in energized_mat])
    result1 = energized_fields

    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (46, 24)
    main("input.txt")
