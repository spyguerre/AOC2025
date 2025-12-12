import numpy as np
import sys
import re


def main(input_file=None):
    day = 12
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines() if input_file else None

    # Input mode
    input = inreal

    inlist = [line.strip() for line in input]

    # Parse the shapes and regions
    input_shapes = []
    cur_shape = [-1, []]  # Since shapes are written on multiple lines, store the one currently being parsed here
    regions = []
    for line in inlist:
        # Try to match a region
        match = re.match(r"^(\d+)x(\d+): ([\d ]+)$", line)
        if match:  # If line represents a region
            # Extract all numbers and convert them to integers like so for now: [[n], [p], [count1, count2, ..., countp]]
            region = [[int(k) for k in group.split(" ")] for group in match.groups()]
            # Save the region in the list with a better structure: (n, p, array(count1, count2, ..., countp))
            regions.append(((region[0][0], region[1][0]), np.array(region[2])))
            continue
        
        # Else, check if the line is empty, and that we are currently parsing a present shape
        if not line and cur_shape[0] != -1:
            # The shape that we were currently parsing is done, so we add it to the list
            input_shapes.append(cur_shape)
            # Then reset the current shape
            cur_shape = [-1, []]
            continue
        
        # Else, check if the line is an index of present shape
        match = re.match(r"^(\d+):$", line)
        if match:  # Line represents the index of a present shape
            # Extract it set it as the current shape's index
            cur_shape[0] = int(match.groups()[0])
            continue
        
        # Else, check if the line represents part of a present shape
        match = re.match(r"^([#\.]+)$", line)
        if match:  # The line is part of a present shape
            # Convert the line to a list of ones and zeros
            line_shape = [1 if c == "#" else 0 for c in match.groups()[0]]
            # Append the line to the matrix we're currently parsing
            cur_shape[1].append(line_shape)

    # Compute the array of the number of tiles taken by each present shape
    counts = np.array([sum([sum(row) for row in shape[1]]) for shape in input_shapes])

    # Iterate over each region
    res = 0
    for region in regions:
        # Add 1 to the result each time we encounter a region that has enough space to fit all the presents
        res += region[1] @ counts <= region[0][0]*region[0][1]
    print(res)

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
