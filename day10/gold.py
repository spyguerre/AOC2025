import math
import numpy as np
import sys
import re


# Too expensive in time complexity, but I'll work on that another day :')
def main():
    day = 10
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    machines = [(
        tuple([int(x) for x in re.findall("\\d+", re.findall("\\{(.*)\\}", line)[0])]),
        [[int(x) for x in re.findall("\\d+", parenth)] for parenth in re.findall("\\(\\S+\\)", line)]
    ) for line in input]

    res = 0
    for m in machines:
        print(m)
        goal = m[0]

        actions = [(buttons, [n]) for n, buttons in enumerate(m[1])]
        for i, action in enumerate(actions):
            buttons = action[0]
            but_press = action[1]

            but_res = [0 for _ in range(len(m[0]))]
            for b in buttons:
                but_res[b] += 1
            
            action = (tuple(but_res), tuple(but_press))
            actions[i] = action

        discovering = True
        act_set = {action[0] for action in actions}
        while discovering:
            discovering = False
            l = len(actions)
            for i in range(l):
                for j in range(l):
                    concat_press = list(actions[i][1]) + list(actions[j][1])
                    but_res = list(actions[i][0])
                    for b, activation in enumerate(actions[j][0]):
                        but_res[b] += activation
                    
                    action = (tuple(but_res), tuple(concat_press))

                    valid = sum([action[0][b] > goal[b] for b in range(len(action[0]))]) == 0

                    if valid and action[0] not in act_set:
                        actions.append(action)
                        act_set.add(action[0])
                        discovering = True

        min_press = sys.maxsize
        for action in actions:
            if action[0] == goal and len(action[1]) < min_press:
                min_press = len(action[1])
        res += min_press

    print(res)

if __name__ == "__main__":
    main()
