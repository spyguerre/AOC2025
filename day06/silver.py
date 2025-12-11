import re
import sys


def main(input_file=None):
    day = 6
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines() if input_file else None

    # Input mode
    input = inreal

    inlist = [line.strip() for line in input]

    nbs = []  # A list containing the 3 or 4 lines of numbers as lists of integers
    ops = []  # The list of operations (+ or *) in the same order as the numbers
    for i, line in enumerate(inlist):
        if i == len(inlist) - 1:  # Treat the last line independantly for operations
            ops = re.findall("([\\*\\+])", line)
        else:
            nbs.append([int(match) for match in re.findall("(\\d+)", line)])

    res = 0
    for k, op in enumerate(ops):  # Iterate horizontally from left to right
        subres = 1 if op == "*" else 0  # Init subres as neutral value for the current operator
        
        # Compute subres according to the current operator
        for nb_line in nbs:  # Iterate over each line of numbers
            if op == "*":
                subres *= nb_line[k]
            else:
                subres += nb_line[k]
    
        res += subres
    
    print(res)


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
