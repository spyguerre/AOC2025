import re


def main():
    day = 6
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    inlist = [line.split("\n")[0] for line in input]  # Not clean without strip() I think, but we do need the spaces at the start and end this time D:

    # Retrieve the operations first, since nothing changed here
    ops = []
    line = inlist[len(inlist) - 1]
    ops = re.findall("([\\*\\+])", line)
    ops.reverse()  # Reverse it so that we can easily read from right to left later

    nbs = []  # A list that contains each problem's set of numbers (read vertically, and from right to left)
    pb = []  # Used only in the loop: the current problem's numbers parsed so far
    for j in range(len(inlist[0]) - 1, -1, -1):  # Iterate horizontally, from right to left
        cur = []  # The current number being parsed: for now, cur is a list of chars representing digits or spaces

        # Add all the digits that represent the current number
        for k in range(len(inlist) - 1):  # Iterate vertically, from top to bottom of number rows
            cur += inlist[k][j]

        # Remove spaces from the list to keep only the digits
        cur = [c for c in cur if c != " "]

        # If the current number's list is empty, it means we have reached the end of a problem
        if not cur:
            # If the list of numbers in the current problem is not empty, we register it to the list of problems
            if pb:
                nbs.append(pb)
                pb = []  # Then empty the current problem's list because we'll start a new one soon
        # Else the current number's list represents a number, so we add it to the current problem
        else:
            cur = "".join(cur)  # Convert it to a string
            cur = int(cur)  # Then to an integer
            pb.append(cur)
    # Add the last (= left-most) problem to the list of problems, since there is no extra space on the left of the inputs
    nbs.append(pb)

    # And finally compute the final result
    res = 0
    for k, pb in enumerate(nbs):  # Iterate over the problems, from right to left (if we compare it with the input)
        subres = 1 if ops[k] == "*" else 0  # Init subres as neutral value for the current operator

        # Compute subres according to the current operator
        for nb in pb:  # Iterate over each number in the problem
            if ops[k] == "*":
                subres *= nb
            else:
                subres += nb

        res += subres

    print(res)


if __name__ == "__main__":
    main()
