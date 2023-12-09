import re


input_data = open("03/input.txt", "r").read().split("\n")
width = len(input_data[0])
# add line of dots to start and end
input_data = ["." * width] + input_data + ["." * width]
sum = 0
for line_before, line, line_after in zip(input_data, input_data[1:], input_data[2:]):
    pattern = "\d+"
    # if no number in line, skip
    if not re.search(pattern, line):
        continue
    # find all numbers in line, with index
    indexes, numbers = zip(
        *[(m.start(), m.group()) for m in re.finditer(pattern, line)]
    )

    for i, number in enumerate(numbers):
        start = max(0, indexes[i] - 1)
        end = min(width, indexes[i] + len(number) + 1)
        adjacent = line_before[start:end] + line[start:end] + line_after[start:end]
        symbols = [x for x in adjacent if not x.isdigit() and x != "."]
        if symbols:
            sum += int(number)
print(sum)
