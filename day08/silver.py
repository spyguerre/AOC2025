import math
import numpy as np
import sys
import re


def main(input_file=None):
    day = 8
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines()

    # Input mode
    input = inreal
    n_con = 1000 if input == incustom or input == inreal else 10  # Number of connections to make

    # Preprocess the input into a list of coordinates
    boxes = [re.findall("(\\d+)", line.strip()) for line in input]
    boxes = [[int(nb) for nb in row] for row in boxes]

    # Create a list of all possible connections by doing triangle iteration on boxes matrix
    connections = []
    for i, (x1, y1, z1) in enumerate(boxes):
        for j, (x2, y2, z2) in enumerate(boxes):
            if i >= j:
                continue
            dist = math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2 + abs(z2-z1)**2)  # Euclidian distance 3D
            connections.append([(x1, y1, z1), (x2, y2, z2), dist])
    # Sort the list of possible connections from shortest to longest distance
    connections.sort(key=lambda con: con[2])
    # Only keep the n_con first connections (10 or 1000 depending on the input mode)
    connections = connections[:n_con]

    # Dict to map a circuit id to the list of its boxes
    circuits = {}  # key = id | value = list of coordinates
    # A second dict to map a box's coordinates to its circuit id, which serves as an inverted index
    boxmap = {}  # key = coordinates | value = circuit id

    # Update the two dicts by running the n_con first connections
    max_cid = 0  # Counter for the greatest assigned circuit id
    for c1, c2, _ in connections:  # Iterate over the connections
        # Check whether both sets of coordinates whether they are already associated with a circuit id
        seen_c1 = c1 in boxmap.keys()
        seen_c2 = c2 in boxmap.keys()

        # Both boxes are already in a circuit
        if seen_c1 and seen_c2:
            # Fetch each box's circuit id
            c1_cid = boxmap[c1]
            c2_cid = boxmap[c2]

            # If the circuits are different, link them together
            if c1_cid != c2_cid:
                circuits[c1_cid].extend(circuits[c2_cid])  # Add all the boxes of circuit c2_cid to circuit c1_cid
                while circuits[c2_cid]:
                    c = circuits[c2_cid].pop()  # Gradually extract the coordinates from circuit c2_cid
                    boxmap[c] = c1_cid  # And update the reverse index
                circuits.pop(c2_cid)  # Remove circuit c2_cid from the circuits map

        # If c1 is in a circuit and c2 isn't, we add c2 to c1's circuit
        elif seen_c1:
            circuit_id = boxmap[c1]  # Fetch c1's circuit id
            circuits[circuit_id].append(c2)  # Add c2 to c1's circuit
            boxmap[c2] = circuit_id  # And update the reverse index

        # The other way around; if c2 is in a circuit and c1 isn't, we add c1 to c2's circuit
        elif seen_c2:
            circuit_id = boxmap[c2]  # Fetch c2's circuit id
            circuits[circuit_id].append(c1)  # Add c1 to c2's circuit
            boxmap[c1] = circuit_id  # And update the reverse index

        # Else, both boxes are not in any circuit, so we create a circuit with only 2 boxes
        else:
            max_cid += 1  # Increment the greatest assigned circuit id
            circuits[max_cid] = [c1, c2]  # Init the circuit in the dict
            boxmap[c1], boxmap [c2] = max_cid, max_cid  # And update the reverse index
    
    # Extract the list of sizes of each circuit after the partial iteration is complete
    sizes = [len(cir[1]) for cir in circuits.items()]
    sizes.sort(reverse=True)  # Sort with greatest sizes first

    # And finally multiply the first three sizes together
    res = sizes[0] * sizes[1] * sizes[2]

    print(res)


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
                
                trans_cond = self.get(new_coos, 0) != "#"  # Transition condition definition
                if self.get(new_coos, 1) == sys.maxsize and trans_cond:  # Ensure it is a new node
                    file.append(new_coos)  # Add node to discover

                    # Compute new distance
                    new_dist = cur_dist + 1  # Distance rule definition
                    self.set(new_coos, new_dist, 1)
    
    # Displays the map according to index k, with a min padding pad, and with col_str between columns
    def print(self, k=0, pad=0, col_str=""):
        for row in self.inmap:
            prt_str = ""

            for j, node in enumerate(row):
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
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
