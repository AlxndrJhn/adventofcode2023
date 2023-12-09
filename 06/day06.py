import re
import tqdm

input_data = open("05/input.txt", "r").read().split("\n")


starting_speed = 0  # mm/s
speed_gain_per_ms = 1  # mm/s /ms

pattern_num = "\d+"

time_line = input_data[0].replace(" ", "")
dists_line = input_data[1].replace(" ", "")

times = [int(x) for x in re.findall(pattern_num, time_line)]
dists = [int(x) for x in re.findall(pattern_num, dists_line)]

product = 1
for time, record_dist in zip(times, dists):
    ways_to_beat_record = 0
    for t_hold in tqdm.tqdm(range(time + 1)):
        start_speed = starting_speed + speed_gain_per_ms * t_hold
        rest_time = time - t_hold
        dist_covered = start_speed * rest_time
        if dist_covered > record_dist:
            ways_to_beat_record += 1
    product *= ways_to_beat_record
print(product)
