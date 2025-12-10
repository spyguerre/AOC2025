import sys


def main():
    day = 9
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    # Extract the list of coordinates of the red tiles
    red_tiles = [line.strip().split(",") for line in input]
    red_tiles = [(int(i), int(j)) for (i, j) in red_tiles]
    
    bestarea = 0  # The area of the best rectangle found
    bestcoos = []  # Best rectangle's two pairs of coordinates, unused but useful for debugging :)
    # Strict triangle iteration over the "pair of red tiles matrix"
    for a, (i1, j1) in enumerate(red_tiles):
        for b, (i2, j2) in enumerate(red_tiles):
            if a < b:  # Don't treat the same pair twice
                continue
            
            # Compute area
            area = (abs(i2-i1) + 1)*(abs(j2-j1) + 1)

            # Update best rectangle if the current one is larger
            if bestarea < area:
                bestarea = area
                bestcoos = [
                    (i1, j1),
                    (i2, j2)
                ]
    
    print(bestarea)
    # print(bestcoos)


if __name__ == "__main__":
    main()
