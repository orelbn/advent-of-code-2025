"""
Advent of Code 2025 - Day 1: Secret Entrance
Simulate a dial on a safe to find the password based on rotations.
"""

DIAL_SIZE = 100
STARTING_POSITION = 50


def parse_instruction(instruction: str) -> tuple[str, int]:
    """
    Parses an instruction string into direction and distance.

    Args:
        instruction: A string like "L68" or "R48".

    Returns:
        A tuple of (direction, distance).
    """
    return instruction[0], int(instruction[1:])


def rotate(position: int, direction: str, distance: int) -> int:
    """
    Rotates the dial and returns the new position.

    Args:
        position: Current dial position (0-99).
        direction: "L" for left (subtract) or "R" for right (add).
        distance: Number of clicks to rotate.

    Returns:
        The new dial position after rotation.
    """
    if direction == "R":
        position += distance
    elif direction == "L":
        position -= distance
    return position % DIAL_SIZE


def count_zeros_crossed(position: int, direction: str, distance: int) -> int:
    """
    Counts how many times the dial passes through 0 during a rotation.

    This counts every time the dial clicks onto position 0, whether
    it ends there or just passes through.

    Args:
        position: Current dial position before rotation.
        direction: "L" for left or "R" for right.
        distance: Number of clicks to rotate.

    Returns:
        The number of times 0 is visited during this rotation.
    """
    if direction == "R":
        # Moving right: count multiples of DIAL_SIZE crossed
        # from (position + 1) to (position + distance)
        return (position + distance) // DIAL_SIZE - position // DIAL_SIZE
    elif direction == "L":
        # Moving left: count multiples of DIAL_SIZE crossed
        # from (position - 1) down to (position - distance)
        return (position - 1) // DIAL_SIZE - (position - distance - 1) // DIAL_SIZE
    return 0


def solve_part1(instructions: list[str]) -> int:
    """
    Counts how many times the dial ends at 0 after a rotation.

    Args:
        instructions: List of rotation instructions.

    Returns:
        Number of times the dial points at 0 after any rotation.
    """
    position = STARTING_POSITION
    count = 0

    for instruction in instructions:
        direction, distance = parse_instruction(instruction)
        position = rotate(position, direction, distance)
        if position == 0:
            count += 1

    return count


def solve_part2(instructions: list[str]) -> int:
    """
    Counts how many times the dial passes through or lands on 0.

    Args:
        instructions: List of rotation instructions.

    Returns:
        Total number of times the dial points at 0 during all rotations.
    """
    position = STARTING_POSITION
    total = 0

    for instruction in instructions:
        direction, distance = parse_instruction(instruction)
        total += count_zeros_crossed(position, direction, distance)
        position = rotate(position, direction, distance)

    return total


def main():
    """Main entry point."""
    with open("day-1.input.txt") as f:
        instructions = f.read().splitlines()

    part1 = solve_part1(instructions)
    print(f"Part 1: {part1}")

    part2 = solve_part2(instructions)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
