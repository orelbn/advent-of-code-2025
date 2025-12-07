"""
Advent of Code 2025 - Day 2: Gift Shop
Find invalid product IDs that consist of repeated digit patterns.
"""


def parse_ranges(data: str) -> list[tuple[int, int]]:
    """
    Parses the input string into a list of (start, end) ranges.

    Args:
        data: A comma-separated string of ranges (e.g., "11-22,95-115").

    Returns:
        A list of (start, end) tuples.
    """
    return [
        (int(start), int(end))
        for start, end in (r.split("-") for r in data.strip().split(",") if r)
    ]


def generate_repeated_twice(max_val: int) -> list[int]:
    """
    Generates all numbers that are a pattern repeated exactly twice, sorted.

    Examples: 11, 22, ..., 99, 1010, 1111, ..., 123123, etc.

    Args:
        max_val: Maximum value to generate up to.

    Returns:
        Sorted list of all numbers that are patterns repeated exactly twice.
    """
    result = []
    max_digits = len(str(max_val))

    for pattern_len in range(1, max_digits // 2 + 1):
        start = 10 ** (pattern_len - 1) if pattern_len > 1 else 1
        end = 10**pattern_len

        for pattern in range(start, end):
            repeated = int(str(pattern) * 2)
            if repeated > max_val:
                break
            result.append(repeated)

    return result


def generate_repeated_pattern(max_val: int) -> list[int]:
    """
    Generates all numbers that are a pattern repeated at least twice, sorted.

    Examples: 11, 111, 1111, 1212, 121212, 123123, etc.

    Args:
        max_val: Maximum value to generate up to.

    Returns:
        Sorted list of all numbers that are patterns repeated at least twice.
    """
    result = set()
    max_digits = len(str(max_val))

    for pattern_len in range(1, max_digits // 2 + 1):
        start = 10 ** (pattern_len - 1) if pattern_len > 1 else 1
        end = 10**pattern_len

        for pattern in range(start, end):
            pattern_str = str(pattern)
            for repeats in range(2, max_digits // pattern_len + 1):
                repeated = int(pattern_str * repeats)
                if repeated > max_val:
                    break
                result.add(repeated)

    return sorted(result)


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merges overlapping or adjacent ranges.

    Args:
        ranges: List of (start, end) ranges.

    Returns:
        Sorted list of merged non-overlapping ranges.
    """
    if not ranges:
        return []
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        if merged[-1][1] >= start - 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def sum_invalid_in_ranges(
    merged_ranges: list[tuple[int, int]], sorted_invalid: list[int]
) -> int:
    """
    Sums all invalid IDs within the given merged ranges.

    Args:
        merged_ranges: Sorted list of non-overlapping (start, end) ranges.
        sorted_invalid: Sorted list of all invalid IDs.

    Returns:
        The sum of all invalid IDs that fall within any range.
    """
    total = 0
    range_idx = 0

    for num in sorted_invalid:
        # Skip ranges that are completely before this number
        while range_idx < len(merged_ranges) and merged_ranges[range_idx][1] < num:
            range_idx += 1
        if range_idx >= len(merged_ranges):
            break
        # Check if num falls within current range
        if merged_ranges[range_idx][0] <= num <= merged_ranges[range_idx][1]:
            total += num

    return total


def solve_part1(merged_ranges: list[tuple[int, int]], max_val: int) -> int:
    """
    Finds sum of IDs that are patterns repeated exactly twice.

    Args:
        merged_ranges: Sorted list of non-overlapping ranges.
        max_val: Maximum value across all ranges.

    Returns:
        Sum of invalid IDs.
    """
    invalid_set = generate_repeated_twice(max_val)
    return sum_invalid_in_ranges(merged_ranges, invalid_set)


def solve_part2(merged_ranges: list[tuple[int, int]], max_val: int) -> int:
    """
    Finds sum of IDs that are patterns repeated at least twice.

    Args:
        merged_ranges: Sorted list of non-overlapping ranges.
        max_val: Maximum value across all ranges.

    Returns:
        Sum of invalid IDs.
    """
    invalid_set = generate_repeated_pattern(max_val)
    return sum_invalid_in_ranges(merged_ranges, invalid_set)


def main():
    """Main entry point."""
    with open("day-2.input.txt") as f:
        data = f.read()

    ranges = parse_ranges(data)
    merged_ranges = merge_ranges(ranges)
    max_val = max(end for _, end in ranges)

    print(f"Part 1: {solve_part1(merged_ranges, max_val)}")
    print(f"Part 2: {solve_part2(merged_ranges, max_val)}")


if __name__ == "__main__":
    main()
