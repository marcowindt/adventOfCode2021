import os


TEST = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        chunks = fd.read()

    chunks = chunks.split('\n')

    open_close = {'(': ')', '[': ']', '{': '}', '<': '>'}
    close_open = {v: k for k, v in open_close.items()}
    illegals = {')': 3, ']': 57, '}': 1197, '>': 25137}
    counts = {')': 0, ']': 0, '}': 0, '>': 0}

    incompletes = []
    for chunk in chunks:
        stack = []

        corrupted = False
        for c in chunk:
            if c in open_close.keys():
                stack.append(c)
            elif c in open_close.values():
                if stack[-1] == close_open[c]:
                    stack.pop()
                else:
                    # print('expected', open_close[stack[-1]], 'but found', c, 'instead')
                    counts[c] += 1
                    corrupted = True
                    break
        if not corrupted:
            incompletes.append((chunk, stack))
            # print('incomplete stack', stack)

    points = {')': 1, ']': 2, '}': 3, '>': 4}
    scores = []
    for incomplete, stack in incompletes:
        closing = ''
        score = 0
        stack.reverse()
        for c in stack:
            closing += open_close[c]
            score *= 5
            score += points[open_close[c]]
        scores.append(score)

    scores = list(sorted(scores, reverse=False))

    print("PART 1:", sum([illegals[k] * counts[k] for k in illegals.keys()]))
    print("PART 2:", scores[len(scores) // 2])


if __name__ == '__main__':
    solution()
