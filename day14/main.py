import os
from collections import Counter


TEST = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        polymers = fd.read()

    # polymers = TEST
    original_template, rules = polymers.split('\n\n')
    rules = {rule.split(' -> ')[0]: rule.split(' -> ')[1] for rule in rules.split('\n')}

    template = original_template

    step = 1
    while step <= 10:
        new_template = ""

        i = 0
        while i < len(template) - 1:
            x, y = template[i], template[i + 1]
            new_template += x + rules[x + y]

            if i == len(template) - 2:
                new_template += y

            i += 1

        template = new_template
        step += 1

    print("PART 1:", Counter(template).most_common()[0][1] - Counter(template).most_common()[-1][1])

    counts = {combination: 0 for combination in rules.keys()}
    template = original_template
    for i in range(len(template) - 1):
        combo = template[i] + template[i + 1]
        counts[combo] += 1

    step = 1
    while step <= 40:
        update = {}

        for combination, count in counts.items():
            first = combination[0] + rules[combination]
            second = rules[combination] + combination[1]

            if first in update:
                update[first] += count
            else:
                update[first] = count

            if second in update:
                update[second] += count
            else:
                update[second] = count

        counts = update
        step += 1

    atoms = set(rules.values())
    nums = {atom: 0 for atom in atoms}

    for combo, count in counts.items():
        nums[combo[0]] += count
        nums[combo[1]] += count

    nums = Counter(nums).most_common()

    # since we count per pair, we are counting every atom twice, so divide by 2
    # plus one, for some reason
    print("PART 2:", int(nums[0][1] / 2 - nums[-1][1] / 2) + 1)


if __name__ == '__main__':
    solution()
