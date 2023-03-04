import numpy as np
from math import inf as INF


def print_board(board):
    chars = {1: 'x', 2: 'o', 0: ' '}
    print('-------------')
    for x in board:
        for y in x:
            print('|', chars[y], end=' ')
        print('|\n' + '-------------')
    print()


def game_over(board):
    # Check rows
    for x in board:
        if len(set(x)) == 1:
            return x[0]

    # Check columns
    for x in board.T:
        if len(set(x)) == 1:
            return x[0]

    # Check diagonals
    if len(set(board.diagonal())) == 1:
        return board.diagonal()[0]
    if len(set(np.fliplr(board).diagonal())) == 1:
        return np.fliplr(board).diagonal()[0]

    # Check if board is full
    if 0 not in board:
        return -1

    # Game is not over
    return 0


def make_move(board, player):
    if player == 1:
        pos = int(input('Enter position (1-9): '))
        if pos < 1 or pos > 9:
            raise ValueError('Illegal move!')
        row = (pos-1) // 3
        col = (pos-1) % 3
        if board[row][col] != 0:
            raise ValueError('Illegal move!')
        board[row][col] = 1
    else:
        value, row, col = ab_minimax(board, 0, -INF, INF, True)
        board[row][col] = 2


def ab_minimax(board, depth, alpha, beta, maximizing_player):
    best_r, best_c = -1, -1
    result = game_over(board)
    if result == 1:
        return -(10-depth), best_r, best_c
    elif result == 2:
        return 10-depth, best_r, best_c
    elif result == -1:
        return 0, best_r, best_c

    legal_moves = np.where(board == 0)

    if maximizing_player:
        value = -INF
        for r, c in zip(legal_moves[0], legal_moves[1]):
            board[r][c] = 2
            next_value, next_r, next_c = ab_minimax(board, depth+1, alpha, beta, False)
            if next_value > value:
                value = next_value
                best_r, best_c = r, c
            board[r][c] = 0
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value, best_r, best_c
    else:
        value = INF
        for r, c in zip(legal_moves[0], legal_moves[1]):
            board[r][c] = 1
            next_value, next_r, next_c = ab_minimax(board, depth+1, alpha, beta, True)
            if next_value < value:
                value = next_value
                best_r, best_c = r, c
            board[r][c] = 0
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_r, best_c


board = np.zeros((3, 3))
player = 1
while not game_over(board):
    print_board(board)
    try:
        make_move(board, player)
        player = 3 - player
    except ValueError as e:
        print(e)


print('Game over!')
print_board(board)
result = game_over(board)
if result == 1:
    print('You won!')
elif result == 2:
    print('You lost!')
else:
    print('It\'s a tie!')
