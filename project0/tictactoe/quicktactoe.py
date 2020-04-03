from tictactoe import initial_state, player, actions, result, winner, terminal, utility, MaxValue, MinValue
import math
import random

X = "X"
O = "O"
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    To be quicker if we detect a winning move we take it, not taking into account other moves
    """

    if terminal(board) is True:
        return None

    # Code for player O
    if player(board) is O:
        v = float("inf")
        for action in actions(board):
            actionvalue = MaxValue(result(board, action))
            if actionvalue == -1:
                return action
            if actionvalue < v:
                optimal = action
                v = actionvalue
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
                actionvalue = MinValue(result(board, action))
                if actionvalue == 1:
                    return action
                if actionvalue > v:
                    optimal = action
                    v = actionvalue
            return optimal
