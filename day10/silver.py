import sys
import re


def main():
    day = 10
    intest = open(f"day{day:02d}/test_input.txt", "r").readlines()
    inreal = open(f"day{day:02d}/input.txt", "r").readlines()

    # Input mode
    input = inreal

    machines = [(
        tuple([False if x == "." else True for x in re.findall("\\[(.*)\\]", line)[0]]),
        [[int(x) for x in re.findall("\\d+", parenth)] for parenth in re.findall("\\(\\S+\\)", line)]
    ) for line in input]

    res = 0
    for m in machines:
        goal = m[0]

        actions = [(buttons, [n]) for n, buttons in enumerate(m[1])]
        for i, action in enumerate(actions):
            buttons = action[0]
            but_press = action[1]

            but_res = [False for _ in range(len(m[0]))]
            for b in buttons:
                but_res[b] = not but_res[b]
            
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
                        if activation:
                            but_res[b] = not but_res[b]
                    
                    action = (tuple(but_res), tuple(concat_press))
                    if action[0] not in act_set:
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
