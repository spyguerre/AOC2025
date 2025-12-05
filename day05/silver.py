import re


def main():
    day = 5
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal
    
    inlist = [line.strip() for line in input]

    # Split the list between ranges of fresh ids and available ids
    fresh_list, avail_ing = [], []
    seen_empty = False  # Separator
    for line in inlist:
        if not line:  # Triggered when we see empty line
            seen_empty = True
            continue
        
        if not seen_empty:  # Before empty line
            fresh_ids = re.findall("(.*)-(.*)", line)[0]  # Extract start and end of this range
            id_s, id_e = int(fresh_ids[0]), int(fresh_ids[1])  # Convert to int
            fresh_list.append((id_s, id_e))
        else:  # After empty line
            avail_ing.append(int(line))

    res = 0
    for id in avail_ing:  # Check available ingredients one by one
        for id_s, id_e in fresh_list:  # For each available ingredient, check if it is in any of the ranges
            if id_s <= id <= id_e:
                res += 1
                break  # Important to not count a id twice

    print(res)


if __name__ == "__main__":
    main()
