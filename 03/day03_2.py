import re


input_data_full = open("03/input.txt", "r").read().split("\n")
input_data = open("03/input.txt", "r").read().split("\n")
width = len(input_data[0])
neg_numb_pattern = "-\d+"
assert any(re.search(neg_numb_pattern, line) for line in input_data_full)
assert "*" not in input_data_full[0] and "*" not in input_data_full[-1]


def get_numbers_and_locs(line):
    numbers = []
    locs = []
    pattern = "-?\d+"
    for match in re.finditer(pattern, line):
        numbers.append(int(match.group()))
        locs.append(match.span())
    return numbers, locs


_sum = 0
for line_bef, line, line_after in zip(
    input_data[:-2], input_data[1:-1], input_data[2:]
):
    stars = [idx for idx, char in enumerate(line) if char == "*"]
    numbers_locs = [get_numbers_and_locs(li) for li in [line_bef, line, line_after]]
    for star_idx in stars:
        numbers_direct_proximity = []
        for numbers, locs in numbers_locs:
            for number, loc in zip(numbers, locs):
                if loc[0] - 1 <= star_idx <= loc[1]:
                    numbers_direct_proximity.append(number)
        if len(numbers_direct_proximity) == 2:
            _sum += numbers_direct_proximity[0] * numbers_direct_proximity[1]
print(_sum)
