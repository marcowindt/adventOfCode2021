import os
from collections import Counter
from queue import PriorityQueue
from functools import reduce


def before_target(probe, t_x, t_y):
    return probe[0] < t_x[0] and probe[1] > t_y[1]


def passed_target(probe, t_x, t_y):
    return probe[0] > t_x[1] or probe[1] < t_y[0]


def in_target(probe, t_x, t_y):
    return t_x[0] <= probe[0] <= t_x[1] and t_y[0] <= probe[1] <= t_y[1]


def step(probe, velocity):
    probe = (probe[0] + velocity[0], probe[1] + velocity[1])

    if velocity[0] > 0:
        velocity = velocity[0] - 1, velocity[1] - 1
    elif velocity[0] < 0:
        velocity = velocity[0] + 1, velocity[1] - 1
    else:
        velocity = velocity[0], velocity[1] - 1

    return probe, velocity


def simulate(probe, velocity, target_x, target_y):
    probes = []
    touched_target = False
    highest = 0
    while not passed_target(probe, target_x, target_y):
        probe, velocity = step(probe, velocity)

        probes.append(probe)
        if probe[1] > highest:
            highest = probe[1]

        if in_target(probe, target_x, target_y):
            touched_target = True
            break

    return probes, touched_target, highest


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        target_area = fd.read()

    target_x_y = target_area.split('target area: ')[1]
    target_xs, target_ys = target_x_y.split(', ')
    target_x1, target_x2 = target_xs.split('=')[1].split('..')
    target_y1, target_y2 = target_ys.split('=')[1].split('..')

    target_x = (int(target_x1), int(target_x2))
    target_y = (int(target_y1), int(target_y2))

    # target_x[0] <= n * (n + 1) / 2 <= target_x[1]
    # possible_ys = []
    # for y in range(target_y[0], target_y[1] + 1):
    #     for i in range(-100, 1121):
    #         if - i * (i + 1) / 2 == y:
    #             print(i, y)
    #             possible_xs.append(i)

    possible_xs = []
    for v_x in range(1, target_x[1] + 1):
        probe_x = 0

        current_v_x = v_x
        while probe_x < target_x[0] and current_v_x != 0:
            probe_x += current_v_x

            if target_x[0] <= probe_x <= target_x[1]:
                possible_xs.append(v_x)

            if current_v_x > 0:
                current_v_x -= 1
            elif current_v_x < 0:
                current_v_x += 1

    was_in_target = 0
    highest = 0
    point = (0, 0)
    for v_x in possible_xs:
        for v_y in range(target_y[0], 300):
            probes, touched, p_highest = simulate((0, 0), (v_x, v_y), target_x=target_x, target_y=target_y)
            if touched:
                was_in_target += 1
                if p_highest > highest:
                    highest = p_highest
                    point = (v_x, v_y)

    print("PART 1:", int(highest), point)
    print("PART 2:", was_in_target)


if __name__ == '__main__':
    solution()
