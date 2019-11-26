#!/usr/bin/python3

import sys
import numpy
import solver

class Reader:

    def read_area(self, filename):
        result = numpy.genfromtxt(filename, delimiter = " ", dtype = (numpy.int32, numpy.int32))

        if len(result.shape) == 1:
            result = numpy.array([result])

        return result

class Formatter:

    def print_area(self, area, graphical):
        if graphical:
            for row in area:
                for value in row:
                    color = ""
                    field = "█"

                    if value == 0:
                        field = " "
                    elif value == 1:
                        color = ""
                    else:
                        color = "31"

                    self.print(field + field, color, end = "")
                    
                print("")
        else:
            for row in area:
                print(" ".join(map(str, row)))

    def print_path(self, path):
        result = []

        for action in path:
            name = ""

            if action[1] == 1:
                name = "go"
            elif action[0] == -1:
                name = "left"
            elif action[0] == 1:
                name = "right"
            elif action[0] == 2:
                name = "back"

            if result and result[-1][0] == name:
                result[-1][1] += 1
            else:
                result.append([name, 1])

        result = map(lambda item: item[0] if item[1] == 1 else str(item[1]) + "x " + item[0], result)
        result = ", ".join(result)

        print(result)

    def merge(self, area, path):
        result = numpy.copy(area)
        current = solver.Array.find(result, 2)
        current = [current[0], current[1], 0]

        for action in path:
            current = solver.State.apply_action(area, current, action)
            result[(current[0], current[1])] = 4

        return result

    def print(self, content, color, end = "\n"):
        if "win" in sys.platform: # There is no support for colors in Windows CMD.
            print("▓▓" if color == "31" else content, end = end)
        else:
            print("\033[" + color + "m", content, "\033[0m", sep = "", end = end)