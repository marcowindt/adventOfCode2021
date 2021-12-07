import os
from statistics import median


TEST = """16,1,2,0,4,2,7,1,2,14"""


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        crabs = fd.read()

    crabs = [int(crab) for crab in crabs.split(',')]
    positions = [h for h in range(min(crabs), max(crabs) + 1)]

    print("PART 1:", sum([abs(x - int(median(crabs))) for x in crabs]))

    min_fuel = 99999999999999
    for pos in positions:
        def fuel(crab):
            return abs(crab - pos) * (abs(crab - pos) + 1) / 2
        fuel = sum([fuel(x) for x in crabs])

        if fuel < min_fuel:
            min_fuel = fuel

    print("PART 2:", int(min_fuel))


if __name__ == '__main__':
    solution()
