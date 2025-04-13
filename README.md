# 🧩 Sudoku Solver

A Python-based Sudoku solver that accepts either an image or a text file as input, parses the board, and solves it using backtracking

---

## Setup

1. **Clone the Repository**

```
git clone https://github.com/AndreaPallotta/sudoku_solver.git  
cd sudoku-solver
```

2. **Install System Dependencies**

Make sure the following packages are installed (for image parsing):

```bash
sudo apt update && sudo apt install -y libgl1 libglib2.0-0 tesseract-ocr
```

3. **Create and Activate Conda Environment**

```bash
conda env create -f env.yaml  
conda activate sudoku-solver
```

---

## Usage

Run the solver with:

```bash
python main.py -i <path_to_input> [--file] [-t TIMEOUT]
```

### Arguments:

- `-i` or `--input`: Path to the input Sudoku file or image.
- `-f` or `--file`: Use this flag if the input is a plain text file (instead of an image).
- `-t` or `--timeout`: Max time (in seconds) allowed for solving the puzzle (default: 10 seconds)

### Examples

From an image:

```bash
python main.py -i puzzles/sudoku1.png
```

From a .txt file:

```bash
# Check the /data folder for example files
python main.py -i puzzles/sudoku1.txt --file
```

With a custom timeout:

```bash
python main.py -i puzzles/hard.png -t 20
```
