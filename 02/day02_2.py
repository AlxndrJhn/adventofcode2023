input_data = open("02/input.txt", "r").read().split("\n")

# Game 44: 7 green, 5 red, 1 blue; 6 green, 1 blue, 5 red; 2 blue, 6 green; 3 green, 2 red; 4 green; 6 red
max_stones = {"red": 99, "green": 99, "blue": 99}

sum = 0
for line in input_data:
    game_id, game_rounds_str = line.split(":")
    game_id = game_id.split(" ")[1]
    game_rounds = game_rounds_str.split(";")

    is_valid = True
    max_stones_game = {"red": 0, "green": 0, "blue": 0}
    for round in game_rounds:
        stones = round.split(",")
        for stone in stones:
            number, color = stone.strip().split(" ")
            assert color in max_stones_game
            if int(number) > max_stones_game[color]:
                max_stones_game[color] = int(number)
    power = max_stones_game["red"] * max_stones_game["green"] * max_stones_game["blue"]
    sum += int(power)
print(sum)
