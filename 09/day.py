from collections import defaultdict
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}\\input.txt", "r").read().split("\n")

# Each line in the report contains the history of a single value.
# prediction of the next value
# difference at each step
# If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.
# sum of extrapolated values

# Part 1
_sum = 0
for line in input_data:
    numbers = [int(n) for n in re.findall(r"-?\d+", line)]
    assert "." not in line and "," not in line
    # first derivative
    current_derivative = list(numbers)
    derivatives = [current_derivative]
    while not all(x == 0 for x in current_derivative):
        current_derivative = [
            current_derivative[i + 1] - current_derivative[i]
            for i in range(len(current_derivative) - 1)
        ]
        derivatives.append(current_derivative)

    # add zero to last derivative
    derivatives[-1].append(0)

    for i in range(len(derivatives) - 2, -1, -1):
        derivatives[i].append(derivatives[i + 1][-1] + derivatives[i][-1])
    extrapolated = derivatives[0][-1]
    _sum += extrapolated
print(_sum)

# Part 2
_sum = 0
for line in input_data:
    numbers = [int(n) for n in re.findall(r"-?\d+", line)]
    assert "." not in line and "," not in line
    # first derivative
    current_derivative = list(numbers)
    derivatives = [current_derivative]
    while not all(x == 0 for x in current_derivative):
        current_derivative = [
            current_derivative[i + 1] - current_derivative[i]
            for i in range(len(current_derivative) - 1)
        ]
        derivatives.append(current_derivative)

    # add zero to last derivative
    derivatives[-1].insert(0, 0)

    for i in range(len(derivatives) - 2, -1, -1):
        derivatives[i].insert(0, derivatives[i][0] - derivatives[i + 1][0])
    extrapolated = derivatives[0][0]
    _sum += extrapolated
print(_sum)
