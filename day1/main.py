import os


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        sweeps = fd.readlines()
    sweeps = [int(sweep) for sweep in sweeps]

    increasing = 0
    for i in range(1, len(sweeps)):
        if sweeps[i] - sweeps[i - 1] > 0:
            increasing += 1

    print("PART 1:", increasing)

    increasing = 0
    for i in range(3, len(sweeps)):
        first = sweeps[i - 3] + sweeps[i - 2] + sweeps[i - 1]
        second = sweeps[i - 2] + sweeps[i - 1] + sweeps[i]
        if second > first:
            increasing += 1

    print("PART 2:", increasing)


if __name__ == '__main__':
    solution()
