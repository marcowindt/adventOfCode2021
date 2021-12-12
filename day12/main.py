import os


TEST = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


SECOND_TEST = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""


LARGE_EXAMPLE = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        caves = fd.read()

    caves = caves.split('\n')
    caves = [cave.split('-') for cave in caves]

    caveology = {}
    for node1, node2 in caves:
        if node1 not in caveology:
            caveology[node1] = [node2]
        else:
            caveology[node1].append(node2)
        if node2 not in caveology:
            caveology[node2] = [node1]
        else:
            caveology[node2].append(node1)

    paths = [['start']]
    finished = []
    prev_len = 0
    while len(paths) != prev_len:
        prev_len = len(paths)
        new_paths = []
        for i, path in enumerate(paths):
            if path[-1] == 'end':
                finished.append(path.copy())
                continue
            for node in caveology[path[-1]]:
                if node == 'start' or (node.islower() and node in path):
                    continue
                new_paths.append(path + [node])
        paths = new_paths

    print("PART 1:", len(finished))

    twice = []
    for node in caveology.keys():
        if node.islower() and node != 'start' and node != 'end':
            twice.append(node)

    paths = [['start']]
    finished = []
    prev_len = 0
    while len(paths) != prev_len:
        prev_len = len(paths)
        new_paths = []
        for i, path in enumerate(paths):
            if path[-1] == 'end':
                finished.append(path)
                continue
            for node in caveology[path[-1]]:
                if node == 'start':
                    continue
                if node.islower() and node in path:
                    if node not in twice:
                        continue
                    breaked = False
                    for t in twice:
                        if path.count(t) > 1:
                            breaked = True
                            break
                    if breaked:
                        continue
                new_paths.append(path + [node])
        paths = new_paths

    print("PART 2:", len(finished))


if __name__ == '__main__':
    solution()
