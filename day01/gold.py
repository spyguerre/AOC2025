day = 1

input = open(f"day{day:02d}/input.txt", "r").readlines()

inmap = [[c for c in line.strip()] for line in input]
inlist = [(line.strip()[0], int(line.strip()[1:])) for line in input]

dial = 50
pw = 0

for line in inlist:
    old_dial = dial  # Save dial number before turning it

    step = line[1]

    if step >= 100:  # Increment password for steps over 100 individually and update step to 0-99 range
        time_0_seen = step // 100
        pw += time_0_seen
        step -= (time_0_seen) * 100

    if step == 0:  # Skip this step if step remains at 0 -> avoids counting the same 0 click twice when finishing n*100 inc/dec starting from 0
        dial = dial % 100
        continue
    
    # Move dial
    if line[0] == "L":
        dial -= step
    else:
        dial += step

    # Detect we moved through 0 if we have to update dial because of the wraparound
    # -> "and old_dial != 0" or else we also count a click if the previous position was 0 and we move the dial left
    # -> "or dial == 0" to also count the click when we stop right on 0 without crossing it towards left
    if dial != dial % 100 and old_dial != 0 or dial == 0:
        pw += 1
    
    dial = dial % 100  # Make sure to wrap around 0-100

print(pw)
