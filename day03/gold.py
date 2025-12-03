day = 3
input = open(f"day{day:02d}/input.txt", "r").readlines()
inlist = [line.strip() for line in input]

nb = 12  # The number of batteries to allow per bank: 2 for silver or 12 for gold
res = 0
for bank in inlist:  # Treat each line independantly
    greatests = []  # Store here the list of selected digits, from most to least important
    last_ind = -1  # Store here the last greatest's index (init at -1 so we can start searching at index 0)

    for k in range(nb):  # Look for 12 digits, one at a time
        greatest = 0  # Look for the greatest digit in the bank, that saves at least nb-k-1 digits after it

        for i, battery in enumerate(bank):
            battery = int(battery)

            # Eliminate indices that are before the last selected digit's index, and the indices that don't save enough space after them for the rest of the next digits
            if i <= last_ind or len(bank) - (nb-k-1) <= i:
                continue
            
            if greatest < battery:  # Strict comparison here in order to let the maximum of possibilities later
                greatest = battery
                last_ind = i

        greatests.append(greatest)

    # Compute number and add it to the result
    res += sum([greatest * (10**(nb-1 - j)) for j, greatest in enumerate(greatests)])

print(res)
