import os
import argparse
import signal

from parsers.file_parser import parse_file
from parsers.image_parser import parse_image
from solver.core import solve
from solver.utils import print_board, is_board_valid, timed

def timeout_handler(signum, frame):
    raise TimeoutError("Solver exceeded time limit.")

@timed("Solving")
def run_solver(board, timeout):
    """
    Runs the Sudoku solver with a timeout.
    
    Args:
        board (np.ndarray): The Sudoku board to solve.
        timeout (int): Timeout in seconds for the solver.
    
    Returns:
        bool: True if the puzzle is solved, False otherwise.
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        solved = solve(board)
        signal.alarm(0)
    except TimeoutError:
        print("Solver timed out.")
        return False
    
    return solved

@timed("Parsing")
def run_parser(input_path, is_file):  
    """
    Parses the input based on its type (file or image).
    
    Args:
        input_path (str): Path to the input file or image.
        is_file (bool): True if the input is a file, False if it's an image.
    
    Returns:
        np.ndarray: Parsed Sudoku board.
    """
    if is_file:
        return parse_file(input_path)
    else:
        return parse_image(input_path)

def parse_args():
    """
    Parses command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument("-i", "--input", type=str, help="Path to the Sudoku puzzle file or image.")
    parser.add_argument("-f", "--file", action="store_true", help="Specify if the input is a file.")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Timeout in seconds for the solver.")
    
    return parser.parse_args()

if __name__ == "__main__":
    os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5'
    args = parse_args()

    if not os.path.isfile(args.input):
        raise ValueError(f"Invalid file path: {args.input}")

    board = run_parser(args.input, args.file)
    print("Initial board:")
    print_board(board)
    if not is_board_valid(board):
        raise ValueError("Invalid Sudoku board.")
    print("Solving Sudoku...")

    solved = run_solver(board, args.timeout)

    if solved:
        print("Solved Sudoku:")
        print_board(board)
    else:
        print("No solution exists.")