# -*- coding: utf-8 -*-
import sys
from ruler import Ruler

DATASET = sys.argv[1]


with open("DATASET.txt", "r") as dataset:

    lines = dataset.readlines()

    nb_lines = len(lines)

    numero = 0

    for i in range(0, nb_lines, 2):

        numero += 1
        ruler = Ruler(lines[i].strip(), lines[i+1].strip())
        ruler.compute()
        top, bottom = ruler.report()
        print(f"====== example # {numero} -distance = {ruler.distance}")
        print(top)
        print(bottom)
