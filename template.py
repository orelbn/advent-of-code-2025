"""
Advent of Code 2025 - Day X
"""


def parse_input(data: str):
    """
    Parses the raw input data.

    Args:
        data: The raw input string.

    Returns:
        Parsed input data.
    """
    lines = data.strip().splitlines()
    return lines


def structure_data(parsed: list[str]):
    """
    Structures the parsed input data into a more usable format.

    Args:
        parsed: The parsed input data.

    Returns:
        Structured data.
    """
    pass


def solve_part1(data):
    """
    Solves Part 1.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 1.
    """
    pass


def solve_part2(data):
    """
    Solves Part 2.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 2.
    """
    pass


def main():
    with open("day-X.input.txt", "r") as f:
        data = f.read()

    parsed = parse_input(data)
    # structured = structure_data(parsed)

    part1_result = solve_part1(parsed)
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(parsed)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
