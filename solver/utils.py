import time

def is_valid_move(board, row, col, num):
    """
    Checks if placing a number in a specific cell is valid according to Sudoku rules.
    
    Args:
        board (np.ndarray): The Sudoku board.
        row (int): The row index.
        col (int): The column index.
        num (int): The number to place.
        
    Returns:
        bool: True if the move is valid, False otherwise.
    """
    for i in range(9):
        if board[row, i] == num and col != i:
            return False
        if board[i, col] == num and row != i:
            return False
    
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3

    for i in range(box_col_start, box_col_start + 3):
        for j in range(box_row_start, box_row_start + 3):
            if board[j, i] == num and (j != row or i != col):
                return False
    return True

def find_empty_cells(board):
    """
    Finds the first empty cell in the Sudoku board."""
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                return i, j
    return None

def is_board_valid(board):
    """
    Checks if the Sudoku board is valid according to Sudoku rules.
    Args:
        board (np.ndarray): The Sudoku board to validate.
    Returns:
        bool: True if the board is valid, False otherwise.
    """
    row = [[False] * 9 for _ in range(9)]
    col = [[False] * 9 for _ in range(9)]
    sub = [[False] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            c = board[i][j]
            if c == 0:
                continue
            num = int(c) - 1
            k = i // 3 * 3 + j // 3
            if row[i][num] or col[j][num] or sub[k][num]:
                return False
            row[i][num] = True
            col[j][num] = True
            sub[k][num] = True
    
    return True

def print_board(board):
    """
    Prints the Sudoku board in a readable format.
    
    Args:
        board (np.ndarray): The Sudoku board.
    """
    for row in board:
        print(" ".join(str(num) if num != 0 else '-' for num in row))

def timed(label):
    """
    Decorator to time the execution of a function.
    Args:
        label (str): Label for the timed function.
    Returns:
        function: Decorated function that prints the execution time.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            print(f"{label} took {duration:.4f} seconds")
            return result
        return wrapper
    return decorator
