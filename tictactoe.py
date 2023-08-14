import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns the player who has the next turn based on the current board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # If there are more X's than O's on the board, it's O's turn, and vice versa.
    return O if x_count > o_count else X

def actions(board):
    """
    Returns a set of all possible (i, j) actions on the board where the cell is empty.
    """
    available_actions = set()

    # Iterate through the board. If cell is empty, add its (i, j) coordinate to the set.
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available_actions.add((i, j))

    return available_actions

def result(board, action):
    """
    Returns the board state after making the given move.
    If the move is invalid, raises a ValueError.
    """
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError("Invalid action: Cell is not empty.")

    # Create a copy of the board and make the move.
    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)

    return new_board

def winner(board):
    """
    Checks all possible winning combinations.
    Returns the winning player if found, else returns None.
    """
    # Check rows for a winner
    for row in board:
        if all(cell == row[0] and cell != EMPTY for cell in row):
            return row[0]

    # Check columns for a winner
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    # No winner found
    return None

def terminal(board):
    """
    Returns True if game is over (either a tie or someone has won), else returns False.
    """
    game_over_due_to_win = winner(board) is not None
    game_over_due_to_tie = all(cell != EMPTY for row in board for cell in row)
    
    return game_over_due_to_win or game_over_due_to_tie

def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    current_player = player(board)
    
    # If board is terminal, return None as there are no valid moves
    if terminal(board):
        return None

    if current_player == X:
        value, best_move = max_value(board)
    else:
        value, best_move = min_value(board)

    return best_move

def max_value(board):
    if terminal(board):
        return utility(board), None

    value = -math.inf
    best_move = None

    for action in actions(board):
        next_value, _ = min_value(result(board, action))
        if next_value > value:
            value = next_value
            best_move = action
        if value == 1: # Pruning
            break

    return value, best_move

def min_value(board):
    if terminal(board):
        return utility(board), None

    value = math.inf
    best_move = None

    for action in actions(board):
        next_value, _ = max_value(result(board, action))
        if next_value < value:
            value = next_value
            best_move = action
        if value == -1: # Pruning
            break

    return value, best_move
