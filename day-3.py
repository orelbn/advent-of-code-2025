"""
Advent of Code 2025 - Day 3: Lobby
Power the escalator by finding maximum joltage from battery banks.
"""

from bisect import bisect_right


def parse_input(data: str) -> list[str]:
    """
    Parses the raw input data.

    Args:
        data: The raw input string.

    Returns:
        List of battery banks, where each bank is a string of digits.
    """
    return data.strip().splitlines()


def max_joltage(battery_bank: str, num_batteries: int) -> int:
    """
    Finds the largest number that can be formed by selecting `num_batteries` digits
    from the battery bank while maintaining their original order.

    Args:
        battery_bank: String of digits representing battery joltages.
        num_batteries: Number of batteries (digits) to select.

    Returns:
        The largest number that can be formed.
    """
    n = len(battery_bank)

    # digit_indices[d] = list of indices where digit d appears
    # Index 9 = digit 9, Index 8 = digit 8, etc.
    digit_indices: list[list[int]] = [[] for _ in range(10)]
    for i, d in enumerate(battery_bank):
        digit_indices[int(d)].append(i)

    result = 0
    last_index = -1

    for i in range(num_batteries):
        digits_remaining = num_batteries - i
        max_valid_index = n - digits_remaining

        # Remove exhausted digit lists from the end (last index <= last_index)
        while digit_indices and (
            not digit_indices[-1] or digit_indices[-1][-1] <= last_index
        ):
            digit_indices.pop()

        # Find highest digit with valid index
        digit = len(digit_indices) - 1
        while digit >= 0:
            indices = digit_indices[digit]
            pos = bisect_right(indices, last_index)
            if pos < len(indices) and indices[pos] <= max_valid_index:
                result = result * 10 + digit
                last_index = indices[pos]
                break
            digit -= 1

    return result


def solve_part1(battery_banks: list[str]) -> int:
    """
    Finds total joltage when selecting 2 batteries from each bank.

    Args:
        battery_banks: List of battery bank strings.

    Returns:
        Sum of maximum joltages from each bank.
    """
    return sum(max_joltage(bank, 2) for bank in battery_banks)


def solve_part2(battery_banks: list[str]) -> int:
    """
    Finds total joltage when selecting 12 batteries from each bank.

    Args:
        battery_banks: List of battery bank strings.

    Returns:
        Sum of maximum joltages from each bank.
    """
    return sum(max_joltage(bank, 12) for bank in battery_banks)


def main():
    """Main entry point."""
    with open("day-3.input.txt") as f:
        data = f.read()

    parsed = parse_input(data)

    print(f"Part 1: {solve_part1(parsed)}")
    print(f"Part 2: {solve_part2(parsed)}")


if __name__ == "__main__":
    main()
