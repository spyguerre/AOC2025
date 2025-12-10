from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np
import re


def main():
    day = 10
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    machines = [(
        # First component of each machine is the target joltage sequence 
        tuple([int(x) for x in re.findall("\\d+", re.findall("\\{(.*)\\}", line)[0])]),
        # Second component is the list of lightbulb indices that are changed, for each button (that I often named "actions" in my code)
        # We define an action as a couple that contains the list of changes to the lightbulbs at index 0, and the list which contains the indices of each button pressed at index 1
        [([int(x) for x in re.findall("\\d+", parenth)], [n]) for n, parenth in enumerate(re.findall("\\(\\S+\\)", line))]
    ) for line in input]

    res = 0
    for m in machines:  # Treat each machine individually
        
        # Modify index 0 of each action for the current machine: transform the list of indices of lightbulbs, into the list of len(lightbulbs) booleans that represent whether the lightbulb at each index should or not change state
        actions = m[1]
        for i, action in enumerate(actions):
            buttons = action[0]
            but_press = action[1]

            # Init the action as if it changed no joltage integer
            but_res = [0 for _ in range(len(m[0]))]
            for b in buttons:
                # Replace value by 1 for the indices that are affected by the current action
                but_res[b] += 1
            
            # Update the action tuple
            action = (tuple(but_res), tuple(but_press))  # action = ("result", "buttons")
            actions[i] = action

        # Then, define variables to use with scipy and solve the Multi-Integer Linear Problem (MILP)

        # Number of variables in the linear problem (i.e. number of buttons)
        n = len(actions)

        # Goal for joltage values sequence
        g = np.array(m[0], dtype=int)

        # Compute the Button matrix formally
        B = np.array([action[0] for action in actions], dtype=int)
        B = B.transpose()
        
        # Instanciate the constraints formally: We need to solve lb <= A @ x <= up, so in our problem: B @ x = g
        constraints = LinearConstraint(A=B, lb=g, ub=g)

        # Init the bounds, since we only want positive button presses
        bounds = Bounds(lb=0, ub=np.inf)

        # Since we want to minimize the sum, set all the weights to 1 (all button presses have the same cost)
        w = np.array([1 for _ in range(n)])
        
        # Ensure we only work with integers
        integrality = [1 for _ in range(n)]

        # Use scipy to optimize the button presses (i.e. solve B @ x = g, with x being the smallest regarding the sum of its values)
        X = milp(c=w, constraints=constraints, bounds=bounds, integrality=integrality)

        # Append result of optimal list of button presses to final result
        res += int(sum(X.x))  # We convert it back to int, since scipy uses a float array even if we only use integer variables

    print(res)

if __name__ == "__main__":
    main()
