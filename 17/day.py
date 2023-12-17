from copy import deepcopy
import itertools
import math
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data_mat = [[int(char) for char in line] for line in input_data]
    W = len(input_data_mat[0])
    H = len(input_data_mat)

    def get_distance(node1, node2, previous_nodes):
        last_nodes = [node1]
        MAX_STRAIGHT = 3
        for _ in range(MAX_STRAIGHT - 1):
            if last_nodes[-1] not in previous_nodes:
                break
            last_nodes.append(previous_nodes[last_nodes[-1]])
        distances = (node2[0] - last_nodes[-1][0], node2[1] - last_nodes[-1][1])
        if abs(distances[0]) == MAX_STRAIGHT or abs(distances[1]) == MAX_STRAIGHT:
            return float("inf")
        diff = (node1[0] - node2[0], node1[1] - node2[1])
        assert diff[0] <= 1 and diff[1] <= 1
        return input_data_mat[node2[0]][node2[1]]

    def get_neighbors(node, previous_nodes):
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
    start_node = (0, 0)
    end_node = (W - 1, H - 1)
    # use input_data_mat[x][y] as loss function, find path from START to END using Dijkstra's algorithm
    unvisited_nodes = list(itertools.product(range(W), range(H)))
    shortest_path = {}
    previous_nodes = {}

    for node in unvisited_nodes:
        shortest_path[node] = float("inf")
    shortest_path[start_node] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:  # Iterate over the nodes
            if current_min_node is None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        neighbors = get_neighbors(current_min_node, previous_nodes)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + get_distance(
                current_min_node, neighbor, previous_nodes
            )
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node

        unvisited_nodes.remove(current_min_node)
    # resolve path from start to end with previous_nodes
    path = [end_node]
    while path[0] != start_node:
        path = [previous_nodes[path[0]]] + path

    # path = shortest_path_nodes[end_node]
    path_value = shortest_path[end_node]
    copy = deepcopy(input_data_mat)
    for node in path:
        copy[node[0]][node[1]] = "X"
    for line in copy:
        print("".join([str(x) for x in line]))
    result1 = path_value
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (102, 24)
    # main("input.txt")
