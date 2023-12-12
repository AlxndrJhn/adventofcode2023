from collections import defaultdict
import re
import itertools
from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}/input.txt", "r").read().split("\n")

# part 1

_sum = 0
for line in tqdm(input_data):
    if not line:
        continue
    seq, groups_str = line.split(" ")
    indexes_of_qmark = [i for i, x in enumerate(seq) if x == "?"]
    len_of_groups = [int(x) for x in re.findall(r"\d+", groups_str)]
    options = [".", "#"]
    combs = list(itertools.product(options, repeat=len(indexes_of_qmark)))

    for combination in combs:
        new_line = seq
        for i, index in enumerate(indexes_of_qmark):
            new_line = new_line[:index] + combination[i] + new_line[index + 1 :]

        # count the length of each sequence of repeated characters
        groups_lengths = []
        for k, g in itertools.groupby(new_line):
            if k == "#":
                groups_lengths.append(len(list(g)))

        if groups_lengths == len_of_groups:
            _sum += 1
print(_sum)

