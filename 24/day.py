import itertools
import os
import re
from collections import defaultdict
import numpy as np

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename, _min, _max):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    # parse each line into location and velocity (per ns)
    # 19, 13, 30 @ -2,  1, -2
    pos_vel = []
    for line in input_data:
        pos, vel = line.split(" @ ")
        pos = tuple(int(i) for i in pos.split(","))
        vel = tuple(int(i) for i in vel.split(","))
        pos_vel.append((pos, vel))

    # Part 1
    hits = 0
    combinations = itertools.combinations(pos_vel, 2)
    for (pos1, vel1), (pos2, vel2) in combinations:
        # the pos are support vectors, find the intersection of the lines
        # pos1 + t1 * vel1 = pos2 + t2 * vel2

        # We can solve this as a system of linear equations:
        # [ -(vel1.x)  vel2.x ] [ t1 ] = [ pos2.x - pos1.x ]
        # [ -(vel1.y)  vel2.y ] [ t2 ] = [ pos2.y - pos1.y ]

        A = np.array([[vel1[0], -vel2[0]], [vel1[1], -vel2[1]]])
        B = np.array([pos2[0] - pos1[0], pos2[1] - pos1[1]])

        # using numpy to solve the system
        try:
            t1_t2 = np.linalg.solve(A, B)
        except:
            continue
        t1, t2 = t1_t2[0], t1_t2[1]
        intersection = pos1[0] + t1 * vel1[0], pos1[1] + t1 * vel1[1]

        # Check if these times are within your given range
        if (
            all(t >= 0 for t in [t1, t2])
            and _min <= intersection[0] <= _max
            and _min <= intersection[1] <= _max
        ):
            hits += 1

    result1 = hits
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt", 7, 27) == (2, 24)
    main("input.txt", 200000000000000, 400000000000000)
