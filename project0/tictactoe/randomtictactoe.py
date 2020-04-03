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
    """

    if terminal(board) is True:
        return None

    # Code for player O
    if player(board) is O:
        v = float("inf")
        optimal = []
        for action in actions(board):
            actionvalue = MaxValue(result(board, action))
            if actionvalue < v:
                optimal.clear()
                optimal.append(action)
                v = actionvalue
            elif actionvalue == v:
                optimal.append(action)
        i = random.randrange(len(optimal))
        return optimal[i]

    # Code for player X
    else:
        """
        As any first move is expected to tie playing optimally, just randomize the first move to be quicker
        To make it more interesting, we take a random move between all the optimal sollutions so that the computer wont always play the same game.
        """

        if board == [[EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY]]:
                        return (random.randrange(3),random.randrange(3))
        else:
            v = float("-inf")
            optimal = []
            for action in actions(board):
                actionvalue = MinValue(result(board, action))
                if actionvalue > v:
                    optimal.clear()
                    optimal.append(action)
                    v = actionvalue
                elif actionvalue == v:
                    optimal.append(action)
            i = random.randrange(len(optimal))
            return optimal[i]
