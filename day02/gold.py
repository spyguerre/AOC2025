day = 2

input = open(f"day{day:02d}/input.txt", "r").readlines()[0].split(",")
inlist = [(int(line.split("-")[0]), int(line.split("-")[1])) for line in input]

res = 0
for s, e in inlist:  # Extract start and end
    for i in range(s, e+1):  # Loop over ints between s & e for each range
        str_ = str(i)
        l = len(str_)

        last_seen = "a"
        invalid = False
        for size in range(1, l//2+1):
            if l%size != 0:  # Ensure that size can divide number i's length -> Only a small optimization
                continue
            
            candidate = str_[0:size]  # Extract the candidate string for this size
            flag = True  # Flag to represent whether all the substrings checked so far are identical to candidate
            for k in range(l//size):
                ind = k*size
                if str_[ind : ind+size] != candidate:
                    flag = False
                    break

            if flag:  # If the flag is still true, the "invalid id condition" is respected for i
                invalid = True
                break

        if invalid:  # Increment result if i is invalid
            res += i

print(res)
