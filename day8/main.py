import os


TEST = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


REAL_DIGITS = {
    'abcefg': '0',
    'cf': '1',
    'acdeg': '2',
    'acdfg': '3',
    'bcdf': '4',
    'abdfg': '5',
    'abdefg': '6',
    'acf': '7',
    'abcdefg': '8',
    'abcdfg': '9',
}


def valid_mapping(mapping, digits):
    mapping = {v: k for k, v in mapping.items()}
    for digit in digits:
        real_segments = ''
        for segment in digit:
            real_segments += mapping[segment]

        if ''.join(sorted(real_segments)) not in REAL_DIGITS:
            return False
    return True


def convert(mapping, digits):
    mapping = {v: k for k, v in mapping.items()}

    converted = ''
    for digit in digits:
        real_segments = ''
        for segment in digit:
            real_segments += mapping[segment]

        converted += REAL_DIGITS[''.join(sorted(real_segments))]

    return int(converted)


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        signals = fd.read()

    # signals = TEST
    signals = [(signal.split(' | ')[0].split(' '), signal.split(' | ')[1].split(' ')) for signal in signals.split("\n")]

    d = {2: 1, 4: 4, 3: 7, 7: 8}
    c = {1: 0, 4: 0, 7: 0, 8: 0}

    for left, right in signals:
        for signal in right:
            if len(signal) in d:
                c[d[len(signal)]] += 1

    print("PART 1:", sum(c.values()))

    output = []
    for s, (left, right) in enumerate(signals):
        display = {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None}
        mapping = {}

        for signal in left:
            if len(signal) in d:
                mapping[d[len(signal)]] = signal

        found = False
        for k in range(2):
            if found:
                break

            display['c'] = mapping[1][k]
            display['f'] = mapping[1][(k + 1) % 2]
            display['a'] = mapping[7].replace(display['c'], '').replace(display['f'], '')

            mapping_4 = mapping[4].replace(display['c'], '').replace(display['f'], '').replace(display['a'], '')
            for j in range(2):
                display['b'] = mapping_4[j]
                display['d'] = mapping_4[(j + 1) % 2]

                check_display = display.copy()

                remaining = [c for c in 'abcdefg' if c not in check_display.values()]

                if found:
                    break
                for i in range(2):
                    check_display['e'] = remaining[i]
                    check_display['g'] = remaining[(i + 1) % 2]

                    if valid_mapping(check_display, left):
                        output.append(convert(check_display, right))
                        found = True
                        break

    print("PART 2:", sum(output))


if __name__ == '__main__':
    solution()
