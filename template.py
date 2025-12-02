import math
import numpy as np


day = 0

input = open(f"day{day:02d}/input.txt", "r").readlines()

inmap = [[c for c in line.strip()] for line in input]
inlist = ["" for line in input]
