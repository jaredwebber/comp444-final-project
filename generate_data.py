from random import random

NUM_LINES = 5000
VARIATION = 6
NUM_POINTS = 722
INITIAL_DISTANCE = random() * 400

curr_dist = INITIAL_DISTANCE


def get_variation() -> int:
    return random() * VARIATION if random() < 0.5 else -random() * VARIATION


f = open("Project/test_data.txt", "w")

for i in range(1, NUM_LINES):
    f.write(f"{curr_dist}\n")
    curr_dist += get_variation()

f.close()
