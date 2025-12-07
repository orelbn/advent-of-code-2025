"""
Advent of Code 2025 - Day 7
"""


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


def solve_part1(board: list[str]):
    """
    Solves Part 1.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 1.
    """

    start = board[0].find("S")
    m = len(board)
    n = len(board[0])
    seen = set()

    def traverse(row, col) -> int:
        if row < 0 or row >= m or col < 0 or col >= n or (row, col) in seen:
            return 0
        seen.add((row, col))

        if board[row][col] == "^":
            return 1 + traverse(row, col + 1) + traverse(row, col - 1)
        else:
            return traverse(row + 1, col)

    return traverse(0, start)


def solve_part2(board: list[str]):
    """
    Solves Part 2.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 2.
    """
    start = board[0].find("S")
    m = len(board)
    n = len(board[0])
    mp = {}

    def traverse(row, col) -> int:
        if row < 0 or row >= m or col < 0 or col >= n:
            return 0
        if (row, col) in mp:
            return mp[(row, col)]

        if board[row][col] == "^":
            mp[(row, col)] = 1 + traverse(row, col + 1) + traverse(row, col - 1)
            return mp[(row, col)]
        else:
            mp[(row, col)] = traverse(row + 1, col)
            return mp[((row, col))]

    return traverse(0, start) + 1


def main():
    with open("day-7.input.txt", "r") as f:
        data = f.read()

    parsed = parse_input(data)

    part1_result = solve_part1(parsed)
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(parsed)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
