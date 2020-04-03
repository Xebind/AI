"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math
import random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    board = [[EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY]]

    return board


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == [[EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY],
                    [EMPTY, EMPTY, EMPTY]]:
        return X
    else:
        Xcount = 0
        Ocount = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] is X:
                    Xcount = Xcount + 1
                if board[i][j] is O:
                    Ocount = Ocount + 1
        if Xcount > Ocount:
            return O
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                actions.append((i,j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != None:
        raise ValueError("Invalid action")

    copyboard = deepcopy(board)
    if player(board) is X:
        copyboard[action[0]][action[1]] = X
        return copyboard
    else:
        copyboard[action[0]][action[1]] = O
        return copyboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] =="O":
            return O
        elif board[0][i] == board[1][i] == board[2][i] =="O":
            return O
        elif board[i][0] == board[i][1] == board[i][2] == "X":
            return X
        elif board[0][i] == board[1][i] == board[2][i] == "X" :
            return X
    if board[0][0] == board[1][1] == board[2][2] =="O" or board[0][2] == board[1][1] == board[2][0] == "O":
        return O
    if board[0][0] == board[1][1] == board[2][2] =="X" or board[0][2] == board[1][1] == board[2][0] == "X":
        return X
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == "X" or winner(board) == "O":
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    elif winner(board) is O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board) is True:
        return None

    # Code for player O
    if player(board) is O:
        v = float("inf")
        for action in actions(board):
            if MaxValue(result(board, action)) < v:
                optimal = action
                v = MaxValue(result(board, action))
        return optimal
    # Code for player X
    else:
        """
        As any first move is expected to tie playing optimally, just randomize the first move to be quicker
        """
        if board == [[EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]:
                        return (random.randrange(3),random.randrange(3))
        else:
            v = float("-inf")
            for action in actions(board):
                if MinValue(result(board, action)) > v:
                    optimal = action
                    v = MinValue(result(board, action))
            return optimal


def MaxValue(board):
    if terminal(board) is True:
        return utility(board)
    else:
        v = float("-inf")
        for action in actions(board):
            v = max(v, MinValue(result(board,action)))
        return v

def MinValue(board):
    if terminal(board) is True:
        return utility(board)
    else:
        v = float("inf")
        for action in actions(board):
            v = min(v, MaxValue(result(board,action)))
        return v
