import re
import sys


def main(input_file=None):
    day = 5
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines() if input_file else None

    # Input mode
    input = inreal
    
    inlist = [line.strip() for line in input]
    # Keep only the fresh ranges ids now
    fresh_list = []
    seen_empty = False  # Separator
    for line in inlist:
        if not line:  # Triggered when we see empty line
            seen_empty = True
            continue
        
        if not seen_empty:  # Before empty line
            fresh_ids = re.findall("(.*)-(.*)", line)[0]  # Extract start and end of this range
            id_s, id_e = int(fresh_ids[0]), int(fresh_ids[1])  # Convert to int
            fresh_list.append((id_s, id_e))
        else:
            break  # Not interested in what's after empty line anymore
    
    # Sort list of ranges by start id
    fresh_list.sort(key=lambda ids: ids[0])

    res = 0
    cursor = 0  # Cursor cointaining at each end of iteration the maximum id + 1 (i.e., the smallest id that can be added after those we already have)
    for id_s, id_e in fresh_list:  # Iterate over the ranges of fresh ids
        res += max(id_e - max(cursor, id_s) + 1, 0)  # Compute number of new ids (see comments.md)
        cursor = max(cursor, id_e + 1)  # Update cursor

    print(res)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
