import math
import re
import sys


def main(input_file=None):
    day = 8
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines() if input_file else None

    # Input mode
    input = inreal

    # Preprocess the input into a list of coordinates
    boxes = [re.findall("(\\d+)", line.strip()) for line in input]
    boxes = [[int(nb) for nb in row] for row in boxes]
    box_count = len(boxes)

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

    # Dict to map a circuit id to the list of its boxes
    circuits = {}  # key = id | value = list of coordinates
    # A second dict to map a box's coordinates to its circuit id, which serves as an inverted index
    boxmap = {}  # key = coordinates | value = circuit id

    # Update the two dicts by running the n_con first connections
    max_cid = 0  # Counter for the greatest assigned circuit id
    bc1, bc2 = None, None  # Variables that will hold the coordinates of the last two boxes when we break the loop
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

        # If we have all the boxes in one big circuit, save the coordinates of the last two boxes to connect and break the loop
        if circuits.items() and len(list(circuits.items())[0][1]) == box_count:
            bc1, bc2 = c1, c2
            break

    # And finally multiply the X coordinates of the last two boxes to connect :)
    print(bc1[0] * bc2[0])


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
