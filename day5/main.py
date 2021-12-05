import os
import collections

TEST = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


def generate_points(x1, y1, x2, y2):
    # check to prevent division by zero
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1
        return set([(x1, y) for y in range(y1, y2 + 1)])

    m = (y2 - y1) / (x2 - x1)
    # y = mx + c
    # find c
    c = y1 - m * x1

    if x1 > x2:
        x1, x2 = x2, x1
    xs = [x for x in range(x1, x2 + 1)]

    return set([(x, int(m * x + c)) for x in xs])


def initial_solution(my_vents):
    intersections = set()
    for i, (x1, y1, x2, y2) in enumerate(my_vents):
        for j in range(i + 1, len(my_vents)):
            line1 = generate_points(x1, y1, x2, y2)
            line2 = generate_points(*my_vents[j])
            intersections = intersections.union(line1.intersection(line2))

    print("PART 1:", len(intersections))


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        vents = fd.read()
    vents = vents.split('\n')
    vents = [(vent.split(' -> ')[0], vent.split(' -> ')[1]) for vent in vents]
    vents = [(int(left.split(',')[0]), int(left.split(',')[1]), int(right.split(',')[0]), int(right.split(',')[1])) for left, right in vents]

    only_horizontal_or_vertical = [vent for vent in vents if vent[0] == vent[2] or vent[1] == vent[3]]

    all_points = []
    for i, (x1, y1, x2, y2) in enumerate(only_horizontal_or_vertical):
        all_points.extend(list(generate_points(x1, y1, x2, y2)))
    print("PART 1:", len([item for item, count in collections.Counter(all_points).items() if count > 1]))

    all_points = []
    for i, (x1, y1, x2, y2) in enumerate(vents):
        all_points.extend(list(generate_points(x1, y1, x2, y2)))
    print("PART 2:", len([item for item, count in collections.Counter(all_points).items() if count > 1]))


if __name__ == '__main__':
    solution()
