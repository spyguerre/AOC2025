import math
import numpy as np
import sys
import re


def sparse_coos(k_coos, k):
    for sparse_index, index in enumerate(k_coos):
        if type(index) is tuple:
            k1, k2 = index
            if k1 < k < k2:
                return sparse_index
        else:
            if k == index:
                return sparse_index


def main():
    day = 9
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    inlist = [line.strip().split(",") for line in input]
    inlist = [(int(i), int(j)) for (i, j) in inlist]

    # Make a list of all i coordinates
    temp_i_coos = list(set([c[0] for c in inlist]))
    temp_j_coos = list(set([c[1] for c in inlist]))
    temp_i_coos.sort()
    temp_j_coos.sort()

    i_coos = [-1]
    j_coos = [-1]

    i2 = None
    for n in range(len(temp_i_coos) - 1):
        i1, i2 = temp_i_coos[n], temp_i_coos[n+1]
        i_coos.append(i1)
        i_coos.append((i1, i2))
    i_coos.append(i2)
    j2 = None
    for n in range(len(temp_j_coos) - 1):
        j1, j2 = temp_j_coos[n], temp_j_coos[n+1]
        j_coos.append(j1)
        j_coos.append((j1, j2))
    j_coos.append(j2)

    i_coos.append(sys.maxsize)
    j_coos.append(sys.maxsize)

    inmap = [["." for _ in range(len(j_coos))] for _ in range(len(i_coos))]
    inmap = Map2d(inmap)

    for i, j in inlist:
        inmap.set((sparse_coos(i_coos, i), sparse_coos(j_coos, j)), "#", 0)

    inlistlooped = inlist.copy() + [inlist[0]]

    for k, (i1, j1) in enumerate(inlistlooped):
        if k == len(inlistlooped)-1:
            break

        i2, j2 = inlistlooped[k+1]

        if i1 == i2:
            i_sparse = sparse_coos(i_coos, i1)
            j_min_sparse = sparse_coos(j_coos, min(j1, j2))
            j_max_sparse = sparse_coos(j_coos, max(j1, j2))
            for j_sparse in range(j_min_sparse+1, j_max_sparse):
                inmap.set((i_sparse, j_sparse), "|", 0)
        else:
            j_sparse = sparse_coos(j_coos, j1)
            i_min_sparse = sparse_coos(i_coos, min(i1, i2))
            i_max_sparse = sparse_coos(i_coos, max(i1, i2))
            for i_sparse in range(i_min_sparse+1, i_max_sparse):
                inmap.set((i_sparse, j_sparse), "-", 0)

    inmap.dijkstra(Map2d.d4, (0, 0))

    bestcoos = None
    bestarea = 0
    for a, (i1, j1) in enumerate(inlist):
        for b, (i2, j2) in enumerate(inlist):
            if a < b:
                continue

            area = (abs(int(i2)-int(i1)) + 1)*(abs(int(j2)-int(j1)) + 1)
            if not area > bestarea:
                continue

            i1_sparse, j1_sparse = sparse_coos(i_coos, i1), sparse_coos(j_coos, j1)
            i2_sparse, j2_sparse = sparse_coos(i_coos, i2), sparse_coos(j_coos, j2)

            possible = True
            for i_sparse in range(min(i1_sparse, i2_sparse), max(i1_sparse, i2_sparse)+1):
                for j_sparse in range(min(j1_sparse, j2_sparse), max(j1_sparse, j2_sparse)+1):
                    if inmap.get((i_sparse, j_sparse), 1) < sys.maxsize:
                        possible = False
                        break
                if not possible:
                    break

            if not possible:
                continue
            
            if area > bestarea:
                bestarea = area
                bestcoos = [
                    (i1, j1),
                    (i2, j2)
                ]
    print(bestarea)
    print(bestcoos)
    # inmap.print()


# Utility class representing a 2D matrix
class Map2d():
    d4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    d8 = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def __init__(self, inmap):
        self.inmap = [[[value, sys.maxsize] for value in row] for row in inmap]

    # Returns the height of the input map
    def height(self):
        return len(self.inmap)
    
    # Returns the width of the input map
    def width(self):
        return len(self.inmap[0])

    # Returns whether the given coordinates are inside the map
    def coos_in_map(self, coos):
        return 0 <= coos[0] < self.height() and 0 <= coos[1] < self.width()

    # Getter for node (or index k of node if k!=None) at coordinates coos
    def get(self, coos, k=None):
        if k is not None:
            return self.inmap[coos[0]][coos[1]][k]
        else:
            return self.inmap[coos[0]][coos[1]]

    # Sets index i (or node if k=None) of cell at coordinates coos to input value (or node if k=None)
    def set(self, coos, value, k=None):
        if k is not None:
            self.inmap[coos[0]][coos[1]][k] = value
        else:
            self.inmap[coos[0]][coos[1]] = value

# Returns a flattened list of all the nodes in the map
    def iter(self):
        res = []
        for row in self.inmap:
            res.extend(row)
        return res

    # Returns the first occurence (in reading order) of a node containing a given value at index k
    def find_first(self, value, k=0):
        for i, row in enumerate(self.inmap):
            for j, node in enumerate(row):
                if node[k] == value:
                    return [i, j]

    # Returns the list of all occurences (in reading order) of nodes containing a given value at index k
    def find_all(self, value, k=0):
        res = []
        for i, row in enumerate(self.inmap):
            for j, node in enumerate(row):
                if node[k] == value:
                    res.append([i, j])
        return res

    # Resets indices > 1 of each node
    def reset(self):
        for row in self.inmap:
            for node in row:
                for k in range(len(node)):
                    if k == 0:
                        continue
                    elif k == 1:
                        node[k] = sys.maxsize
                    else:
                        node[k] = 0  # Reset other indices at 0 by default

    # Performs dijkstra's algorithm with allowed directions dirs and a given starting point start
    # Saves distance in each node at index 1
    def dijkstra(self, dirs, start):
        start_dist = 0  # Start distance definition
        self.set(start, start_dist, 1)
        file = [start]

        while file:
            pos = file.pop(0)
            cur_dist = self.get(pos, 1)

            for dir in dirs:
                new_coos = self.add_coos(pos, dir)

                if not self.coos_in_map(new_coos):  # Ensure new coos are inside the map
                    continue
                
                trans_cond = self.get(new_coos, 0) not in ["#", "-", "|"]  # Transition condition definition
                if self.get(new_coos, 1) == sys.maxsize and trans_cond:  # Ensure it is a new node
                    file.append(new_coos)  # Add node to discover

                    # Compute new distance
                    new_dist = cur_dist + 1  # Distance rule definition
                    self.set(new_coos, new_dist, 1)
    
    # Displays the map according to index k, with a min padding pad, and with col_str between columns
    def print(self, k=0, pad=0, col_str=""):
        for j in range(len(self.inmap[0])):
            prt_str = ""

            for i in range(len(self.inmap)):
                node = self.get((i, j))
                if j != 0:
                    prt_str += col_str
                
                prt_str += f"{str("inf" if type(node[k]) is int and node[k] == sys.maxsize else node[k]):>{pad}}"

            print(prt_str)

    # Adds two sets of coordinates and returns them
    @staticmethod
    def add_coos(coos1, coos2):
        return [coos1[i] + coos2[i] for i in range(min(len(coos1), len(coos2)))]

    # Returns a deep copy of a 2D list
    @staticmethod
    def deep_copy(inmap):
        return [[cell for cell in row] for row in inmap]


if __name__ == "__main__":
    main()
