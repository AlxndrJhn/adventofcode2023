from collections import defaultdict
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = [
    block.split()
    for block in open(f"{this_folder}/input.txt", "r").read().split("\n\n")
]


# Part 1
def get_reflections(block):
    hashes = []
    reflections = []
    for i in range(len(block)):
        hashes.append(hash(block[i]))

    # find idx in seen_rows where all elements afterwards appear reversed before idx
    for i in range(1, len(hashes)):
        after = hashes[i:]
        before_mirrored = hashes[:i][::-1]
        max_len = min(len(after), len(before_mirrored))
        if after[:max_len] == before_mirrored[:max_len]:
            reflections.append(i)
    assert len(reflections) <= 1
    return None if not reflections else reflections[0]


_sum = 0
for block in input_data:
    vertical_reflection = get_reflections(block)

    new_block = []
    for col_i in range(len(block[0])):
        col = "".join([row[col_i] for row in block])
        new_block.append(col)

    horizontal_reflection = get_reflections(new_block)

    assert vertical_reflection or horizontal_reflection, [print(line) for line in block]
    assert not (vertical_reflection and horizontal_reflection), [
        print(line) for line in block
    ]
    _sum += 100 * (vertical_reflection or 0) + (horizontal_reflection or 0)
print(_sum)
