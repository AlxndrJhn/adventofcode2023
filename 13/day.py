import itertools

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = [
    block.split()
    for block in open(f"{this_folder}/input.txt", "r").read().split("\n\n")
]


# Part 1
def get_single_reflection(block):
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
    vertical_reflection = get_single_reflection(block)

    new_block = []
    for col_i in range(len(block[0])):
        col = "".join([row[col_i] for row in block])
        new_block.append(col)

    horizontal_reflection = get_single_reflection(new_block)

    assert vertical_reflection or horizontal_reflection, [print(line) for line in block]
    assert not (vertical_reflection and horizontal_reflection), [
        print(line) for line in block
    ]
    _sum += 100 * (vertical_reflection or 0) + (horizontal_reflection or 0)
print(_sum)


# Part 2
def get_all_reflections(block):
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
    return reflections


def get_clean_reflection_idx(block):
    old_vert_reflec = get_all_reflections(block)
    for x, y in itertools.product(range(len(block)), range(len(block[0]))):
        copied = [row[:] for row in block]
        toggled_char = "#" if copied[x][y] == "." else "."
        copied[x] = copied[x][:y] + toggled_char + copied[x][y + 1 :]
        new_reflecs = get_all_reflections(copied)
        if old_vert_reflec and old_vert_reflec[0] in new_reflecs:
            new_reflecs.remove(old_vert_reflec[0])
        if new_reflecs:
            reflec_idx = new_reflecs[0]
            reflected_range = min(len(block) - reflec_idx, reflec_idx)
            if reflec_idx - reflected_range <= x < reflec_idx + reflected_range:
                assert len(new_reflecs) == 1
                return new_reflecs[0]
    return None


_sum = 0
for block in input_data:
    vertical_reflection = get_clean_reflection_idx(block)

    horizontal_reflection = None
    if vertical_reflection is None:
        new_block = []
        for col_i in range(len(block[0])):
            col = "".join([row[col_i] for row in block])
            new_block.append(col)

        horizontal_reflection = get_clean_reflection_idx(new_block)

    assert vertical_reflection or horizontal_reflection, [print(line) for line in block]
    assert not (vertical_reflection and horizontal_reflection), [
        print(line) for line in block
    ]

    _sum += 100 * (vertical_reflection or 0) + (horizontal_reflection or 0)
print(_sum)
