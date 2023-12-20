import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    input_data = [line.split(" -> ") for line in input_data if line]

    # Part 1
    components = {}
    for line in input_data:
        name, connected_to_str = line
        connected_to_nodes = connected_to_str.split(", ")
        for connection in connected_to_nodes:
            if connection not in components:
                components[connection] = {"type": "output", "connected_to": []}
        if name == "broadcaster":
            components[name] = {
                "type": "broadcaster",
                "connected_to": connected_to_nodes,
            }
        elif name.startswith("%"):
            components[name[1:]] = {
                "type": "flip-flop",
                "connected_to": connected_to_nodes,
                "state": "off",
            }
        elif name.startswith("&"):
            components[name[1:]] = {
                "type": "conjunction",
                "connected_to": connected_to_nodes,
            }
        else:
            raise ValueError(f"Unknown component type: {name}")
    inputs_to_conjunction = defaultdict(list)
    for name, component in components.items():
        if component["type"] == "output":
            continue
        for connected_to_name in component["connected_to"]:
            if components[connected_to_name]["type"] == "conjunction":
                inputs_to_conjunction[connected_to_name].append(name)
    for name, component in components.items():
        if component["type"] == "output":
            continue
        if component["type"] == "conjunction":
            component["inputs"] = inputs_to_conjunction[name]
            component["input_states"] = ["low"] * len(inputs_to_conjunction[name])

    PUSHES = 1000
    counter = {"low": 0, "high": 0}
    for _ in range(PUSHES):
        execute_all_pulses(components, counter)
    # %flip-flop: prefix %, starts off, low pulse flips, high pulse ignored, sends low when >off, sends high when >on
    # &conjunction: prefix &, remember type of last pulse of each input, start with low pulse memory,
    #   if all(high) for all inputs, send low, high otherwise
    # broadcast: sends what it received
    # button module:low pulse to broadcaster when pressed

    result1 = counter["low"] * counter["high"]
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    output_name = "rx"
    if output_name not in components:
        return result1, None

    node_to_rx = next(
        node for name, node in components.items() if output_name in node["connected_to"]
    )
    nodes_to_watch = node_to_rx["inputs"]

    # reset components
    counter = {"low": 0, "high": 0}
    for name, component in components.items():
        if component["type"] in ["broadcaster", "output"]:
            continue
        if component["type"] == "flip-flop":
            component["state"] = "off"
        elif component["type"] == "conjunction":
            component["input_states"] = ["low"] * len(component["inputs"])
        else:
            raise ValueError(f"Unknown component type: {name}")

    was_high_at_iter = [None] * len(nodes_to_watch)
    iter_count = 0
    while True:
        execute_all_pulses(components, counter)
        for i in range(len(nodes_to_watch)):
            node_name = nodes_to_watch[i]
            component = components[node_name]
            all_memories_high = all(
                state == "high" for state in component["input_states"]
            )
            if all_memories_high:
                if was_high_at_iter[i] is None:
                    was_high_at_iter[i] = iter_count
                else:
                    diff = iter_count - was_high_at_iter[i]
                    was_high_at_iter[i] = iter_count
                    print(f"Loop for {node_name}: {diff}")
                # if all(was_high_at_iter):
                #     print(f"this iteration: {iter_count}")
                # break
        # if all(was_high_at_iter):
        #     break
        iter_count += 1
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


def execute_all_pulses(components, counter):
    queue = [("broadcaster", "low", "button")]
    while queue:
        name, pulse, _from = queue.pop(0)
        # print(f"{_from} -{pulse}-> {name}")
        counter[pulse] += 1
        component = components[name]
        _type = component["type"]
        if _type == "output":
            continue
        if _type == "broadcaster":
            for other_name in component["connected_to"]:
                queue.append((other_name, pulse, name))
        elif _type == "flip-flop":
            if pulse == "low":
                component["state"] = "on" if component["state"] == "off" else "off"
                pulse_to_send = "low" if component["state"] == "off" else "high"
                for other_name in component["connected_to"]:
                    queue.append((other_name, pulse_to_send, name))
        elif _type == "conjunction":
            idx_of_input = component["inputs"].index(_from)
            component["input_states"][idx_of_input] = pulse
            if all(state == "high" for state in component["input_states"]):
                pulse_to_send = "low"
            else:
                pulse_to_send = "high"
            for other_name in component["connected_to"]:
                queue.append((other_name, pulse_to_send, name))
        else:
            raise ValueError(f"Unknown component type: {name}")


if __name__ == "__main__":
    assert main("input2.txt") == (32000000, None)
    assert main("input3.txt") == (11687500, None)
    main("input.txt")
