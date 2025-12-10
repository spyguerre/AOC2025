import sys


# Iterates the list k_coos (made up of sorted integers and ranges), and returns the compressed index of the list to which an index k belongs
def compressed_coos(k_coos, k):
    for comp_index, index in enumerate(k_coos):
        # Case of a range of two integers; check if k is strictly between the two integers
        if type(index) is tuple:
            k1, k2 = index
            if k1 < k < k2:
                return comp_index
        # Case for a simple integer column; check if the integer is k
        else:
            if k == index:
                return comp_index


def main():
    day = 9
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    # Extract the list of coordinates of the red tiles
    red_tiles = [line.strip().split(",") for line in input]
    red_tiles = [(int(i), int(j)) for (i, j) in red_tiles]

    # Make a temporary list of all i and j coordinates, sorted and without duplicate
    temp_i_coos = sorted(list(set([c[0] for c in red_tiles])))
    temp_j_coos = sorted(list(set([c[1] for c in red_tiles])))

    # Init the actual list of the compressed matrix's i and j indices
    # Init with an element for padding, used to explore the graph on the sides later
    i_coos = [-1]
    j_coos = [-1]

    # Append an element per row of the compressed matrix, that reflect the coordinates of the actual map.
    # We append in turn the index of a red tile's y coordinate, and the range between the current red tile and the next one
    i2 = None
    for n in range(len(temp_i_coos) - 1):
        i1, i2 = temp_i_coos[n], temp_i_coos[n+1]
        i_coos.append(i1)
        i_coos.append((i1, i2))
    i_coos.append(i2)  # Don't forget the last row
    # Same for j indices
    j2 = None
    for n in range(len(temp_j_coos) - 1):
        j1, j2 = temp_j_coos[n], temp_j_coos[n+1]
        j_coos.append(j1)
        j_coos.append((j1, j2))
    j_coos.append(j2)  # Don't forget the last column

    # Append a last element for padding like earlier
    i_coos.append(sys.maxsize)
    j_coos.append(sys.maxsize)

    # Init the compressed matrix with the right size
    comp_matrix = [["." for _ in range(len(j_coos))] for _ in range(len(i_coos))]
    comp_matrix = Map2d(comp_matrix)

    # Set all red tiles in the compressed matrix
    for i, j in red_tiles:
        comp_matrix.set((compressed_coos(i_coos, i), compressed_coos(j_coos, j)), "#", 0)

    # Create a copy if the list and add duplicate the first element to the end, to handle looping around the points more easily
    red_tiles_looped = red_tiles.copy() + [red_tiles[0]]

    # Add vertical or horizontal chars to the map (instead of just the "X"s), where the green tiles between each pair of points are
    for k in range(len(red_tiles_looped)):
        if k == len(red_tiles_looped)-1:  # Last point is also the first one in this list, which we already treated
            break
        
        # Extract the coordinates from the list of red tiles
        i1, j1 = red_tiles_looped[k]
        i2, j2 = red_tiles_looped[k+1]

        # If the two points are connected by an horizontal line
        if i1 == i2:
            # Compute the line's indices in the compressed matrix
            i_comp = compressed_coos(i_coos, i1)
            j_min_comp = compressed_coos(j_coos, min(j1, j2))
            j_max_comp = compressed_coos(j_coos, max(j1, j2))

            # Only iterate strictly between the limits to avoid replacing the "#"s on either side
            for j_comp in range(j_min_comp+1, j_max_comp):
                comp_matrix.set((i_comp, j_comp), "|", 0)  # (We use "|" for horizontal lines since we print the transposed matrix for debugging today)

        # Else, the two points are connected by an vertical line
        else:
            # Compute the line's indices in the compressed matrix
            j_comp = compressed_coos(j_coos, j1)
            i_min_comp = compressed_coos(i_coos, min(i1, i2))
            i_max_comp = compressed_coos(i_coos, max(i1, i2))
            
            # Only iterate strictly between the limits to avoid replacing the "#"s on either side
            for i_comp in range(i_min_comp+1, i_max_comp):
                comp_matrix.set((i_comp, j_comp), "-", 0)  # (We use "-" for vertical lines since we print the transposed matrix for debugging today)

    # Run the graph exploration in the compressed matrix, starting at (0, 0) which we know is a tile on the outside (padding)
    comp_matrix.dijkstra(Map2d.d4, (0, 0))

    bestarea = 0  # The area of the best rectangle found
    bestcoos = None  # Best rectangle's two pairs of coordinates, unused but useful for debugging :)
    # Strict triangle iteration over the "pair of red tiles matrix"
    for a, (i1, j1) in enumerate(red_tiles):
        for b, (i2, j2) in enumerate(red_tiles):
            if a < b:  # Don't treat the same pair twice
                continue
            
            # Compute area
            area = (abs(i2-i1) + 1)*(abs(j2-j1) + 1)
            if not area > bestarea:  # If it isn't greater than the current best one, no need to investigate further
                continue
            
            # Compute the indices of the rectangle's red tile corners in the compressed matrix
            i1_comp, j1_comp = compressed_coos(i_coos, i1), compressed_coos(j_coos, j1)
            i2_comp, j2_comp = compressed_coos(i_coos, i2), compressed_coos(j_coos, j2)

            # Check that every tile in the compressed matrix (and thus, in the normal map) have not been explored by Dijkstra
            possible = True
            for i_comp in range(min(i1_comp, i2_comp), max(i1_comp, i2_comp)+1):
                for j_comp in range(min(j1_comp, j2_comp), max(j1_comp, j2_comp)+1):
                    if comp_matrix.get((i_comp, j_comp), 1) < sys.maxsize:  # Unexplored tiles are equal to sys.maxsize; we do want the unexplored, since we ran Dijkstra on the outside of the polygon formed by the input and stopped it from crossing the "#", "-" and "|"s.
                        possible = False
                        break
                if not possible:  # Give up faster on invalid rectangles
                    break
            if not possible:  # Skip invalid rectangles
                continue
            
            # And finally update the best area
            bestarea = area
            bestcoos = [
                (i1, j1),
                (i2, j2)
            ]
    print(bestarea)
    # print(bestcoos)
    # comp_matrix.print()  # I changed the print function for this problem only, to make it print the transposed matrix (since the coordinates are inverted in the subject...)


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
