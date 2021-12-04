import os


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        bingo = fd.read()

    drawn, boards = bingo.split("\n\n")[0], bingo.split("\n\n")[1:]

    drawn = [int(d) for d in drawn.split(',')]
    boards = [[[int(number) for number in row.split(' ') if number != ''] for row in board.split('\n')] for board in boards]

    boards_won = []
    board_scores = {}
    for d in drawn:
        for num, board in enumerate(boards):
            if num in boards_won:
                continue

            for i, row in enumerate(board):
                for j, col in enumerate(board[i]):
                    if board[i][j] == d:
                        board[i][j] = -1

            for i, row in enumerate(board):
                if sum(row) == -5:
                    points = sum([sum([n for n in board[k] if n != -1]) for k in range(len(board)) if k != i])
                    boards_won.append(num)
                    board_scores[num] = points * d

            for j, col in enumerate(board):
                if sum([board[i][j] for i in range(len(board[0]))]) == -5:
                    points = sum([sum([n for m, n in enumerate(board[k]) if n != -1 and m != j]) for k in range(len(board))])
                    boards_won.append(num)
                    board_scores[num] = points * d

    print("PART 1:", "board", boards_won[0], "score", board_scores[boards_won[0]])
    print("PART 2:", "board", boards_won[-1], "score", board_scores[boards_won[-1]])


if __name__ == '__main__':
    solution()
