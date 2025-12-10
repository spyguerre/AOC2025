import re


def main():
    day = 10
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    # Parse the list of machines
    machines = [(
        # First component of each machine is the target light sequence, as a list of booleans 
        tuple([False if x == "." else True for x in re.findall("\\[(.*)\\]", line)[0]]),
        # Second component is the list of lightbulb indices that are changed, for each button (that I often named "actions" in my code)
        # We define an action as a couple that contains the list of changes to the lightbulbs at index 0, and the list which contains the indices of each button pressed at index 1
        [([int(x) for x in re.findall("\\d+", parenth)], [n]) for n, parenth in enumerate(re.findall("\\(\\S+\\)", line))]
    ) for line in input]

    res = 0
    for m in machines:  # Treat each machine individually
        goal = m[0]  # The target light sequence for this machine

        # Modify index 0 of each action for the current machine: transform the list of indices of lightbulbs, into the list of len(lightbulbs) booleans that represent whether the lightbulb at each index should or not change state
        actions = m[1]
        for i, action in enumerate(actions):
            buttons = action[0]
            but_press = action[1]

            # Init the action as if it changed no lightbulb
            but_res = [False for _ in range(len(m[0]))]
            for b in buttons:
                # Then swap the indices that are affected by the current action
                but_res[b] = not but_res[b]
            
            # Update the action tuple
            action = (tuple(but_res), tuple(but_press))  # action = ("result", "buttons")
            actions[i] = action

        # "Naïve" approach: explore the combinations of button presses
        discovering = True
        act_res_set = {action[0] for action in actions}  # Memoization of the result discovered
        subres = None  # Variable that we'll set as soon as we find the (optimal) solution in the loop to break out of loops quicker
        # While we're still discovering new results of combinations, keep iterating
        # Since we always explore the possibilities with the least amount of button presses first, it ensure we find the optimal solution first
        while discovering and not subres:
            discovering = False  # Set the flag to False not, and set it back to True later if we find a new result; in practice the other flag always exits the loop, but this one might come in handy to help debug cases of impossible machines

            l = len(actions)
            # Triangle iteration over the matrix of pairs of actions (only the ones that we already know)
            for i in range(l):
                for j in range(l):
                    # Triangle search to avoid computing duplicates
                    if j < i:  # Not the other way around, or else we could discover a version of a result that is not optimal
                        continue
                    
                    # Concatenate the list of button pressed
                    concat_press = list(actions[i][1]) + list(actions[j][1])
                    # And update the result of the new combination
                    but_res = list(actions[i][0])
                    for b, activation in enumerate(actions[j][0]):
                        if activation:
                            but_res[b] = not but_res[b]
                    
                    # If the action's result had not yet been found, update the list of known actions and the set of action results
                    action = (tuple(but_res), tuple(concat_press))
                    if action[0] not in act_res_set:
                        actions.append(action)
                        act_res_set.add(action[0])
                        discovering = True
                    
                        # Ultimately, since we find the target light sequence here before the end of the iteration, we can break to speed things up by quite a lot
                        if action[0] == goal:
                            subres = len(action[1])
                            break
                
                if subres:  # Break out faster
                    break
        
        # If we didn't find it while checking in the loop, it's because it was a single-button press (since we only set subres whenever we find a new action result)
        if not subres:
            subres = 1
        res += subres

    print(res)

if __name__ == "__main__":
    main()
