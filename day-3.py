"""
Advent of Code 2025 - Day 3: Lobby
Power the escalator by finding maximum joltage from battery banks.
"""


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

    Uses a greedy linear scan approach: for each position in the result, find the
    highest digit that leaves enough remaining digits to complete the selection.

    Args:
        battery_bank: String of digits representing battery joltages.
        num_batteries: Number of batteries (digits) to select.

    Returns:
        The largest number that can be formed.
    """
    n = len(battery_bank)
    result = 0
    last_index = -1

    for i in range(num_batteries):
        digits_remaining = num_batteries - i
        max_valid_index = n - digits_remaining

        best_digit = -1
        best_index = -1

        for j in range(last_index + 1, max_valid_index + 1):
            digit = int(battery_bank[j])
            if digit > best_digit:
                best_digit = digit
                best_index = j
                if digit == 9:
                    break

        result = result * 10 + best_digit
        last_index = best_index

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
