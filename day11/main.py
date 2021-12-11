import os


TEST = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

SMALL_TEST = """11111
19991
19191
19991
11111"""

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),            (0, 1),
    (1, -1),   (1, 0),  (1, 1)
]


def adjacent(i, j, octopuses):
    xs = [(i + dx, j + dy) for dx, dy in DIRECTIONS]
    return [(i, j) for i, j in xs if 0 <= i < len(octopuses) and 0 <= j < len(octopuses[0])]


def all_flashing(octopuses):
    for i in range(len(octopuses)):
        for j in range(len(octopuses)):
            if octopuses[i][j] != 0:
                return False
    return True


def print_step(step: int, octopuses, total_flashing):
    print("AFTER STEP:", step)
    for row in octopuses:
        print(''.join([str(x) for x in row]))
    print("total_flashing:", total_flashing)
    print('')


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        octopuses = fd.read()

    octopuses = octopuses.split('\n')
    octopuses = [[int(octopus) for octopus in row] for row in octopuses]

    step = 1
    total_flashing = 0
    total_flashing_step_100 = 0
    while not all_flashing(octopuses):
        flashing = set()
        for i in range(len(octopuses)):
            for j in range(len(octopuses)):
                octopuses[i][j] += 1
                if octopuses[i][j] > 9:
                    flashing.add((i, j))

        new_flashing = flashing.copy()
        while len(new_flashing):
            added_flashing = set()
            for i, j in new_flashing:
                nearopuses = adjacent(i, j, octopuses)
                for m, n in nearopuses:
                    if (m, n) in flashing:
                        continue
                    octopuses[m][n] += 1
                    if octopuses[m][n] > 9:
                        added_flashing.add((m, n))
            new_flashing = added_flashing
            flashing = flashing.union(new_flashing)

        for i, j in flashing:
            octopuses[i][j] = 0

        if step <= 100:
            total_flashing_step_100 += len(flashing)
        total_flashing += len(flashing)

        # if step % 10 == 0:
        #     print_step(step, octopuses, total_flashing)
        step += 1

    print("PART 1:", total_flashing_step_100)
    print("PART 2:", step - 1)


if __name__ == '__main__':
    solution()
