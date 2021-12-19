import heapq
import os
from math import sqrt
import numpy as np
from scipy.spatial.transform import Rotation as R


def rotations(beacons):
    possibles = []
    for i in range(24):
        possibles.append([])
    for x, y, z in beacons:
        # positive x
        possibles[0].append((+x, +y, +z))
        possibles[1].append((+x, -z, +y))
        possibles[2].append((+x, -y, -z))
        possibles[3].append((+x, +z, -y))

        # negative x
        possibles[4].append((-x, -y, +z))
        possibles[5].append((-x, +z, +y))
        possibles[6].append((-x, +y, -z))
        possibles[7].append((-x, -z, -y))

        # positive y
        possibles[8].append((+y, +z, +x))
        possibles[9].append((+y, -x, +z))
        possibles[10].append((+y, -z, -x))
        possibles[11].append((+y, +x, -z))

        # negative y
        possibles[12].append((-y, -z, +x))
        possibles[13].append((-y, +x, +z))
        possibles[14].append((-y, +z, -x))
        possibles[15].append((-y, -x, -z))

        # positive z
        possibles[16].append((+z, +x, +y))
        possibles[17].append((+z, -y, +x))
        possibles[18].append((+z, -x, -y))
        possibles[19].append((+z, +y, -x))

        # negative z
        possibles[20].append((-z, -x, +y))
        possibles[21].append((-z, +y, +x))
        possibles[22].append((-z, +x, -y))
        possibles[23].append((-z, -y, -x))
    return possibles


def apply_transformation(beacons, r, vector):
    return set([tuple(beacon) for beacon in (np.array(rotations(beacons)[r]) + np.array(vector))])


def find_distances(beacons):
    diff = {}
    inv = {}
    for m in range(len(beacons)):
        for n in range(m + 1, len(beacons)):
            if m == n:
                continue
            b_m = beacons[m]
            b_n = beacons[n]

            euclidean = euclidean_distance(b_m, b_n)
            diff[(b_m, b_n)] = euclidean
            inv[euclidean] = (b_m, b_n)
    return diff, inv


def euclidean_distance(b_m, b_n):
    return sqrt(sum([(b_m[k] - b_n[k]) ** 2 for k in range(3)]))


def dijkstra(graph):
    dist = {0: 0}
    prev = {}
    pq = []

    heapq.heappush(pq, (0, 0))
    seen = set()
    while len(pq) > 0:
        cost, u = heapq.heappop(pq)

        neighbors = graph[u]
        for v in neighbors:
            if v not in seen:
                alt = dist[u] + 1
                seen.add(v)
                if v not in dist or alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))
    return prev


def manhatten(scanner1, scanner2):
    return abs(scanner1[0] - scanner2[0]) + abs(scanner1[1] - scanner2[1]) + abs(scanner1[2] - scanner2[2])


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        scanners = fd.read()
    # with open(os.path.join(os.path.dirname(__file__), './test.txt'), 'r') as fd:
    #     scanners = fd.read()

    scanners = [[eval('(' + pos + ')') for pos in scanner.split('---\n')[1].split('\n')] for scanner in
                scanners.split('\n\n')]

    observed_beacons = set(scanners[0])
    mapping = {}
    for i in range(len(scanners)):
        for j in range(len(scanners)):
            if i == j:
                continue
            beacons_x = scanners[i]
            beacons_y = scanners[j]

            diff_x, inv_x = find_distances(beacons_x)
            diff_x_set = set(diff_x.values())
            diff_y, inv_y = find_distances(beacons_y)
            diff_y_set = set(diff_y.values())

            intersections = len(diff_x_set.intersection(diff_y_set))
            if intersections:
                b_x = set()
                b_y = set()

                for (b_m_x, b_n_x), distance_x in diff_x.items():
                    if distance_x in inv_y:
                        b_x.add(b_m_x)
                        b_x.add(b_n_x)
                        b_y.add(inv_y[distance_x][0])
                        b_y.add(inv_y[distance_x][1])

                b_x = np.array([list(b) for b in b_x])
                b_y = np.array([list(b) for b in b_y])

                all_24_rotations = rotations(b_x)
                for r, beacons_x in enumerate(all_24_rotations):
                    combinations = []
                    for x in beacons_x:
                        for y in b_y:
                            diff = y - x

                            found = True
                            for z in beacons_x:
                                if z + diff not in b_y:
                                    found = False
                                    break
                            if found:
                                if tuple(diff) not in combinations:
                                    combinations.append(tuple(diff))
                    if len(combinations) == 1:
                        mapping[(i, j)] = (r, combinations[0])
                        break

    paths = {}
    for s, d in mapping.keys():
        if s not in paths:
            paths[s] = [d]
            continue
        paths[s].append(d)

    prev = dijkstra(paths)
    for i in range(1, len(scanners)):
        my_scanners = scanners[i]
        if i not in prev:
            print('houston we have a problem', i)
            continue
        u = i
        while u != 0:
            to_map = prev[u]

            my_scanners = apply_transformation(
                beacons=my_scanners,
                r=mapping[(u, to_map)][0],
                vector=mapping[(u, to_map)][1]
            )
            u = prev[u]
        observed_beacons = observed_beacons.union(my_scanners)

    print("PART 1:", len(observed_beacons))

    found_max = 0

    scanners_relative = {}
    for (i, j), (r, scanner_x) in mapping.items():
        if j == 0:
            scanners_relative[(i, j)] = scanner_x
            continue
        my_scanners = [scanner_x]

        if j not in prev:
            print('houston we have a problem', j)
            continue

        u = j
        while u != 0:
            to_map = prev[u]

            my_scanners = apply_transformation(
                beacons=my_scanners,
                r=mapping[(u, to_map)][0],
                vector=mapping[(u, to_map)][1]
            )
            u = prev[u]
        scanners_relative[(i, u)] = list(my_scanners)[0]

    del scanners_relative[(0, 0)]

    for (i, j), scanner_x in scanners_relative.items():
        for (m, n), scanner_y in scanners_relative.items():
            if scanner_y == scanner_x:
                continue
            distance = manhatten(scanner_x, scanner_y)
            if distance > found_max:
                found_max = distance

    print("PART 2:", found_max)


if __name__ == '__main__':
    solution()

# x, y, z ->  x,  y,  z
#         ->  x,  z,  y
#         ->  y,  x,  z
#         ->  y,  z,  x
#         ->  z,  x,  y
#         ->  z,  y,  x
# x, y, z ->  x,  y,  z
#         ->  x,  y, -z
#         ->  x, -y,  z
#         ->  x, -y, -z
#         -> -x,  y,  z
#         -> -x,  y, -z
#         -> -x, -y,  z
#         -> -x, -y, -z
