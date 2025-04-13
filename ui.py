import streamlit as st
import pandas as pd
import concurrent.futures

import time
import tempfile
import os
import pathlib

from parsers.file_parser import parse_file
from parsers.image_parser import parse_image
from solver.core import solve
from solver.utils import is_board_valid

import threading

def run_solver(board, timeout):
    """
    Runs the Sudoku solver with a timeout using threading.
    Args:
        board (np.ndarray): The Sudoku board to solve.
        timeout (int): Timeout in seconds
    Returns:
        bool: True if the puzzle is solved, False otherwise.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(solve, board)
        try:
            result = future.result(timeout=timeout)
            return result
        except concurrent.futures.TimeoutError:
            return False

def get_styled_board(board):
    df = pd.DataFrame(board)
    styled = df.style.hide(axis='columns').hide(axis='index')
    styled.set_table_styles(
        [{'selector': 'td', 'props': [('font-size', '20px')]}]
    )
    return styled.to_html()

os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5'
SUPPORTED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'txt', 'sdku']

st.title("🧩 Sudoku Solver")

uploaded_file = st.file_uploader(f"Upload Sudoku image or text file", type=SUPPORTED_EXTENSIONS)
timeout = st.slider("Solver Timeout (seconds)", 1, 30, 5)

if uploaded_file is not None:
    suffix = pathlib.Path(uploaded_file.name).suffix
    is_image = uploaded_file.name.endswith(('.png', '.jpg', '.jpeg', '.bmp'))

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        if is_image:
            board = parse_image(tmp_path)
        else:
            board = parse_file(tmp_path)

        st.write("Initial board")
        st.write(get_styled_board(board), unsafe_allow_html=True)

        if not is_board_valid(board):
            st.error("Invalid Sudoku board.")
        else:
            st.info("Solving...")
            start = time.time()
            solved = run_solver(board, timeout)
            elapsed = time.time() - start

            if solved:
                st.success(f"Solved in {elapsed:.2f} seconds!")
                st.write(get_styled_board(board), unsafe_allow_html=True)
            else:
                st.error("No solution found or solver timed out.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
