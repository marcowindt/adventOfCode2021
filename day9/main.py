import os


TEST = """2199943210
3987894921
9856789892
8767896789
9899965678"""


def adjacent_points(heightmap, i, j):
    return [heightmap[i][j] for i, j in adjacent(i, j, heightmap)]


def adjacent(i, j, heightmap):
    xs = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    return [(i, j) for i, j in xs if 0 <= i < len(heightmap) and 0 <= j < len(heightmap[0])]


def basin(heightmap, i, j):
    visited = set()
    to_visit = [(i, j)]

    while len(to_visit):
        next_visits = set()
        for v_i, v_j in to_visit:
            neighbors = adjacent(v_i, v_j, heightmap)
            for n_i, n_j in neighbors:
                if (n_i, n_j) not in visited and heightmap[n_i][n_j] != 9 and heightmap[n_i][n_j] > heightmap[v_i][v_j]:
                    next_visits.add((n_i, n_j))

        visited = visited.union(to_visit)
        to_visit = list(next_visits)

    return visited


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        heights = fd.read()

    # heights = TEST
    heights = [[int(x) for x in height] for height in heights.split('\n')]

    low_points = []
    for i, row in enumerate(heights):
        for j, height in enumerate(heights[i]):
            low_point = True
            for x in adjacent_points(heights, i, j):
                if x <= height:
                    low_point = False

            if low_point:
                low_points.append((i, j, height))

    print("PART 1:", sum([p + 1 for i, j, p in low_points]))

    basins = [len(basin(heights, i, j)) for i, j, p in low_points]
    basins = list(sorted(basins, reverse=True))
    print("PART 2:", basins[0] * basins[1] * basins[2])


if __name__ == '__main__':
    solution()
