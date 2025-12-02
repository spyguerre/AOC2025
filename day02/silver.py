day = 2

input = open(f"day{day:02d}/input.txt", "r").readlines()[0].split(",")
inlist = [(int(line.split("-")[0]), int(line.split("-")[1])) for line in input]

res = 0
for s, e in inlist:  # Extract start and end
    for i in range(s, e+1):  # Loop over ints between s & e for each range
        str_ = str(i)
        l = len(str_)

        p1, p2 = str_[:l//2], str_[l//2:]  # Cut the string in half and extract part 1 and 2

        if p1 == p2:  # Check if they are the same
            res += i

print(res)
