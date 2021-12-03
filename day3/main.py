import os


def oxygen_rate_keep(keep):
    if len(keep[1]) >= len(keep[0]):
        return keep[1]
    return keep[0]


def co2_rate_keep(keep):
    if len(keep[0]) <= len(keep[1]):
        return keep[0]
    return keep[1]


def calc_rate(reports, keep_fn):
    digits_len = len(reports[0])
    current = 0

    while current < digits_len:
        keep = {1: [], 0: []}

        for report in reports:
            if report[current] == 1:
                keep[1].append(report)
            else:
                keep[0].append(report)

        reports = keep_fn(keep)
        current += 1

        if len(reports) == 1:
            break

    return reports[0]


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        reports = fd.readlines()
    reports = [[int(x) for x in report if x != "\n"] for report in reports]
    diagnostic = [0] * len(reports[0])

    for report in reports:
        for i, digit in enumerate(report):
            if digit == 1:
                diagnostic[i] += 1

    gamma = [0] * len(diagnostic)
    epsilon = [1] * len(diagnostic)

    for i, d in enumerate(diagnostic):
        if d > len(reports) / 2:
            gamma[i] = 1
            epsilon[i] = 0

    gamma = int("".join(str(x) for x in gamma), 2)
    epsilon = int("".join(str(x) for x in epsilon), 2)

    print("PART 1:", gamma * epsilon)

    o2_rate, co2_rate = calc_rate(reports, oxygen_rate_keep), calc_rate(reports, co2_rate_keep)
    o2_rate = int("".join(str(x) for x in o2_rate), 2)
    co2_rate = int("".join(str(x) for x in co2_rate), 2)

    print("PART 2:", o2_rate * co2_rate)


if __name__ == '__main__':
    solution()
