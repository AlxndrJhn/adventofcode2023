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
    for name, component in components.items():
        component["name"] = name
    node_to_inputs = defaultdict(list)
    for name, component in components.items():
        if component["type"] == "output":
            continue
        for connected_to_name in component["connected_to"]:
            node_to_inputs[connected_to_name].append(name)
    for name, component in components.items():
        component["inputs"] = node_to_inputs[name]
        if component["type"] == "conjunction":
            component["input_states"] = ["low"] * len(node_to_inputs[name])

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
    rx_name = "rx"
    if rx_name not in components:
        return result1, None

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
