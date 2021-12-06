import os
from collections import Counter

TEST = """3,4,3,1,2"""


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        lanterns = fd.read()
    original_lanterns = [int(x) for x in lanterns.split(',')]
    lanterns = original_lanterns.copy()

    day = 1
    while day <= 80:
        new_lanterns = []
        for i, lantern in enumerate(lanterns):
            if lanterns[i] == 0:
                lanterns[i] = 6
                new_lanterns.append(8)
            else:
                lanterns[i] -= 1

        lanterns.extend(new_lanterns)
        day += 1

    print("PART 1:", len(lanterns))

    lns = [0 for _ in range(9)]
    d_lanterns = dict(Counter(original_lanterns.copy()))

    # make sure every possible key exists
    for i in range(9):
        if i in d_lanterns:
            lns[i] = d_lanterns[i]

    day = 1
    while day <= 256:
        lns = [lns[1], lns[2], lns[3], lns[4], lns[5], lns[6], lns[7] + lns[0], lns[8], lns[0]]
        day += 1

    print("PART 2:", sum(lns))


if __name__ == '__main__':
    solution()
