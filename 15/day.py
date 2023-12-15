from collections import defaultdict
import os
import re

this_folder = "\\".join(__file__.split("\\")[:-1])

BOX_COUNT = 256


def get_hash(string):
    current_value = 0
    for char in string:
        ascii_value = ord(char)
        current_value += ascii_value
        current_value *= 17
        current_value %= BOX_COUNT
    return current_value


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split(",")
    # Part 1
    sum1 = 0
    for piece in input_data:
        sum1 += get_hash(piece)
    print(f"Part 1 {filename}: ", sum1)

    # Part 2
    boxes = defaultdict(list)
    for instruction in input_data:
        label, cmd, focal_length = re.split("([=-])", instruction)
        focal_length = int(focal_length) if focal_length else None
        box_num = get_hash(label)
        lense_obj = (label, focal_length)
        idx_to_replace = next(
            (idx for idx, obj in enumerate(boxes[box_num]) if obj[0] == label),
            None,
        )
        if cmd == "=":
            if idx_to_replace is not None:
                boxes[box_num][idx_to_replace] = lense_obj
            else:
                boxes[box_num].append(lense_obj)
        elif cmd == "-":
            if idx_to_replace is not None:
                boxes[box_num].pop(idx_to_replace)
    sum2 = 0
    for i in range(BOX_COUNT):
        for j, (label, focal_length) in enumerate(boxes[i]):
            sum2 += (i + 1) * (j + 1) * focal_length

    print(f"Part 2 {filename}: ", sum2)
    return sum1, sum2


if __name__ == "__main__":
    assert get_hash("HASH") == 52
    assert main("input2.txt") == (1320, 145)
    main("input.txt")
