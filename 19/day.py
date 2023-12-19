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
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    assert main("input2.txt") == (19114, 167409079868000)
    main("input.txt")
