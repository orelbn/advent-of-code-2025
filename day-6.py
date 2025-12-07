"""
Advent of Code 2025 - Day 6: Trash Compactor
Help the young cephalopod solve math problems arranged in vertical columns.
"""

from math import prod


def parse_input(data: str) -> tuple[list[str], list[str], list[tuple[int, int]]]:
    """
    Parses the raw input data into a board, operations, and problem boundaries.

    Args:
        data: The raw input string.

    Returns:
        Tuple of (board rows, operations list, problem boundaries).
    """
    lines = data.strip().splitlines()
    board = lines[:-1]
    operations = lines[-1].split()
    boundaries = find_problem_boundaries(board)
    return board, operations, boundaries


def is_separator_column(board: list[str], col: int) -> bool:
    """Checks if a column contains only spaces (problem separator)."""
    return all(row[col] == " " for row in board)


def find_problem_boundaries(board: list[str]) -> list[tuple[int, int]]:
    """
    Finds the (start, end) column boundaries for each problem.

    Args:
        board: The puzzle board.

    Returns:
        List of (start_col, end_col) tuples for each problem.
    """
    n = len(board[0])
    boundaries = []
    start = 0

    for col in range(n):
        if is_separator_column(board, col):
            if col > start:
                boundaries.append((start, col))
            start = col + 1

    if start < n:
        boundaries.append((start, n))

    return boundaries


def get_number_horizontal(board: list[str], col: int, row: int, end: int) -> int:
    """
    Reads a number horizontally from left to right within a row.

    Args:
        board: The puzzle board.
        col: Starting column index.
        row: Row index.
        end: Ending column index (exclusive).

    Returns:
        The parsed integer value.
    """
    return int("".join(c for c in board[row][col:end] if c != " "))


def get_number_vertical(board: list[str], col: int) -> int:
    """
    Reads a number vertically from top to bottom within a column.

    Args:
        board: The puzzle board.
        col: Column index.

    Returns:
        The parsed integer value.
    """
    return int("".join(row[col] for row in board if row[col] != " "))


def solve_part1(
    board: list[str], operations: list[str], boundaries: list[tuple[int, int]]
) -> int:
    """
    Solves Part 1: Read numbers horizontally within each problem.

    Each problem's numbers are read left-to-right as traditional integers,
    then combined using the operation at the bottom.

    Args:
        board: The puzzle board (rows of the worksheet).
        operations: List of operators ('+' or '*') for each problem.
        boundaries: Precomputed (start, end) column boundaries for each problem.

    Returns:
        Grand total of all problem answers.
    """
    totals = []

    for operation, (col, end) in zip(operations, boundaries):
        nums = [
            get_number_horizontal(board, col, row, end) for row in range(len(board))
        ]

        if operation == "*":
            totals.append(prod(nums))
        else:
            totals.append(sum(nums))

    return sum(totals)


def solve_part2(
    board: list[str], operations: list[str], boundaries: list[tuple[int, int]]
) -> int:
    """
    Solves Part 2: Read numbers vertically (cephalopod math).

    Each column within a problem represents a separate number,
    read top-to-bottom with the most significant digit at the top.

    Args:
        board: The puzzle board (rows of the worksheet).
        operations: List of operators ('+' or '*') for each problem.
        boundaries: Precomputed (start, end) column boundaries for each problem.

    Returns:
        Grand total of all problem answers.
    """
    totals = []

    for operation, (col, end) in zip(operations, boundaries):
        nums = [get_number_vertical(board, c) for c in range(col, end)]

        if operation == "*":
            totals.append(prod(nums))
        else:
            totals.append(sum(nums))

    return sum(totals)


def main():
    """Main entry point."""
    with open("day-6.input.txt") as f:
        data = f.read()

    board, operations, boundaries = parse_input(data)

    print(f"Part 1: {solve_part1(board, operations, boundaries)}")
    print(f"Part 2: {solve_part2(board, operations, boundaries)}")


if __name__ == "__main__":
    main()
