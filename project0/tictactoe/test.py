from tictactoe import initial_state, player, actions, result, winner, terminal, utility, MaxValue, MinValue
X = "X"
O = "O"
EMPTY = None

board = [[X, EMPTY, EMPTY],
                [EMPTY, O, EMPTY],
                [EMPTY, EMPTY, EMPTY]]

for action in actions(board):
    print(f"{action} value of {MaxValue(result(board,action))}")
