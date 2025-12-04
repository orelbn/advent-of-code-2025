"""
Advent of Code 2025 - Day 4: Printing Department
Optimize forklift work to access paper rolls in the printing department.
"""

PAPER_ROLL = "@"
CLEAR = "."
MAX_ADJACENT_FOR_ACCESS = 4


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


def structure_data(parsed: list[str]) -> list[list[str]]:
    """
    Structures the parsed input data into a more usable format.

    Args:
        parsed: The parsed input data.

    Returns:
        Structured data.
    """
    structured = [list(line) for line in parsed]
    return structured


def find_adjacent_papers(
    paper_grid: list[list[str]], row: int, col: int
) -> list[tuple[int, int]]:
    """
    Finds paper rolls in the 8 adjacent cells (excluding center).

    Args:
        paper_grid: 2D grid of paper rolls and clear spaces.
        row: Row index of the cell.
        col: Column index of the cell.

    Returns:
        List of (row, col) positions of adjacent paper rolls.
    """
    rows = len(paper_grid)
    cols = len(paper_grid[0])

    has_row_above = row - 1 >= 0
    has_row_below = row + 1 < rows
    has_col_left = col - 1 >= 0
    has_col_right = col + 1 < cols

    adjacent_rows = [row]
    if has_row_above:
        adjacent_rows.append(row - 1)
    if has_row_below:
        adjacent_rows.append(row + 1)

    adjacent_cols = [col]
    if has_col_left:
        adjacent_cols.append(col - 1)
    if has_col_right:
        adjacent_cols.append(col + 1)

    adjacent_papers = []
    for r in adjacent_rows:
        for c in adjacent_cols:
            is_center = r == row and c == col
            if not is_center and paper_grid[r][c] == PAPER_ROLL:
                adjacent_papers.append((r, c))

    return adjacent_papers


def solve_part1(paper_grid: list[list[str]]) -> int:
    """
    Counts paper rolls that are accessible by forklift.
    A paper roll is accessible if it has fewer than 4 adjacent paper rolls.

    Args:
        paper_grid: 2D grid of paper rolls and clear spaces.

    Returns:
        Number of accessible paper rolls.
    """
    rows = len(paper_grid)
    cols = len(paper_grid[0])

    accessible_count = 0
    for row in range(rows):
        for col in range(cols):
            is_paper_roll = paper_grid[row][col] == PAPER_ROLL
            adjacent_papers = find_adjacent_papers(paper_grid, row, col)
            is_accessible = len(adjacent_papers) < MAX_ADJACENT_FOR_ACCESS
            if is_paper_roll and is_accessible:
                accessible_count += 1

    return accessible_count


def solve_part2(paper_grid: list[list[str]]) -> int:
    """
    Counts total paper rolls that can be removed by repeatedly removing accessible ones.
    A paper roll is accessible if it has fewer than 4 adjacent paper rolls.
    Removing a roll may make adjacent rolls accessible.

    Args:
        paper_grid: 2D grid of paper rolls and clear spaces.

    Returns:
        Total number of paper rolls that can be removed.
    """
    rows = len(paper_grid)
    cols = len(paper_grid[0])

    accessible_count = 0
    candidates = set()
    for row in range(rows):
        for col in range(cols):
            is_paper_roll = paper_grid[row][col] == PAPER_ROLL
            adjacent_papers = find_adjacent_papers(paper_grid, row, col)
            is_accessible = len(adjacent_papers) < MAX_ADJACENT_FOR_ACCESS
            if is_paper_roll and is_accessible:
                accessible_count += 1
                candidates.add((row, col))
                paper_grid[row][col] = CLEAR
                for r, c in adjacent_papers:
                    candidates.add((r, c))

    while candidates:
        row, col = candidates.pop()
        is_paper_roll = paper_grid[row][col] == PAPER_ROLL
        adjacent_papers = find_adjacent_papers(paper_grid, row, col)
        is_accessible = len(adjacent_papers) < MAX_ADJACENT_FOR_ACCESS
        if is_paper_roll and is_accessible:
            accessible_count += 1
            paper_grid[row][col] = CLEAR
            for r, c in adjacent_papers:
                candidates.add((r, c))

    return accessible_count


def main():
    """Main entry point."""
    with open("day-4.input.txt") as f:
        data = f.read()

    parsed = parse_input(data)
    paper_grid = structure_data(parsed)

    print(f"Part 1: {solve_part1(paper_grid)}")
    print(f"Part 2: {solve_part2(paper_grid)}")


if __name__ == "__main__":
    main()
