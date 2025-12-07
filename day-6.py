"""
Advent of Code 2025 - Day 6: Trash Compactor
Help the young cephalopod solve math problems arranged in vertical columns.
"""

from math import prod


def parse_input(data: str) -> tuple[list[str], list[str]]:
    """
    Parses the raw input data into a board and operations.

    Args:
        data: The raw input string.

    Returns:
        Tuple of (board rows, operations list).
    """
    lines = data.strip().splitlines()
    board = lines[:-1]
    operations = lines[-1].split()
    return board, operations


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
    num = 0
    for c in range(col, end):
        if board[row][c] != " ":
            num = num * 10 + int(board[row][c])
    return num


def get_number_vertical(board: list[str], col: int) -> int:
    """
    Reads a number vertically from top to bottom within a column.

    Args:
        board: The puzzle board.
        col: Column index.

    Returns:
        The parsed integer value.
    """
    num = 0
    for row in range(len(board)):
        if board[row][col] != " ":
            num = num * 10 + int(board[row][col])
    return num


def find_problem_end(board: list[str], start_col: int) -> int:
    """
    Finds the ending column of a problem (first all-space column or end of board).

    Args:
        board: The puzzle board.
        start_col: Starting column index.

    Returns:
        The ending column index (exclusive).
    """
    n = len(board[0])
    end = start_col
    for row in range(len(board)):
        idx = board[row].find(" ", start_col)
        end = max(end, idx if idx != -1 else n)
    return end


def solve_part1(board: list[str], operations: list[str]) -> int:
    """
    Solves Part 1: Read numbers horizontally within each problem.

    Each problem's numbers are read left-to-right as traditional integers,
    then combined using the operation at the bottom.

    Args:
        board: The puzzle board (rows of the worksheet).
        operations: List of operators ('+' or '*') for each problem.

    Returns:
        Grand total of all problem answers.
    """
    col = 0
    totals = []

    for operation in operations:
        end = find_problem_end(board, col)
        nums = [
            get_number_horizontal(board, col, row, end) for row in range(len(board))
        ]

        if operation == "*":
            totals.append(prod(nums))
        else:
            totals.append(sum(nums))

        col = end + 1

    return sum(totals)


def solve_part2(board: list[str], operations: list[str]) -> int:
    """
    Solves Part 2: Read numbers vertically (cephalopod math).

    Each column within a problem represents a separate number,
    read top-to-bottom with the most significant digit at the top.

    Args:
        board: The puzzle board (rows of the worksheet).
        operations: List of operators ('+' or '*') for each problem.

    Returns:
        Grand total of all problem answers.
    """
    col = 0
    totals = []

    for operation in operations:
        end = find_problem_end(board, col)
        nums = [get_number_vertical(board, c) for c in range(col, end)]

        if operation == "*":
            totals.append(prod(nums))
        else:
            totals.append(sum(nums))

        col = end + 1

    return sum(totals)


def main():
    """Main entry point."""
    with open("day-6.input.txt") as f:
        data = f.read()

    board, operations = parse_input(data)

    print(f"Part 1: {solve_part1(board, operations)}")
    print(f"Part 2: {solve_part2(board, operations)}")


if __name__ == "__main__":
    main()
