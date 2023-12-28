# if the first argument is a number, use that as the day number, with leading 0
# otherwise, use today's date
if ($args[0] -match "^\d+$") {
    $todayAsNum = $args[0].ToString().PadLeft(2, '0')
}
else {
    $todayAsNum = (Get-Date).ToString("dd")
}

# copy template to new folder
cp -r template "$todayAsNum"
code "$todayAsNum/day.py"
# fetch input from https://adventofcode.com/2023/day/9/input
code "$todayAsNum/input.txt"
code "$todayAsNum/input2.txt"

# open chrome browser
start chrome "https://adventofcode.com/2023/day/$todayAsNum"
start chrome "https://adventofcode.com/2023/day/$todayAsNum/input"
