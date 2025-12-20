"""
Advent of Code 2025 - Day 10: Factory
Configure indicator lights and joltage levels for factory machines.
"""

# uses uv script declaration https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies
# /// script
# dependencies = [
#   "z3-solver",
# ]
# ///
from collections import deque
import z3


def parse_input(data: str) -> list[str]:
    """
    Parses raw input lines.

    Args:
        data: Raw puzzle input.

    Returns:
        List of input lines, one per machine.
    """
    return data.strip().splitlines()


def parse_lights_diagram(diagram: str) -> list[int]:
    """
    Converts indicator light diagram to binary list.

    Args:
        diagram: String like ".##." where . = off, # = on.

    Returns:
        Binary list where 0 = off, 1 = on.
    """
    return [1 if ch == "#" else 0 for ch in diagram]


def structure_data(lines: list[str]) -> dict[str, list]:
    """
    Structures parsed input into usable format.

    Each line format: [lights] (btn1) (btn2) ... {joltages}
    Example: [.##.] (3) (1,3) (2) {3,5,4,7}

    Args:
        lines: Raw input lines.

    Returns:
        Dictionary with:
        - lights_diagrams: Target indicator states for each machine
        - button_configs: Button wirings for each machine
        - joltage_targets: Target joltage levels for each machine
    """
    lights_diagrams: list[list[int]] = []
    button_configs: list[list[list[int]]] = []
    joltage_targets: list[list[int]] = []

    for line in lines:
        parts = line.split()

        lights_diagrams.append(parse_lights_diagram(parts[0].strip("[]")))

        buttons = []
        for part in parts[1:-1]:
            button_indices = [int(x) for x in part.strip("()").split(",")]
            buttons.append(button_indices)
        button_configs.append(buttons)

        joltages = [int(x) for x in parts[-1].strip("{}").split(",")]
        joltage_targets.append(joltages)

    return {
        "lights_diagrams": lights_diagrams,
        "button_configs": button_configs,
        "joltage_targets": joltage_targets,
    }


def find_min_button_presses_lights(
    target: list[int],
    buttons: list[list[int]],
) -> int:
    """
    Finds minimum button presses to configure indicator lights using BFS.

    Each button toggles specific lights between on/off. Lights start all off.

    Args:
        target: Desired light configuration (binary list).
        buttons: List of button configurations, each containing indices to toggle.

    Returns:
        Minimum number of button presses, or None if impossible.
    """
    num_lights = len(target)
    initial = [0] * num_lights

    if initial == target:
        return 0

    seen: dict[tuple[int, ...], int] = {tuple(initial): 0}
    queue = deque([(initial, 0)])

    while queue:
        lights, presses = queue.popleft()

        for button in buttons:
            new_lights = lights[:]
            for idx in button:
                new_lights[idx] = 1 - new_lights[idx]

            state = tuple(new_lights)
            next_presses = presses + 1

            if state in seen and seen[state] <= next_presses:
                continue

            if new_lights == target:
                return next_presses

            seen[state] = next_presses
            queue.append((new_lights, next_presses))

    return None


def find_min_button_presses_joltage(
    targets: list[int],
    buttons: list[list[int]],
) -> int:
    """
    Finds minimum button presses to reach target joltage levels using Z3.

    Each button press increases specific counter values by 1. Counters start at 0.

    Args:
        targets: Target joltage values for each counter.
        buttons: Button configurations (which counters each button affects).

    Returns:
        Minimum total button presses, or None if impossible.
    """
    num_buttons = len(buttons)

    optimizer = z3.Optimize()
    press_counts = [z3.Int(f"button_{i}") for i in range(num_buttons)]

    for count in press_counts:
        optimizer.add(count >= 0)

    for counter_idx, target_value in enumerate(targets):
        contributions = sum(
            (
                press_counts[btn_idx]
                for btn_idx, button in enumerate(buttons)
                if counter_idx in button
            ),
            z3.IntVal(0),
        )
        optimizer.add(contributions == target_value)

    optimizer.minimize(sum(press_counts))

    if optimizer.check() == z3.sat:
        model = optimizer.model()
        return sum(model.eval(count).as_long() for count in press_counts)

    return None


def solve_part1(
    lights_diagrams: list[list[int]],
    button_configs: list[list[list[int]]],
) -> int:
    """
    Solves Part 1: Configure indicator lights for all machines.

    Args:
        lights_diagrams: Target light configurations for each machine.
        button_configs: Button wirings for each machine.

    Returns:
        Total minimum button presses across all machines.
    """
    total_presses = 0

    for target, buttons in zip(lights_diagrams, button_configs):
        presses = find_min_button_presses_lights(target, buttons)
        if presses is not None:
            total_presses += presses

    return total_presses


def solve_part2(
    joltage_targets: list[list[int]],
    button_configs: list[list[list[int]]],
) -> int:
    """
    Solves Part 2: Configure joltage levels for all machines.

    Args:
        joltage_targets: Target joltage values for each machine.
        button_configs: Button wirings for each machine.

    Returns:
        Total minimum button presses across all machines.
    """
    total_presses = 0

    for targets, buttons in zip(joltage_targets, button_configs):
        presses = find_min_button_presses_joltage(targets, buttons)
        if presses is not None:
            total_presses += presses

    return total_presses


def main():
    """Main entry point."""
    with open("day-10.input.txt") as f:
        data = f.read()

    lines = parse_input(data)
    structured = structure_data(lines)

    part1_result = solve_part1(
        structured["lights_diagrams"],
        structured["button_configs"],
    )
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(
        structured["joltage_targets"],
        structured["button_configs"],
    )
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
