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
    else:
        options = []
        for action in actions(board):
            options.append(action)
        i = random.randrange(len(options))
        #print(f"{options} length= {len(options)}, chose {i}")
        return options[i]
