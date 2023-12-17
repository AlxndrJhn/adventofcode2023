from copy import deepcopy
import itertools
import math
import os
import re
from collections import defaultdict
import functools

this_folder = "\\".join(__file__.split("\\")[:-1])


class Dir:
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


diff_to_dir = {
    (-1, 0): Dir.UP,
    (1, 0): Dir.DOWN,
    (0, -1): Dir.LEFT,
    (0, 1): Dir.RIGHT,
}

MAX_STRAIGHT = 3


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [[int(char) for char in line] for line in input_data]
    W = len(input_data_mat[0])
    H = len(input_data_mat)
    start_node = (0, 0)
    end_node = (W - 1, H - 1)

    @functools.lru_cache(maxsize=None)
    def get_distance(node1, node2):
        if node1[2] == Dir.DOWN and node2[2] == Dir.UP:
            return float("inf")
        if node1[2] == Dir.UP and node2[2] == Dir.DOWN:
            return float("inf")
        if node1[2] == Dir.LEFT and node2[2] == Dir.RIGHT:
            return float("inf")
        if node1[2] == Dir.RIGHT and node2[2] == Dir.LEFT:
            return float("inf")

        if node2[3] == MAX_STRAIGHT:
            return float("inf")

        return input_data_mat[node2[0]][node2[1]]

    def get_neighbors(node):
        x, y = node

        neighbors = []
        if x > 0:
            # UP
            neighbors.append((x - 1, y))
        if x < W - 1:
            # DOWN
            neighbors.append((x + 1, y))
        if y > 0:
            # LEFT
            neighbors.append((x, y - 1))
        if y < H - 1:
            # RIGHT
            neighbors.append((x, y + 1))
        return neighbors

    # Part 1
    # list of Dirs
    dirs = [Dir.UP, Dir.DOWN, Dir.LEFT, Dir.RIGHT]

    # use input_data_mat[x][y] as loss function, find path from START to END using Dijkstra's algorithm
    unvisited_nodes = set(itertools.product(range(W), range(H), dirs, range(3)))
    shortest_path = defaultdict(lambda: float("inf"))
    previous_nodes = {}

    shortest_path[start_node[0], start_node[1], Dir.RIGHT, 1] = 0

    while unvisited_nodes:
        print(len(unvisited_nodes))
        current_min_node = min(unvisited_nodes, key=lambda node: shortest_path[node])
        if shortest_path[current_min_node] == float("inf"):
            break
        *node, from_dir, dir_count = current_min_node
        node = tuple(node)
        neighbors = get_neighbors(node)
        for neighbor in neighbors:
            x_n, y_n = neighbor
            diff = (x_n - node[0], y_n - node[1])
            dir_to_n = diff_to_dir[diff]
            dir_count_n = dir_count + 1 if dir_to_n == from_dir else 0
            selector = (x_n, y_n, dir_to_n, dir_count_n)
            tentative_value = shortest_path[current_min_node] + get_distance(
                current_min_node, selector
            )
            if tentative_value < shortest_path[selector]:
                shortest_path[selector] = tentative_value
                previous_nodes[selector] = current_min_node

        unvisited_nodes.remove(current_min_node)

    all_end_nodes = [node for node in shortest_path if node[:2] == end_node]
    all_costs = [shortest_path[node] for node in all_end_nodes]
    lowest_cost = min(all_costs)

    result1 = lowest_cost
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (102, 24)
    main("input.txt")
