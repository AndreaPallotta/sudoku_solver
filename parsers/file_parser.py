import os
import numpy as np

def parse_file(file_path):
    """
    Parses a Sudoku grid from a file.
    Args:
        file_path (str): Path to the Sudoku file.
    Returns:
        np.ndarray: A 2D array representing the Sudoku grid.
    """
    if not file_path.lower().endswith(('.sdku', '.txt')):
        raise ValueError(f"Unsupported file format: {file_path}")
    
    grid = []
    with open(file_path, 'r') as file:
        content = file.readlines()
        if len(content) != 9:
            raise ValueError(f"File must contain 9 rows. Found: {len(content)}")
        for line in content:
            line = line.strip()
            if len(line) != 9:
                raise ValueError(f"Each row must contain 9 characters. Found: {line}")
            if line and not line.startswith('#'):
                grid.append([int(num) if num.isdigit() else 0 for num in line])

    return np.array(grid)