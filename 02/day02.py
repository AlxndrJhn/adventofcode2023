input_data = open("02/input.txt", "r").read().split("\n")

# Game 44: 7 green, 5 red, 1 blue; 6 green, 1 blue, 5 red; 2 blue, 6 green; 3 green, 2 red; 4 green; 6 red
max_stones = {"red": 12, "green": 13, "blue": 14}

sum = 0
for line in input_data:
    game_id, game_rounds_str = line.split(":")
    game_id = game_id.split(" ")[1]
    game_rounds = game_rounds_str.split(";")

    is_valid = True
    for round in game_rounds:
        stones = round.split(",")
        for stone in stones:
            number, color = stone.strip().split(" ")
            assert color in max_stones
            if int(number) > max_stones[color]:
                is_valid = False
                break
        if not is_valid:
            break

    if not is_valid:
        continue

    sum += int(game_id)
print(sum)
