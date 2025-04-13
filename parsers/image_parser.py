import cv2
import os
import numpy as np
import pytesseract

def get_distance(point1, point2):
    """
    Calculates the Euclidean distance between two points.
    Args:
        point1 (np.ndarray): First point.
        point2 (np.ndarray): Second point.
    Returns:
        float: The distance between the two points.
    """
    return np.linalg.norm(point1 - point2)

def extract_digit(cell_img):
    """
    Extracts a digit from a cell image using Tesseract OCR.
    Args:
        cell_img (np.ndarray): The image of the cell.
        Returns:
        int: The digit extracted from the cell image.
    """
    gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (0, 0), fx=5, fy=5, interpolation=cv2.INTER_LINEAR)
    _, thresh = cv2.threshold(resized, 150, 255, cv2.THRESH_BINARY_INV)

    config = r'--psm 10 --oem 3 --tessdata-dir "/usr/share/tesseract-ocr/5/tessdata"'
    text = pytesseract.image_to_string(thresh, config=config).strip()
    
    if text.isdigit():
        return int(text)
    return 0

def parse_image(image_path):
    """
    Parses a Sudoku puzzle image and extracts the grid.
    Args:
        image_path (str): Path to the Sudoku image.
    Returns:
        np.ndarray: A 2D array representing the Sudoku grid.
    """
    if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        raise ValueError(f"Unsupported file format: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read the image file: {image_path}")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    binary = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    corners = cv2.approxPolyDP(largest_contour, epsilon, True)

    if len(corners) != 4:
        raise ValueError("Could not find the corners of the sudoku grid.")

    corners = corners.reshape(4, 2)
    sum_coords = corners.sum(axis=1)
    diff_coords = np.diff(corners, axis=1).flatten()

    top_left = corners[np.argmin(sum_coords)]
    bottom_right = corners[np.argmax(sum_coords)]
    top_right = corners[np.argmin(diff_coords)]
    bottom_left = corners[np.argmax(diff_coords)]

    ordered = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")

    width = int(max(get_distance(ordered[0], ordered[1]), get_distance(ordered[2], ordered[3])))
    height = int(max(get_distance(ordered[0], ordered[3]), get_distance(ordered[1], ordered[2])))

    dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")
    matrix = cv2.getPerspectiveTransform(ordered, dst)
    warped_image = cv2.warpPerspective(image, matrix, (width, height))

    cell_width = width // 9
    cell_height = height // 9

    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            x1, y1 = j * cell_width, i * cell_height
            x2, y2 = (j + 1) * cell_width, (i + 1) * cell_height
            cell = warped_image[y1:y2, x1:x2]
            digit = extract_digit(cell)
            row.append(digit)
        grid.append(row)

    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("Parsed grid is not 9x9.")
    return np.array(grid)
