import os


TEST = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def horizontal_fold(dots, x):
    """
    #.##.|#..#.
    #...#|.....
    .....|#...#
    #...#|.....
    .#.#.|#.###
    .....|.....
    .....|.....
    """
    for i in range(len(dots)):
        if dots[i][0] > x:
            dots[i] = x - (dots[i][0] - x), dots[i][1]
    return dots


def vertical_fold(dots, y):
    """
    ...#..#..#.
    ....#......
    ...........
    #..........
    ...#....#.#
    ...........
    ...........
    -----------
    ...........
    ...........
    .#....#.##.
    ....#......
    ......#...#
    #..........
    #.#........
    """
    for i in range(len(dots)):
        if dots[i][1] > y:
            dots[i] = dots[i][0], y - (dots[i][1] - y)
    return dots


def visualize(dots):
    bottom = 0
    right = 0

    for d in dots:
        if d[0] > right:
            right = d[0]
        if d[1] > bottom:
            bottom = d[1]

    visualized = [['.' for _ in range(right + 1)] for _ in range(bottom + 1)]

    for d in dots:
        visualized[d[1]][d[0]] = '#'

    for row in visualized:
        print(''.join(row))


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        paper = fd.read()

    # paper = TEST
    dots = [(int(dot.split(',')[0]), int(dot.split(',')[1])) for dot in paper.split('\n\n')[0].split('\n')]
    folds = [(fold.split('=')[0][-1], int(fold.split('=')[1])) for fold in paper.split('\n\n')[1].split('\n')]

    for axis, n in folds[:1]:
        if axis == 'y':
            dots = vertical_fold(dots, y=n)
        else:
            dots = horizontal_fold(dots, x=n)

    print("PART 1:", len(set(dots)))

    for axis, n in folds[1:]:
        if axis == 'y':
            dots = vertical_fold(dots, y=n)
        else:
            dots = horizontal_fold(dots, x=n)

    print("PART 2:")
    visualize(dots)


if __name__ == '__main__':
    solution()
