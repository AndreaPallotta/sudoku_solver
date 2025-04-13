from .utils import is_valid_move, find_empty_cells

def solve(board, depth=0, max_depth=1000, dead_end_cells=None):
    """
    Solves the Sudoku puzzle using backtracking.
    
    Args:
        board (np.ndarray): The Sudoku board to solve.
        
    Returns:
        bool: True if the puzzle is solved, False otherwise.
    """
    empty_cell = find_empty_cells(board)
    
    if not empty_cell:
        return True
    
    row, col = empty_cell
    
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row, col] = num
            if solve(board):
                return True
            board[row, col] = 0
    return False
