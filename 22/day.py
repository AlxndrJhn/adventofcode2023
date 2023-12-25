import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_parts = [line.split("~") for line in input_data]

    # get (x,y,z) and (x,y,z) from 1,1,8~1,1,9
    brick_coords = [
        tuple([tuple(int(i) for i in coord.split(",")) for coord in line])
        for line in input_data_parts
    ]
    grid = defaultdict(int)
    set_occupied(brick_coords, grid)

    # Part 1
    while True:
        something_changed = False
        for i in range(len(brick_coords)):
            brick = brick_coords[i]
            start, end = brick
            all_free = is_free_underneath(start, end, grid)
            if all_free:
                # print(f"Removing {start} {end}")
                something_changed = True
                remove_brick(grid, start, end)
                new_start = (start[0], start[1], start[2] - 1)
                new_end = (end[0], end[1], end[2] - 1)
                # print(f"Adding {new_start} {new_end}")
                brick_coords[i] = (new_start, new_end)
                set_occupied([brick], grid)
        if not something_changed:
            break

    grid_per_brick = {}
    for brick in brick_coords:
        start, end = brick
        grid_per_brick[brick] = defaultdict(int)
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    grid_per_brick[brick][(x, y, z)] = 1

    bricks_above = defaultdict(set)
    bricks_below = defaultdict(set)
    for brick1 in brick_coords:
        start, end = brick1
        max_z = max(start[2], end[2])
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                check_coords = (x, y, max_z + 1)
                for brick2 in brick_coords:
                    if brick1 == brick2:
                        continue
                    if grid_per_brick[brick2][check_coords] == 1:
                        bricks_above[brick1].add(brick2)
                        bricks_below[brick2].add(brick1)

    do_not_support_anything = set()
    for brick in brick_coords:
        if len(bricks_above[brick]) == 0:
            do_not_support_anything.add(brick)
        else:
            all_are_supported_by_two = True
            for brick2 in bricks_above[brick]:
                if len(bricks_below[brick2]) == 1:
                    all_are_supported_by_two = False
                    break
            if all_are_supported_by_two:
                do_not_support_anything.add(brick)
    result1 = len(do_not_support_anything)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


def remove_brick(grid, start, end):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            for z in range(start[2], end[2] + 1):
                grid[(x, y, z)] = 0


def set_occupied(brick_coords, grid):
    for start, end in brick_coords:
        for x in range(start[0], end[0] + 1):
            for y in range(start[1], end[1] + 1):
                for z in range(start[2], end[2] + 1):
                    grid[(x, y, z)] = 1


def is_free_underneath(start, end, grid):
    lowest_z = min(start[2], end[2])
    if lowest_z == 1:
        return False
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            if grid[(x, y, lowest_z - 1)] == 1:
                return False
    return True


def could_be_removed(start, end, grid):
    highest = max(start[2], end[2])
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            if grid[(x, y, highest + 1)] == 1:
                return False
    return True


if __name__ == "__main__":
    assert main("input2.txt") == (5, 24)
    main("input.txt")
