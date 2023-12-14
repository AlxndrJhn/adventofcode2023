$todayAsNum = (Get-Date).ToString("dd")
# copy template to new folder
cp -r template "$todayAsNum"
code "$todayAsNum/day.py"
# fetch input from https://adventofcode.com/2023/day/9/input
code "$todayAsNum/input.txt"
code "$todayAsNum/input2.txt"

# open chrome browser
start chrome "https://adventofcode.com/2023/day/$todayAsNum"
start chrome "https://adventofcode.com/2023/day/$todayAsNum/input"
