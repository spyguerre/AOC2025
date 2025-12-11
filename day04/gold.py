import sys


def main(input_file=None):
    day = 4
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines()

    # Input mode
    input = inreal

    # Load map input
    inmap = [[c for c in line.strip()] for line in input]
    inmap = Map2d(inmap)

    res = 0
    last_changes_count = None
    # Continue while we keep removing paper rolls
    while last_changes_count != 0:
        changes_count = 0  # Count the total number of paper rolls removed this iteration
        # Iterate over the nodes of the map
        for i, line in enumerate(inmap.inmap):
            for j, c in enumerate(line):
                # Only treat nodes that are paper rolls
                if c[0] == "@":
                    count = 0    # Count the adjacent nodes that are paper rolls
                    for dir in Map2d.d8:
                        new_coos = Map2d.add_coos([i, j], dir)
                        # Ensure nearby coordinates are in the map then check that they correspond to another paper roll
                        if inmap.coos_in_map(new_coos) and inmap.get(new_coos, 0) == "@":
                            count += 1
                
                    # Increment the result and changes count the paper roll is removable, and removes the paper roll
                    if count < 4:
                        res += 1
                        changes_count += 1
                        inmap.set([i, j], ".", 0)

        # Update this iteration's changes count
        last_changes_count = changes_count
        
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
