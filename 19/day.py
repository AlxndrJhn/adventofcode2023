from copy import deepcopy
import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])

REJECT = "R"
ACCEPT = "A"

GT = ">"
LT = "<"


def main(filename):
    workflows_str, ratings_str = (
        open(f"{this_folder}/{filename}", "r").read().split("\n\n")
    )
    workflows = {}
    for line in workflows_str.split("\n"):
        # parse "qqz{s>2770:qs,m<1801:hdj,R}" into dict

        name = line.split("{")[0]
        conditions_groups = line.split("{")[1].split("}")[0].split(",")
        default = conditions_groups.pop(-1)
        conditions = []
        for condition_group in conditions_groups:
            rgx = r"([xmas])([<>])(\d+):([A-Za-z]+)"
            var, op, val_str, _next = re.match(rgx, condition_group).groups()
            condition = {
                "var": var,
                "op": op,
                "val": int(val_str),
                "next": _next,
            }
            conditions.append(condition)

        workflows[name] = {"conditions": conditions, "default": default}

    _sum = 0

    for line in ratings_str.split("\n"):
        # parse "{x=787,m=2655,a=1222,s=2876}" into a dict
        if not line:
            continue
        rating = {k: int(v) for k, v in re.findall(r"([a-z])=(\d+)", line)}

        current_workflow = "in"
        workflows_traj = []
        while True:
            workflows_traj += [current_workflow]
            if current_workflow == REJECT:
                break
            if current_workflow == ACCEPT:
                break
            workflow = workflows[current_workflow]
            for condition in workflow["conditions"]:
                if condition["op"] == GT:
                    if rating[condition["var"]] > int(condition["val"]):
                        current_workflow = condition["next"]
                        break
                elif condition["op"] == LT:
                    if rating[condition["var"]] < int(condition["val"]):
                        current_workflow = condition["next"]
                        break
                else:
                    raise Exception(f"Unknown operator {condition['op']}")
            else:
                current_workflow = workflow["default"]

        if current_workflow == ACCEPT:
            _sum += sum(rating.values())
        print(f"{rating}: {' -> '.join(workflows_traj)}")
    # Part 1
    result1 = _sum
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    def get_default_interval():
        # including start, excluding endw
        return (1, 4000 + 1)

    # workflow, x, m, a, s
    interval_queue = [
        (
            "in",
            get_default_interval(),
            get_default_interval(),
            get_default_interval(),
            get_default_interval(),
            [None],
        ),
    ]
    combis = 0
    name_to_interval = {
        "x": 0,
        "m": 1,
        "a": 2,
        "s": 3,
    }
    while interval_queue:
        wf_name, *intervals, path = interval_queue.pop(0)
        path = path + [wf_name]
        for lower, upper in intervals:
            span = upper - lower
            assert span > 1
        if wf_name == REJECT:
            continue
        if wf_name == ACCEPT:
            product = 1
            for lower, upper in intervals:
                product *= upper - lower
            combis += product
            continue
        workflow = workflows[wf_name]
        for condition in workflow["conditions"]:
            idx_interval = name_to_interval[condition["var"]]
            interval_to_check = intervals[idx_interval]
            if condition["op"] == GT:
                if interval_to_check[1] - 1 > condition["val"]:
                    copied_intervals = deepcopy(intervals)
                    new_interval1 = (condition["val"] + 1, interval_to_check[1])
                    copied_intervals[idx_interval] = new_interval1
                    interval_queue.append((condition["next"], *copied_intervals, path))

                    new_interval2 = (interval_to_check[0], condition["val"] + 1)
                    intervals[idx_interval] = new_interval2
            elif condition["op"] == LT:
                if interval_to_check[0] < condition["val"]:
                    copied_intervals = deepcopy(intervals)
                    new_interval1 = (interval_to_check[0], condition["val"])
                    copied_intervals[idx_interval] = new_interval1
                    interval_queue.append((condition["next"], *copied_intervals, path))

                    new_interval2 = (condition["val"], interval_to_check[1])
                    intervals[idx_interval] = new_interval2

            else:
                raise Exception(f"Unknown operator {condition['op']}")
        copied_intervals = deepcopy(intervals)
        interval_queue.append((workflow["default"], *copied_intervals, path))

    result2 = combis
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (19114, 167409079868000)
    main("input.txt")
