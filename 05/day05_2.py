from collections import defaultdict
import re


input_data = open("05/input.txt", "r").read().split("\n")

seeds = [int(x) for x in re.findall("\d+", input_data[0])]
# split each 2 seeds into a pair
seed_pairs = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]

print_trajectory = True


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


def get_interval(key, mapping):
    for intervals, dst in mapping.items():
        if key < intervals[0]:
            continue
        if key > intervals[1]:
            continue
        return intervals, dst
    else:
        return (None, None), None


def get_next_interval(key, mapping):
    smallest_dist = float("inf")
    smallest_interval = None
    smallest_dst = None
    for intervals, dst in mapping.items():
        if key < intervals[0]:
            if intervals[0] - key < smallest_dist:
                smallest_dist = intervals[0] - key
                smallest_interval = intervals
                smallest_dst = dst
            continue
        if key > intervals[1]:
            continue
        raise Exception("This should not happen")
    return smallest_interval, smallest_dst


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
list_of_pairs = [list(x) for x in seed_pairs]

while stage != "location":
    target_map = [x for x in maps if x[0] == stage][0]
    _, next_stage = target_map

    new_list_of_pairs = []
    for idx, (start, _range) in enumerate(list_of_pairs):
        i = start
        while i < start + _range:
            rest_interval = _range - (i - start)
            (start_mapping, end_mapping), start_mapped = get_interval(
                i, maps[target_map]
            )
            if start_mapping is None:
                next_interval, next_dst = get_next_interval(i, maps[target_map])
                if next_interval is None:
                    new_list_of_pairs.append([i, rest_interval])
                    i += rest_interval
                    continue
                else:
                    interval = min(next_interval[0] - i, rest_interval)
                    new_list_of_pairs.append([i, interval])
                    i += interval
                    continue
            start_new_interval = max(start_mapping, i)
            end_new_interval = min(end_mapping, i + rest_interval - 1)
            new_range = end_new_interval - start_new_interval + 1

            mapped_start_new_interval = get_mapping(
                start_new_interval, maps[target_map]
            )
            new_list_of_pairs.append([mapped_start_new_interval, new_range])
            i += new_range

    stage = next_stage
    list_of_pairs = new_list_of_pairs


lowest = min(list_of_pairs, key=lambda x: x[0])[0]
print(lowest - 1)
