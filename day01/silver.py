import sys


day = 1

input_file = sys.argv[1] if len(sys.argv) > 1 else f"day{day:02d}/input.txt"

input = open(input_file, "r").readlines()

inmap = [[c for c in line.strip()] for line in input]
inlist = [(line.strip()[0], int(line.strip()[1:])) for line in input]

dial = 50
pw = 0

for line in inlist:
    step = line[1]

    # Move dial
    if line[0] == "L":
        dial -= step
    else:
        dial += step

    dial = dial % 100  # Make sure to wrap around 0-100

    if dial == 0:  # Increment password when end dial is 0
        pw += 1

print(pw)
