"""
Advent of Code 2025 - Day 5: Cafeteria
Find fresh ingredients by checking if IDs fall within given ranges.
"""

import bisect


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


def is_in_ranges(value: int, merged_ranges: list[tuple[int, int]]) -> bool:
    """
    Checks if a value falls within any of the merged ranges using binary search.

    Args:
        value: The integer value to check.
        merged_ranges: Sorted, non-overlapping list of (start, end) tuples.

    Returns:
        True if value is within any range, False otherwise.
    """
    # Find the rightmost range where start <= value
    idx = bisect.bisect_right(merged_ranges, (value, float("inf"))) - 1
    if idx >= 0:
        start, end = merged_ranges[idx]
        return start <= value <= end
    return False


def solve_part1(merged_ranges: list[tuple[int, int]], ingredients: list[int]) -> int:
    """
    Counts how many ingredient IDs are fresh (fall within any range).

    Args:
        merged_ranges: Sorted, merged list of (start, end) tuples.
        ingredients: List of ingredient IDs as integers.

    Returns:
        Number of fresh ingredient IDs.
    """
    return sum(1 for ing in ingredients if is_in_ranges(ing, merged_ranges))


def solve_part2(merged_ranges: list[tuple[int, int]]) -> int:
    """
    Counts total unique IDs considered fresh across all ranges.

    Args:
        merged_ranges: Sorted, merged list of (start, end) tuples.

    Returns:
        Total count of unique fresh ingredient IDs.
    """
    return sum(end - start + 1 for start, end in merged_ranges)


def main():
    """Main entry point."""
    with open("day-5.input.txt") as f:
        data = f.read()

    parsed = parse_input(data)
    ranges, ingredients = structure_data(parsed)

    range_pairs = sorted(
        (int(low), int(high)) for rng in ranges for low, high in [rng.split("-")]
    )
    merged_ranges = interval_merge(range_pairs)
    ingredient_ids = [int(ing) for ing in ingredients]

    print(f"Part 1: {solve_part1(merged_ranges, ingredient_ids)}")
    print(f"Part 2: {solve_part2(merged_ranges)}")


if __name__ == "__main__":
    main()
