from collections import defaultdict
import itertools
import math

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}/input.txt", "r").read().split("\n")

instructions = input_data[0]

nodes_to_connections = {}
for line in input_data[2:]:
    name, connections = line.split(" = ")
    left, right = connections.strip("()").replace(" ", "").split(",")
    assert name not in nodes_to_connections
    nodes_to_connections[name] = (left, right)

# steps = 0
# node = "AAA"
# insts = itertools.cycle(instructions)
# while node != "ZZZ":
#     inst = next(insts)
#     if inst == "L":
#         node = nodes_to_connections[node][0]
#     else:
#         node = nodes_to_connections[node][1]
#     steps += 1
# print(steps)

# Part 2


# assert get_steps([3, 4], [0, 0], 3) == 12
# assert get_steps([3, 4], [1, 0], 3) == 0


steps = 0
nodes = [node for node in nodes_to_connections.keys() if node.endswith("A")]
insts = itertools.cycle(instructions)
visited_nodes = defaultdict(list)
loop_lengths = [0 for _ in nodes]
loop_indexes = [None for _ in nodes]
while not all(node.endswith("Z") for node in nodes):
    inst = next(insts)
    if inst == "L":
        selector = 0
    else:
        selector = 1
    for i, node in enumerate(nodes):
        this_visited_nodes = visited_nodes[i]
        nodes[i] = nodes_to_connections[node][selector]
        if loop_lengths[i]:
            loop_indexes[i] = (loop_indexes[i] + 1) % loop_lengths[i]
            continue
        if nodes[i].endswith("Z") and nodes[i] in this_visited_nodes:
            # adding nodes[i] means that two loops have been found
            index_of_node = this_visited_nodes.index(nodes[i])
            current_length = len(this_visited_nodes)
            loop_indexes[i] = 0
            loop_lengths[i] = current_length - index_of_node
            loop_nodes = this_visited_nodes[index_of_node:]
            count_of_z_nodes = sum(node.endswith("Z") for node in loop_nodes)
            assert count_of_z_nodes == 1
            assert loop_nodes[0] == nodes[i]
            continue
        this_visited_nodes.append(nodes[i])
    steps += 1
    if all(loop_lengths):
        break

max_value = math.lcm(*loop_lengths)
print(max_value)
