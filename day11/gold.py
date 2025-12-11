import numpy as np
import sys


def main(input_file=None):
    day = 11
    intest = open(f"day{day:02d}/test_input_gold.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()
    incustom = open(input_file, "r").readlines() if input_file else None

    # Input mode
    input = inreal

    # Parse input into a dictionary, that maps each server name to [the number of requests its received so far, and the list of its own outputs]
    # For gold puzzle, the number of requests received so far is stored in an array in the following format: [neither dac nor fft, dac only, fft only, both dac & fft], so that we can keep track of requests that were redirected by each important server
    servers = dict([tuple([s if k == 0 else [np.array([0, 0, 0, 0]), s.split(" ")] for k, s in enumerate(line.strip().split(": "))]) for line in input])

    # Mark that we start by sending 1 request to the "svr" server (which obviously wasn't redirected by either "fft" nor "dac" yet)
    servers["svr"][0] = np.array([1, 0, 0, 0])
    # Create the "out" server that will just count requests and not redirect them
    servers["out"] = [np.array([0, 0, 0, 0]), []]

    
    # Create queue with starting server
    queue = ["svr"]
    while queue:  # Second wrapper while loop, so that we can refill the queue while there still are servers that have unsent requests
        while queue:  # Iterate while the queue isn't empty
            # Extract info about the current server
            cur_srv = queue.pop(0)
            cur_nbpaths, cur_outputs = servers[cur_srv]

            for output in cur_outputs:
                # It the current server is "dac" or "fft", mark and update received requests accordingly before redirecting them
                if cur_srv == "dac":
                    a, b, c, d = cur_nbpaths
                    cur_nbpaths = np.array([0, a+b, 0, c+d])
                elif cur_srv == "fft":
                    a, b, c, d = cur_nbpaths
                    cur_nbpaths = np.array([0, 0, a+c, b+d])

                # If the output server hasn't received any request yet, add it to the queue to visit it later
                if not servers[output][0].any():  # This condition ensures that each server is only added to the list once per "wrapper while loop" iteration
                    queue.append(output)
                # Transfer requests received so far to each server in the current server's output list
                servers[output][0] += cur_nbpaths
                servers[cur_srv][0] = np.array([0, 0, 0, 0])  # We need to clear the current server's unsent requests, now that we check them for the wrapper while loop

        # Refill the queue with servers that still have unsent requests (except the "out" server, which doesn't redirect requests)
        queue = [key for key, (nbpaths, _) in servers.items() if key != "out" and nbpaths.any()]

    print(servers["out"][0][-1])


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
