"""
Advent of Code 2025 - Day 7: Laboratories
Analyze tachyon beam splitting through a quantum manifold.
"""


def parse_input(data: str) -> list[str]:
    """
    Parses the raw input data into a manifold diagram.

    Args:
        data: The raw input string.

    Returns:
        List of strings representing the manifold rows.
    """
    return data.strip().splitlines()


def solve_part1(manifold: list[str]) -> int:
    """
    Counts total beam splits in the manifold.

    Tachyon beams move downward and split at '^' splitters,
    creating new beams going left and right. Uses a set to
    track visited positions and avoid counting merged beams.

    Args:
        manifold: The manifold diagram.

    Returns:
        Total number of times beams are split.
    """
    start_col = manifold[0].find("S")
    rows = len(manifold)
    cols = len(manifold[0])
    visited = set()

    def traverse(row: int, col: int) -> int:
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return 0
        if (row, col) in visited:
            return 0
        visited.add((row, col))

        if manifold[row][col] == "^":
            return 1 + traverse(row, col + 1) + traverse(row, col - 1)
        return traverse(row + 1, col)

    return traverse(0, start_col)


def solve_part2(manifold: list[str]) -> int:
    """
    Counts total timelines using many-worlds interpretation.

    Each splitter creates two timelines (left and right paths).
    Uses memoization to count paths efficiently, as the same
    position can be reached via different timeline branches.

    Args:
        manifold: The manifold diagram.

    Returns:
        Total number of timelines after particle completes all journeys.
    """
    start_col = manifold[0].find("S")
    rows = len(manifold)
    cols = len(manifold[0])
    memo = {}

    def traverse(row: int, col: int) -> int:
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return 0
        if (row, col) in memo:
            return memo[(row, col)]

        if manifold[row][col] == "^":
            result = 1 + traverse(row, col + 1) + traverse(row, col - 1)
        else:
            result = traverse(row + 1, col)

        memo[(row, col)] = result
        return result

    return traverse(0, start_col) + 1


def main():
    """Main entry point."""
    with open("day-7.input.txt") as f:
        data = f.read()

    manifold = parse_input(data)

    print(f"Part 1: {solve_part1(manifold)}")
    print(f"Part 2: {solve_part2(manifold)}")


if __name__ == "__main__":
    main()
