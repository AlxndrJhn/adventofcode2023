from collections import defaultdict
import re


input_data = open("05/input.txt", "r").read().split("\n")

seeds = [int(x) for x in re.findall("\d+", input_data[0])]

print_trajectory = False


def get_mapping(key, mapping):
    for intervals, dst in mapping.items():
        if key < intervals[0]:
            continue
        if key > intervals[1]:
            continue
        offset = key - intervals[0]
        return dst + offset
    else:
        return key


maps = defaultdict(dict)  # type: ignore
for line in input_data[1:]:
    if line == "":
        continue

    if "map" in line:
        first_part = line.split(" ")[0]
        _from, to = first_part.split("-to-")
        continue

    dst, src, _range = [int(x) for x in re.findall("\d+", line)]
    maps[(_from, to)][(src, src + _range)] = dst

stage = "seed"
list_of_ids = list(seeds)

trajectory = [""] * len(list_of_ids)
while stage != "location":
    target_map = [x for x in maps if x[0] == stage]
    new_list_of_ids = []
    for idx, before in enumerate(list_of_ids):
        assert len(target_map) == 1
        _, next_stage = target_map[0]
        after = get_mapping(before, maps[target_map[0]])
        if print_trajectory:
            trajectory[idx] += f"{stage} {before}, "
        new_list_of_ids.append(after)
    stage = next_stage
    list_of_ids = new_list_of_ids

if print_trajectory:
    for traj in trajectory:
        print(traj.strip(", "))

lowest = min(list_of_ids)
print(lowest)
