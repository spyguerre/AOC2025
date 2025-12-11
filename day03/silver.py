import sys


day = 3

input_file = sys.argv[1] if len(sys.argv) > 1 else f"day{day:02d}/input.txt"

input = open(input_file, "r").readlines()

inlist = [line.strip() for line in input]

res = 0
for bank in inlist:  # Treat each line independantly
    
    greatest = 0  # Look for the greatest digit in the bank, that saves at least one space after it
    ind = 0  # Store its index here
    for i, battery in enumerate(bank):
        battery = int(battery)

        # Don't allow "greatest" to be the last number, since we need a 2-digits number and need it to be the tens digit
        if i == len(bank) - 1:
            continue

        if greatest < battery:  # Strict comparison here in order to let the maximum of possibilities later
            greatest = battery
            ind = i
    
    second = 0  # Look for the second greatest digit in the bank
    ind2 = 0  # Store its index here
    for i, battery in enumerate(bank):
        battery = int(battery)

        if i <= ind:  # Second greatest has to be after "greatest" in the bank
            continue

        if second < battery:
            second = battery
            ind2 = i

    res += greatest*10 + second  # Compute number and add it to the result

print(res)
