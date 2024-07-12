import copy

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def make_player_move(board):
    while True:
        try:
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
            if board[row][col] == ' ':
                return row, col
            else:
                print("That space is already occupied. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter valid row and column numbers.")

def is_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    # Check if the board is full
    return all(board[i][j] != '-' for i in range(3) for j in range(3))

def get_available_moves(board):
    # Get a list of available moves (empty spaces) on the board
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == '-']

def minimax(board, depth, maximizing_player):
    if is_winner(board, 'X'):
        return 1
    elif is_winner(board, 'O'):
        return -1
    elif is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_available_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = 'X'
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_available_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = 'O'
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

def make_ai_move(board):
    best_score = float('-inf')
    best_move = None
    for move in get_available_moves(board):
        new_board = copy.deepcopy(board)
        new_board[move[0]][move[1]] = 'X'
        eval = minimax(new_board, 4, False)  # You can adjust the depth of the search here
        if eval > best_score:
            best_score = eval
            best_move = move
    return best_move


