import sys


def main(input_file=None):
    day = 11
    intest = open(f"day{day:02d}/test_input_silver.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines()

    # Input mode
    input = inreal

    # Parse input into a dictionary, that maps each server name to [the number of requests its received so far, and the list of its own outputs]
    servers = dict([[s if k == 0 else [0, tuple(s.split(" "))] for k, s in enumerate(line.strip().split(": "))] for line in input])
    
    # Mark that we start by sending 1 request to the "you" server
    servers["you"][0] = 1
    # Create the "out" server that will just count requests and not redirect them
    servers["out"] = [0, []]

    # Create queue with starting server
    queue = ["you"]
    while queue:  # Iterate while the queue isn't empty
        # Extract info about the current server
        cur_srv = queue.pop(0)
        cur_nbpaths, cur_outputs = servers[cur_srv]

        for o in cur_outputs:
            # If the output server hasn't received any request yet, add it to the queue to visit it later
            if servers[o][0] == 0:  # This condition ensures that each server is only added to the list once
                queue.append(o)
            # Transfer requests received so far to each server in the current server's output list
            servers[o][0] += cur_nbpaths
    
    # Since the input graph is made so that a single queue iteration is enough for part 1, the out server now contains the count of all possible paths from "you" to "out"
    print(servers["out"][0])


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
