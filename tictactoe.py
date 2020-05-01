"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_counter += 1
            elif cell == O:
                o_counter += 1
    
    if o_counter < x_counter:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    if (board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]
    elif (board[0][2] == board[1][1] == board[2][0]):
        return board[2][0]
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2]):
            return board[i][0]
        
        if (board[0][i] == board[1][i] == board[2][i]):
            return board[0][i]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    x_counter = 0
    o_counter = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_counter += 1
            elif cell == O:
                o_counter += 1
    
    if o_counter + x_counter <9:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_move = None
    if player(board) == X:
        value = -2
        
        for action in actions(board):
            minimum = min_value(result(board, action))
            if minimum > value:
                value = minimum
                best_move = action
        return best_move
    else:
        value = 2
        for action in actions(board):
            maximum = max_value(result(board, action))
            if maximum < value:
                value = maximum
                best_move = action
        return best_move

def max_value(board):
    if terminal(board):
        return utility(board)

    v = -2
    for action in actions(board):
        v=max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)

    v = 2
    for action in actions(board):
        v=min(v, max_value(result(board, action))) 
    
    return v