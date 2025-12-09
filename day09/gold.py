import math
import numpy as np
import sys
import re


def main():
    day = 9
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    inlist = [line.strip().split(",") for line in input]
    inlist = [(int(i), int(j)) for (i, j) in inlist]

    i_min = min(inlist, key=lambda x: x[0])[0]
    i_max = max(inlist, key=lambda x: x[0])[0]
    j_min = min(inlist, key=lambda x: x[1])[1]
    j_max = max(inlist, key=lambda x: x[1])[1]

    aug = []
    for k, (i1, j1) in enumerate(inlist):
        if k == len(inlist) - 1:
            break

        aug.append(inlist[k])
        aug.append((
            (inlist[k][0] + inlist[k+1][0]) // 2,
            (inlist[k][1] + inlist[k+1][1]) // 2
        ))
    l = len(inlist)
    aug.append(inlist[l-1])
    aug.append((
            (inlist[l-1][0] + inlist[0][0]) // 2,
            (inlist[l-1][1] + inlist[0][1]) // 2
    ))

    links = {}
    inlistcopy = inlist.copy()
    inlistcopy.append(inlist[0])
    for k, (i1, j1) in enumerate(inlistcopy):
        if k == len(inlistcopy) - 1:
            break
        
        i2, j2 = inlistcopy[k+1]

        if i1 == i2:
            if not i1 in links.keys():
                links[i1] = []
            
            if j1 < j2:
                links[i1].append([j1, j2-1])
            else:
                links[i1].append([j2, j1-1])

    bestcoos = []
    bestarea = 0
    for a, (i1, j1) in enumerate(inlist):
        for b, (i2, j2) in enumerate(inlist):
            if a <= b:
                continue
            
            area = abs(int(i2)-int(i1) + 1)*abs(int(j2)-int(j1) + 1)

            if not bestarea < area:
                continue

            possible = True
            for (i3, j3) in aug:
                if (i1 < i3 < i2 or i2 < i3 < i1) \
                and (j1 < j3 < j2 or j2 < j3 < j1):
                    possible = False
                    break
            if not possible:
                continue

            j_mid = (j1+j2) // 2
            i_mid = (i1+i2) // 2

            green = False
            for i in range(i_min, i_max):
                if i in links.keys():
                    for ran in links[i]:
                        if ran[0] <= j_mid <= ran[1]:
                            green = not green
                if i == i_mid:
                    possible = green
                    break
            
            # print((i1, j1), (i2, j2), possible)

            if not possible:
                continue
            
            if bestarea < area:
                bestarea = area
                bestcoos = [
                    (i1, j1),
                    (i2, j2)
                ]
    print(bestcoos)
    print(bestarea)


if __name__ == "__main__":
    main()
