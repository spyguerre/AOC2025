import sys


def main():
    day = 7
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    # Create map object
    inmap = [[c for c in line.strip()] for line in input]
    inmap = Map2d(inmap)

    # Assume start is always in the first row and look for start column
    s = inmap.find_first("S")  # Start coordinates

    for row in inmap.inmap:  # Init the index 1 of nodes at 0 (instead of maxint)
        for node in row:
            node[1] = 0
    inmap.set(s, 1, 1)  # Init index 1 of start at 1 (1 possible path at the start)

    queue = [s]  # Init a queue with starting position
    while queue:  # Iterate until queue is empty
        cur_coos = queue.pop(0)  # The coordinates of the current node

        next_coos = Map2d.add_coos(cur_coos, (1, 0))  # The node below the current node
        if not inmap.coos_in_map(next_coos):  # Skip cases where we reached the bottom end of the map
            continue
        
        # If the node below is a splitter
        if inmap.get(next_coos, 0) == "^":
            # Compute coordinates of node on the left and right of the splitter
            next_left = Map2d.add_coos(next_coos, [0, -1])
            next_right = Map2d.add_coos(next_coos, [0, 1])

            # Compute whether each node has already been marked
            seen_left = inmap.get(next_left, 0) == "|"
            seen_right = inmap.get(next_right, 0) == "|"
            seen_cur = inmap.get(cur_coos, 0) == "|"

            # If this is the first time going through this path
            if not seen_cur:
                # If nodes on the left/right of the splitter have not been and will not be treated according to our current state, add them to the queue (ensures we only treat each path once and avoid duplicates)
                if next_left not in queue and not seen_left:
                    queue.append(next_left)
                if next_right not in queue and not seen_right:
                    queue.append(next_right)

            # Update the count of available paths in index 1 of the nodes next to the splitter (i.e., what's currently in it + what's currently above the splitter)
            inmap.set(next_left, inmap.get(next_left, 1) + inmap.get(cur_coos, 1), 1)
            inmap.set(next_right, inmap.get(next_right, 1) + inmap.get(cur_coos, 1), 1)
        
        # Else propagate the beam, only on empty space
        elif inmap.get(next_coos, 0) == ".":
            # Compute whether the next node has already been marked
            seen_next = inmap.get(next_coos, 0) == "|"
            # If next node has not been and will not be treated according to our current state, add it to the queue (ensures we only treat each path once and avoid duplicates)
            if next_coos not in queue and not seen_next:
                queue.append(next_coos)
            # Update the count of available paths in index 1 of the next node (i.e., what's currently in it + what's currently above it)
            inmap.set(next_coos, inmap.get(cur_coos, 1) + inmap.get(next_coos, 1), 1)
        
        # Replace index 0 of the current node
        inmap.set(cur_coos, "|", 0)

    # And finally iterate over each node in the bottom row to find all the possible paths
    res = sum([node[1] for node in inmap.inmap[inmap.height() - 1]])
    print(res)


# Utility class representing a 2D matrix
class Map2d():
    d4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    d8 = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def __init__(self, inmap):
        self.inmap = [[[value, sys.maxsize] for value in row] for row in inmap]

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
    main()
