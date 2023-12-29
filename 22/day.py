from functools import lru_cache
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

    def num_to_alpha(num):
        return chr(ord("A") + num)

    name_to_coords = {num_to_alpha(i): coord for i, coord in enumerate(brick_coords)}
    coords_to_name = defaultdict(lambda: None)
    for name, brick in name_to_coords.items():
        set_links_to_brick(coords_to_name, name, brick)
    while True:
        something_changed = False
        for name, brick in name_to_coords.items():
            lowest_z = min(brick, key=lambda x: x[2])[2]
            if lowest_z == 1:
                continue
            is_blocked = False
            for z in range(lowest_z - 1, 0, -1):
                for x, y in get_xy_generator(brick):
                    if coords_to_name[(x, y, z)] is not None:
                        new_z = z + 1
                        is_blocked = True
                        break
                if is_blocked:
                    break
            else:
                new_z = 1
            if new_z != lowest_z:
                remove_links_to_brick(coords_to_name, name, brick)
                lower_brick = move_down(brick, lowest_z - new_z)
                name_to_coords[name] = lower_brick
                set_links_to_brick(coords_to_name, name, lower_brick)
                something_changed = True
        if not something_changed:
            break
    # check supporting
    bricks_above, bricks_below = get_brick_graph(name_to_coords)
    bricks_that_are_optional = set()
    for name in name_to_coords.keys():
        if len(bricks_above[name]) == 0:
            bricks_that_are_optional.add(name)
            continue
        all_above_have_two_below = True
        for above_name in bricks_above[name]:
            if len(bricks_below[above_name]) == 1:
                all_above_have_two_below = False
                break
        if all_above_have_two_below:
            bricks_that_are_optional.add(name)
    result1 = len(bricks_that_are_optional)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    affected_bricks = 0
    for name in name_to_coords.keys():
        if len(bricks_above[name]) == 0:
            continue
        count_affected = 0
        bricks_to_check = set(bricks_above[name])
        bricks_that_fall = set(name)
        while bricks_to_check:
            brick = bricks_to_check.pop()
            below_bricks_that_do_not_fall = (
                bricks_below[brick] - bricks_that_fall - {name}
            )
            has_two_or_more_below = len(below_bricks_that_do_not_fall) >= 1
            if not has_two_or_more_below:
                count_affected += 1
                bricks_that_fall.add(brick)
                bricks_to_check.update(bricks_above[brick])
        affected_bricks += count_affected
    result2 = affected_bricks
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


def move_down(brick, z_diff):
    return (
        (brick[0][0], brick[0][1], brick[0][2] - z_diff),
        (brick[1][0], brick[1][1], brick[1][2] - z_diff),
    )


def set_links_to_brick(coords_to_name, name, brick):
    # print("set_links_to_brick", name, brick)
    for x, y, z in get_xyz_points(brick):
        assert coords_to_name[(x, y, z)] is None
        coords_to_name[(x, y, z)] = name


def remove_links_to_brick(coords_to_name, name, brick):
    # print("remove_links_to_brick", name, brick)
    pass
    for x, y, z in get_xyz_points(brick):
        assert (
            coords_to_name[(x, y, z)] == name
        ), f"{coords_to_name[(x, y, z)]} is {name}"
        coords_to_name[(x, y, z)] = None


def get_xyz_points(coords):
    return set(
        itertools.product(
            range(coords[0][0], coords[1][0] + 1),
            range(coords[0][1], coords[1][1] + 1),
            range(coords[0][2], coords[1][2] + 1),
        )
    )


def get_xy_generator(coords):
    return set(
        itertools.product(
            range(coords[0][0], coords[1][0] + 1),
            range(coords[0][1], coords[1][1] + 1),
        )
    )


def get_brick_graph(name_to_brick_coords):
    bricks_above = defaultdict(set)
    bricks_below = defaultdict(set)
    for name1, brick1 in name_to_brick_coords.items():
        for name2, brick2 in name_to_brick_coords.items():
            if name1 == name2:
                continue
            brick2_points = get_xyz_points(brick2)
            # check if brick2 is supporting brick1
            coord_brick1_with_lowest_z = min(brick1, key=lambda x: x[2])[2]
            coord_brick1_with_higher_z = max(brick1, key=lambda x: x[2])[2]
            if coord_brick1_with_lowest_z - 1 == 0:  # is on the ground
                bricks_below[name1].add(None)
            for x, y in get_xy_generator(brick1):
                if (x, y, coord_brick1_with_lowest_z - 1) in brick2_points:
                    bricks_below[name1].add(name2)
                    bricks_above[name2].add(name1)
                    break
                if (x, y, coord_brick1_with_higher_z + 1) in brick2_points:
                    bricks_below[name2].add(name1)
                    bricks_above[name1].add(name2)
                    break
    return bricks_above, bricks_below


if __name__ == "__main__":
    assert main("input2.txt") == (5, 7)
    main("input.txt")
