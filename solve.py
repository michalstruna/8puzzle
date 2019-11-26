#!/usr/bin/python3

import argparse
import time
import sys
import numpy

import io_utils
import solver

start = time.time()

# Parse arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stats", help = "show also statistics", action = "store_true")
parser.add_argument("-p", "--plain", help = "print raw maze instead of graphical version", action = "store_true")
parser.add_argument("-i", "--input", help = "specify input file with 2D area")
args = parser.parse_args()

# Load input.
filename = args.input if args.input else "area.txt"
reader = io_utils.Reader()
area = reader.read_area(filename)

# Calculate solution.
finder = solver.PathFinder()
path = finder.find_path(area)

# Print solution.
formatter = io_utils.Formatter()

if path:
    formatter.print_area(formatter.merge(area, path), not args.plain)
    print("")
    print("======= Cesta =======")
    formatter.print_path(path)
else:
    formatter.print_area(area, not args.plain)
    print("Zadání nemá řešení.")    

end = time.time()

# Print statistics.
if args.stats:
    expanded_states = finder.get_expanded_states_count()
    print("")
    print("======= Statistiky =======")
    print("Doba běhu:", round(end - start, 2), "s")
    print("Expandovaných stavů:", expanded_states)

    if path:
        print("Počet akcí:", len(path))
        print("Cena cesty:", solver.Path.get_cost(path))