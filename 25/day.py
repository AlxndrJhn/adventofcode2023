from functools import lru_cache
import itertools
import os
import random
import re
from collections import defaultdict

from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")

    graph = defaultdict(int)
    for line in input_data:
        start, others_str = line.split(": ")
        others = others_str.split(" ")
        for other in others:
            s, e = get_sorted_nodes(start, other)
            graph[(s, e)] = 1

    # Part 1
    def kargers_algorithm(graph):
        copy = graph.copy()
        while len(copy) >= 2:
            total_edges = sum(copy.values())
            uniform_random = random.randint(0, total_edges - 1)

            # get edge that is at index uniform_random
            for edge, weight in copy.items():
                uniform_random -= weight
                if uniform_random <= 0:
                    break
            edge_to_destroy = edge
            start, end = edge_to_destroy
            new_node = f"{start}_{end}"
            copy.pop(edge_to_destroy)

            # reconnect edges
            for edge, weight in list(copy.items()):
                for node_to_destroy in edge_to_destroy:
                    if node_to_destroy in edge:
                        other = edge[1] if edge[0] == node_to_destroy else edge[0]
                        new_edge = get_sorted_nodes(new_node, other)
                        copy[new_edge] += weight
                        copy.pop(edge)

        # Return the number of edges between the two vertices
        return copy

    while True:
        two_node_graph = kargers_algorithm(graph)
        (group1, group2), connections = next(iter(two_node_graph.items()))
        if connections == 3:
            result1 = (group1.count("_") + 1) * (group2.count("_") + 1)
            break
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


def get_sorted_nodes(start, other):
    s, e = start, other
    if s > e:
        s, e = e, s
    return s, e


if __name__ == "__main__":
    assert main("input2.txt") == (54, 24)
    main("input.txt")
