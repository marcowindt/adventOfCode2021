import os


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        steps = fd.readlines()
    steps = [(step.split(' ')[0], int(step.split(' ')[1])) for step in steps]

    position = (0, 0)
    for direction, amount in steps:
        if direction == 'forward':
            position = (position[0] + amount, position[1])
        elif direction == 'up':
            position = (position[0], position[1] - amount)
        elif direction == 'down':
            position = (position[0], position[1] + amount)

    print("PART 1:", position[0] * position[1])

    position = (0, 0, 0)
    for direction, amount in steps:
        if direction == 'forward':
            position = (position[0] + amount, position[1] + position[2] * amount, position[2])
        elif direction == 'up':
            position = (position[0], position[1], position[2] - amount)
        elif direction == 'down':
            position = (position[0], position[1], position[2] + amount)

    print("PART 2:", position[0] * position[1])


if __name__ == '__main__':
    solution()
