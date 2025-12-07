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
    creating new beams going left and right. Processes bottom-up
    iteratively, tracking which cells are reached by any beam.

    Args:
        manifold: The manifold diagram.

    Returns:
        Total number of times beams are split.
    """
    rows = len(manifold)
    cols = len(manifold[0])

    # reached[col] = True if a beam reaches this column from above
    reached = [False] * cols
    reached[manifold[0].find("S")] = True

    total_splits = 0

    for row in range(rows):
        next_reached = [False] * cols
        for col in range(cols):
            if not reached[col]:
                continue
            if manifold[row][col] == "^":
                total_splits += 1
                if col > 0:
                    next_reached[col - 1] = True
                if col < cols - 1:
                    next_reached[col + 1] = True
            else:
                next_reached[col] = True
        reached = next_reached

    return total_splits


def solve_part2(manifold: list[str]) -> int:
    """
    Counts total timelines using many-worlds interpretation.

    Each splitter creates two timelines (left and right paths).
    Processes bottom-up iteratively, counting paths to each cell.

    Args:
        manifold: The manifold diagram.

    Returns:
        Total number of timelines after particle completes all journeys.
    """
    rows = len(manifold)
    cols = len(manifold[0])

    # paths[col] = number of timeline paths reaching this column
    paths = [0] * cols
    paths[manifold[0].find("S")] = 1

    total_timelines = 1  # Start with 1 for the initial timeline

    for row in range(rows):
        next_paths = [0] * cols
        for col in range(cols):
            if paths[col] == 0:
                continue
            if manifold[row][col] == "^":
                total_timelines += paths[col]
                if col > 0:
                    next_paths[col - 1] += paths[col]
                if col < cols - 1:
                    next_paths[col + 1] += paths[col]
            else:
                next_paths[col] += paths[col]
        paths = next_paths

    return total_timelines


def main():
    """Main entry point."""
    with open("day-7.input.txt") as f:
        data = f.read()

    manifold = parse_input(data)

    print(f"Part 1: {solve_part1(manifold)}")
    print(f"Part 2: {solve_part2(manifold)}")


if __name__ == "__main__":
    main()
