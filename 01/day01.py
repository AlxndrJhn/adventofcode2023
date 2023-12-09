import re

input_data = open("01/input.txt", "r").read().split("\n")
nums_as_str = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
replacements = {string: i for i, string in enumerate(nums_as_str, 1)}
summed = 0
for line in input_data:
    if not line:
        continue
    copy = line

    key_to_pos_left = {}
    for key_to_replace in replacements.keys():
        if key_to_replace in copy:
            key_to_pos_left[key_to_replace] = copy.find(key_to_replace)
    if key_to_pos_left:
        smallest_key = min(key_to_pos_left, key=lambda k: key_to_pos_left[k])
        copy = copy.replace(smallest_key, str(replacements[smallest_key]))

    key_to_pos_right = {}
    for key_to_replace in replacements.keys():
        if key_to_replace in copy:
            key_to_pos_right[key_to_replace] = max(
                [m.start() for m in re.finditer(key_to_replace, copy)]
            )
    if key_to_pos_right:
        largest_key = max(key_to_pos_right, key=lambda k: key_to_pos_right[k] + len(k))
        copy = copy.replace(largest_key, str(replacements[largest_key]))
    # if copy != line:
    #     print(line)
    digits = [int(d) for d in copy if d.isdigit()]
    first = digits[0]
    last = digits[-1]
    together = first * 10 + last
    summed += together
print(summed)

with open("01/input.txt") as f:
    print(
        sum(
            [
                int(v[0] + v[-1])
                for v in [d for d in [re.findall(f"(\d)", l) for l in f]]
            ]
        )
    )
with open("01/input.txt") as f:
    digits = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    print(
        sum(
            [
                int(digits.get(v[0], v[0]) + digits.get(v[-1], v[-1]))
                for v in [
                    re.findall(f"(?=(\d|{'|'.join(digits.keys())}))", l) for l in f
                ]
            ]
        )
    )
