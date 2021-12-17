import heapq
import os
from collections import Counter
import heapq as heap


TEST = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""


DIRECTIONS = [
              (-1, 0),
    (0, -1),            (0, 1),
               (1, 0)
]


def adjacent(i, j, octopuses, t=1):
    xs = [(i + dx, j + dy) for dx, dy in DIRECTIONS]
    return [(i, j) for i, j in xs if 0 <= i < len(octopuses) * t and 0 <= j < len(octopuses[0]) * t]


def lookup(p, risks):
    tile_x = p[0] // (len(risks))
    tile_y = p[1] // (len(risks[0]))

    # p[0] % (len(risks) * (tile_x + 1))
    extra_risk = tile_x + tile_y

    risk = (extra_risk + risks[p[0] - (len(risks) * (tile_x + 1))][p[1] - (len(risks[0]) * (tile_y + 1))])
    if risk > 9:
        return risk - 9
    return risk


def dijkstra(risks, tiles=1):
    dist = {(0, 0): 0}
    prev = {}
    pq = []

    heap.heappush(pq, (0, (0, 0)))
    seen = set()
    while len(pq) > 0:
        cost, u = heapq.heappop(pq)

        neighbors = adjacent(u[0], u[1], risks, t=tiles)
        for v in neighbors:
            if v not in seen:
                alt = dist[u] + lookup(v, risks)
                seen.add(v)
                if v not in dist or alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))

    score = 0
    u = (len(risks) * tiles - 1, len(risks[0]) * tiles - 1)
    if u in prev:
        while u != (0, 0):
            score += lookup(u, risks)
            u = prev[u]
    return score


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        risks = fd.read()

    # risks = TEST
    risks = [[int(r) for r in risk] for risk in risks.split('\n')]

    print("PART 1:", dijkstra(risks, tiles=1))
    print("PART 2:", dijkstra(risks, tiles=5))


if __name__ == '__main__':
    solution()
