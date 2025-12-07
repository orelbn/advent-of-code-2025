"""
Advent of Code 2025 - Day X
"""

from math import prod


def parse_input(data: str) -> list[str]:
    """
    Parses the raw input data.

    Args:
        data: The raw input string.

    Returns:
        Parsed input data.
    """
    lines = data.strip().splitlines()
    return lines


def structure_data(parsed: list[str]) -> list[list[str]]:
    """
    Creates a board by separating cols by spaces, and rows by new lines.

    Args:
        parsed: The parsed input data.

    Returns:
        Board with rows and cols
    """
    board = parsed
    operations = board.pop().split()

    return (board, operations)


def get_col_num_simple(board: list[list[str]], col: int, row: int, end: int) -> int:
    num = 0
    while col < end:
        if board[row][col] != " ":
            num = num * 10 + int(board[row][col])
        col += 1
    return num


def get_col_num_complex(board: list[list[str]], col: int, num_rows: int) -> int:
    num = 0
    for row in range(num_rows):
        if board[row][col] != " ":
            num = num * 10 + int(board[row][col])
    return num


def find_end_col(board: list[list[str]], start_col: int, num_rows: int) -> int:
    end = start_col
    n = len(board[0])
    for row in range(num_rows):
        idx = board[row].find(" ", start_col)
        end = max(
            end,
            (idx if idx != -1 else n),
        )
    return end


def solve_part1(board: list[list[str]], operations: list[str]) -> int:
    """
    Solves Part 1.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 1.
    """
    m = len(board)
    col = 0
    i = 0
    num_rows = m
    totals = []
    while i < len(operations):
        end = find_end_col(board, col, num_rows)
        operation = operations[i]
        nums = []
        for row in range(num_rows):
            nums.append(get_col_num_simple(board, col, row, end))
        if operation == "*":
            totals.append(prod(nums))
        else:
            totals.append(sum(nums))
        col = end + 1
        i += 1
    return sum(totals)


def solve_part2(board: list[list[str]], operations: list[str]) -> int:
    """
    Solves Part 2.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 2.
    """
    m = len(board)
    col = 0
    i = 0
    num_rows = m
    totals = []
    while i < len(operations):
        end = find_end_col(board, col, num_rows)
        operation = operations[i]
        nums = []
        for col in range(col, end):
            nums.append(get_col_num_complex(board, col, num_rows))
        if operation == "*":
            totals.append(prod(nums))
        else:
            totals.append(sum(nums))
        col = end + 1
        i += 1
    return sum(totals)


def main():
    with open("day-6.input.txt", "r") as f:
        data = f.read()

    parsed = parse_input(data)
    board, operations = structure_data(parsed)

    part1_result = solve_part1(board, operations)
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(board, operations)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
