import sys


day = 2

input_file = sys.argv[1] if len(sys.argv) > 1 else f"day{day:02d}/input.txt"

input = open(input_file, "r").readlines()[0].split(",")

inlist = [(int(range_.split("-")[0]), int(range_.split("-")[1])) for range_ in input]

res = 0
for s, e in inlist:  # Extract start and end
    for i in range(s, e+1):  # Loop over ints between s & e for each range
        str_ = str(i)
        l = len(str_)

        p1, p2 = str_[:l//2], str_[l//2:]  # Cut the string in half and extract part 1 and 2

        if p1 == p2:  # Check if they are the same
            res += i

print(res)
