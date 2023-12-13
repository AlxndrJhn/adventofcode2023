from collections import defaultdict
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = [
    block.split()
    for block in open(f"{this_folder}/input4.txt", "r").read().split("\n\n")
]

# Part 1
# split at empty lines
_sum = 0
for block in input_data:
    seen_rows = []
    vertical_reflections = []
    for row_i in range(len(block)):
        row = block[row_i]
        hash_row = hash(row)
        if hash_row in seen_rows:
            dists = [
                len(seen_rows) - idx for idx, h in enumerate(seen_rows) if h == hash_row
            ]
            if any(dist == 1 for dist in dists):
                vertical_reflections.append(row_i)
            else:
                for vertical_reflection in list(vertical_reflections):
                    if not any(dist % 2 == 1 for dist in dists):
                        vertical_reflections.remove(vertical_reflection)
        else:
            for vertical_reflection in list(vertical_reflections):
                must_be_reflected = row_i - vertical_reflection < vertical_reflection
                if must_be_reflected:
                    vertical_reflections.remove(vertical_reflection)
                if vertical_reflection * 2 <= row_i:
                    vertical_reflections.remove(vertical_reflection)
        seen_rows.append(hash_row)
    known_cols = []
    horizontal_reflection = None
    for col_i in range(len(block[0])):
        col = "".join([row[col_i] for row in block])
        col_hash = hash(col)
        if col_hash in known_cols:
            dist = len(known_cols) - known_cols.index(col_hash)
            if dist == 1:
                horizontal_reflection = col_i
            elif dist % 2 != 1:
                horizontal_reflection = None
        elif horizontal_reflection:
            if horizontal_reflection * 2 <= col_i:
                horizontal_reflection = None
            else:
                pass
        known_cols.append(col_hash)
    assert vertical_reflection or horizontal_reflection, [print(line) for line in block]
    assert not (vertical_reflection and horizontal_reflection), [
        print(line) for line in block
    ]
    _sum += 100 * (vertical_reflection or 0) + (horizontal_reflection or 0)
print(_sum)
