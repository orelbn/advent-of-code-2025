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


def is_repeated_twice(num: int) -> bool:
    """
    Checks if a number is formed by repeating a pattern exactly twice.

    Examples: 11, 1212, 123123 → True
              111, 121212 → False (these repeat more than twice)

    Args:
        num: The number to check.

    Returns:
        True if the number is a pattern repeated exactly twice.
    """
    s = str(num)
    n = len(s)
    if n % 2 != 0:
        return False
    mid = n // 2
    return s[:mid] == s[mid:]


def is_repeated_pattern(num: int) -> bool:
    """
    Checks if a number is formed by repeating a pattern at least twice.

    Examples: 11, 111, 1212, 121212, 123123 → True

    Args:
        num: The number to check.

    Returns:
        True if the number is a repeating pattern.
    """
    s = str(num)
    n = len(s)

    # Try all possible pattern lengths from 1 to n//2
    for pattern_len in range(1, n // 2 + 1):
        if n % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if the entire string is just this pattern repeated
            if pattern * (n // pattern_len) == s:
                return True
    return False


def sum_invalid_ids(ranges: list[tuple[int, int]], is_invalid: callable) -> int:
    """
    Sums all invalid IDs within the given ranges.

    Args:
        ranges: List of (start, end) ranges to check.
        is_invalid: Function that determines if an ID is invalid.

    Returns:
        The sum of all invalid IDs.
    """
    total = 0
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid(num):
                total += num
    return total


def main():
    """Main entry point."""
    with open("day-2.input.txt") as f:
        data = f.read()

    ranges = parse_ranges(data)

    # Part 1: Pattern repeated exactly twice
    part1 = sum_invalid_ids(ranges, is_repeated_twice)
    print(f"Part 1: {part1}")

    # Part 2: Pattern repeated at least twice
    part2 = sum_invalid_ids(ranges, is_repeated_pattern)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
