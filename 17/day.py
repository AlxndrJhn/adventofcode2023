from copy import deepcopy
import heapq
import itertools
import math
import os
import re
from collections import defaultdict

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
MIN_STRAIGHT2 = 4
MAX_STRAIGHT2 = 10


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [[int(char) for char in line] for line in input_data]
    W = len(input_data_mat[0])
    H = len(input_data_mat)
    start_node = (0, 0)
    end_node = (H - 1, W - 1)

    # def get_distance(node1, node2):
    #     if node1[2] == Dir.DOWN and node2[2] == Dir.UP:
    #         return float("inf")
    #     if node1[2] == Dir.UP and node2[2] == Dir.DOWN:
    #         return float("inf")
    #     if node1[2] == Dir.LEFT and node2[2] == Dir.RIGHT:
    #         return float("inf")
    #     if node1[2] == Dir.RIGHT and node2[2] == Dir.LEFT:
    #         return float("inf")

    #     if node2[3] == MAX_STRAIGHT:
    #         return float("inf")

    #     return input_data_mat[node2[0]][node2[1]]

    def get_neighbors(node):
        x, y = node

        neighbors = []
        if x > 0:
            # UP
            neighbors.append((x - 1, y))
        if x < H - 1:
            # DOWN
            neighbors.append((x + 1, y))
        if y > 0:
            # LEFT
            neighbors.append((x, y - 1))
        if y < W - 1:
            # RIGHT
            neighbors.append((x, y + 1))
        return neighbors

    dirs = [Dir.UP, Dir.DOWN, Dir.LEFT, Dir.RIGHT]

    # Part 1
    start = start_node + (Dir.RIGHT, 1)
    # unvisited_nodes = [
    #     (0 if node == start else float("inf"), node)
    #     for node in itertools.product(range(H), range(W), dirs, range(3))
    # ]
    # heapq.heapify(unvisited_nodes)
    # shortest_path = defaultdict(lambda: float("inf"))
    # shortest_path[start] = 0
    # while unvisited_nodes:
    #     current_shortest_distance, current_node = heapq.heappop(unvisited_nodes)

    #     if current_shortest_distance <= shortest_path[current_node]:
    #         for neighbour in get_neighbors(current_node[:2]):
    #             x_n, y_n = neighbour
    #             diff = (x_n - current_node[0], y_n - current_node[1])
    #             dir_to_n = diff_to_dir[diff]
    #             dir_count_n = current_node[3] + 1 if dir_to_n == current_node[2] else 0
    #             neighbour_node = (x_n, y_n, dir_to_n, dir_count_n)
    #             distance = get_distance(current_node, neighbour_node)
    #             distance_through_current_node = shortest_path[current_node] + distance
    #             if distance_through_current_node < shortest_path[neighbour_node]:
    #                 shortest_path[neighbour_node] = distance_through_current_node
    #                 heapq.heappush(
    #                     unvisited_nodes, (distance_through_current_node, neighbour_node)
    #                 )
    # all_end_nodes = [node for node in shortest_path if node[:2] == end_node]
    # all_costs = [shortest_path[node] for node in all_end_nodes]
    # lowest_cost = min(all_costs)
    # result1 = lowest_cost
    # print(f"Part 1 {filename}: ", result1)

    # Part 2
    opposites = {
        Dir.UP: Dir.DOWN,
        Dir.DOWN: Dir.UP,
        Dir.LEFT: Dir.RIGHT,
        Dir.RIGHT: Dir.LEFT,
    }

    def get_distance2(node1, node2):
        if node1[3] < MIN_STRAIGHT2 and node1[2] != node2[2]:
            return float("inf")

        if opposites[node1[2]] == node2[2]:
            return float("inf")

        if node2[:2] == end_node and node2[3] < MIN_STRAIGHT2:
            return float("inf")

        if node2[3] > MAX_STRAIGHT2 or node1[3] > MAX_STRAIGHT2:
            return float("inf")

        return input_data_mat[node2[0]][node2[1]]

    start_nodes = [
        (0, 0, Dir.RIGHT, 1),
        (0, 0, Dir.DOWN, 1),
    ]
    lowest = float("inf")
    for start in start_nodes:
        unvisited_nodes = [(0, start)]

        heapq.heapify(unvisited_nodes)
        shortest_path = defaultdict(lambda: float("inf"))
        shortest_path[start] = 0
        connected_to = {}
        while unvisited_nodes:
            current_shortest_distance, current_node = heapq.heappop(unvisited_nodes)

            if current_shortest_distance <= shortest_path[current_node]:
                for neighbour in get_neighbors(current_node[:2]):
                    x_n, y_n = neighbour
                    diff = (x_n - current_node[0], y_n - current_node[1])
                    dir_to_n = diff_to_dir[diff]
                    dir_count_n = (
                        current_node[3] + 1 if dir_to_n == current_node[2] else 1
                    )
                    neighbour_node = (x_n, y_n, dir_to_n, dir_count_n)
                    distance = get_distance2(current_node, neighbour_node)
                    distance_through_current_node = (
                        shortest_path[current_node] + distance
                    )
                    if distance_through_current_node < shortest_path[neighbour_node]:
                        shortest_path[neighbour_node] = distance_through_current_node
                        heapq.heappush(
                            unvisited_nodes,
                            (distance_through_current_node, neighbour_node),
                        )
                        connected_to[neighbour_node] = current_node
        all_end_nodes = [node for node in shortest_path if node[:2] == end_node]
        all_costs = [shortest_path[node] for node in all_end_nodes]
        if not all_costs:
            continue

        lowest_cost = min(all_costs)
        end_node = next(
            node for node in all_end_nodes if shortest_path[node] == lowest_cost
        )
        path = [end_node]
        while path[0] in connected_to:
            path.insert(0, connected_to[path[0]])
        if lowest_cost < lowest:
            lowest = lowest_cost
            best_path = path
    result2 = lowest
    print(f"Part 2 {filename}: ", result2)
    result1 = 0
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (0, 94)
    assert main("input3.txt") == (0, 71)
    main("input.txt")
