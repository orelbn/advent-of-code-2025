"""
Advent of Code 2025 - Day 5: Cafeteria
Find fresh ingredients by checking if IDs fall within given ranges.
"""

from collections.abc import Generator


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


def structure_data(parsed: list[str]) -> tuple[list[str], list[str]]:
    """
    Structures the parsed input data into ranges and ingredient IDs.

    Args:
        parsed: The parsed input data.

    Returns:
        A tuple of (ranges, ingredients) where ranges are the fresh ingredient
        ID ranges and ingredients are the IDs to check.
    """
    separator_idx = parsed.index("")
    ranges = parsed[:separator_idx]
    ingredients = parsed[separator_idx + 1 :]
    return ranges, ingredients


def ranges_to_pairs(ranges: list[str]) -> Generator[tuple[int, int], None, None]:
    """
    Converts range strings to (start, end) integer tuples.

    Args:
        ranges: List of range strings in 'start-end' format (e.g., '3-5').

    Yields:
        Tuples of (start, end) integers for each range.
    """
    for rng in ranges:
        low, high = rng.split("-")
        yield int(low), int(high)


def interval_merge(sorted_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merges overlapping or adjacent intervals from a sorted list of ranges.

    Args:
        sorted_ranges: List of (start, end) tuples, sorted by start value.

    Returns:
        List of merged (start, end) tuples with no overlaps.
    """
    merged = []
    curr = sorted_ranges[0]
    for start, end in sorted_ranges[1:]:
        if curr[1] < start:
            merged.append(curr)
            curr = (start, end)
        else:
            curr = (curr[0], max(curr[1], end))
    merged.append(curr)
    return merged


def solve_part1(ranges: list[str], ingredients: list[str]) -> int:
    """
    Counts how many ingredient IDs are fresh (fall within any range).

    Args:
        ranges: List of range strings like '3-5'.
        ingredients: List of ingredient ID strings to check.

    Returns:
        Number of fresh ingredient IDs.
    """
    range_pairs = list(ranges_to_pairs(ranges))

    fresh_count = 0
    for ingredient_id in ingredients:
        for low, high in range_pairs:
            if low <= int(ingredient_id) <= high:
                fresh_count += 1
                break

    return fresh_count


def solve_part2(ranges: list[str]) -> int:
    """
    Counts total unique IDs considered fresh across all ranges.

    Args:
        ranges: List of range strings like '3-5'.

    Returns:
        Total count of unique fresh ingredient IDs.
    """
    range_pairs = sorted(ranges_to_pairs(ranges))
    merged = interval_merge(range_pairs)
    return sum(end - start + 1 for start, end in merged)


def main():
    """Main entry point."""
    with open("day-5.input.txt") as f:
        data = f.read()

    parsed = parse_input(data)
    ranges, ingredients = structure_data(parsed)

    print(f"Part 1: {solve_part1(ranges, ingredients)}")
    print(f"Part 2: {solve_part2(ranges)}")  # Part 2 ignores ingredients


if __name__ == "__main__":
    main()
