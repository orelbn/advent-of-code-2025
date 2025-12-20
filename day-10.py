"""
Advent of Code 2025 - Day 10
"""

from collections import deque
from heapq import heappop, heappush


def parse_input(data: str) -> list[str]:
    """
    Parses the raw input data
    """
    lines = data.strip().splitlines()
    return lines


def transform_to_lights_requirement(lights_str: str) -> list[int]:
    """
    Transforms a lights requirement string into a list of integers.
    """
    res = []
    for ch in lights_str:
        if ch == ".":
            res.append(0)
        elif ch == "#":
            res.append(1)
    return res


def structure_data(parsed: list[str]) -> dict[str, list]:
    """
    Structures the parsed input data into a more usable format.
    """
    lights_requirements: list[int] = []
    change_options: list[list[int]] = []
    joltages_requirements: list[int] = []
    for line in parsed:
        items = line.split()
        lights_requirements.append(transform_to_lights_requirement(items[0]))
        options = []
        for opt in items[1:-1]:
            options.append([int(x) for x in opt.strip("()").split(",")])
        change_options.append(options)
        joltages_requirements.append([int(x) for x in items[-1].strip("{}").split(",")])

    return {
        "lights_requirements": lights_requirements,
        "change_options": change_options,
        "joltages_requirements": joltages_requirements,
    }


def increment_voltages(
    current_voltages: list[int],
    target: list[int],
    switch_options: list[list[int]],
) -> int:
    """
    Uses Dijkstra's algorithm to find the minimum number of moves required
    to reach the target configuration from the current configuration using
    the available switch options.
    """
    if current_voltages == target:
        return 0

    seen: dict[tuple[int, ...], int] = {tuple(current_voltages): 0}
    pq = [(0, current_voltages)]  # (moves, voltages)

    while pq:
        moves, voltages = heappop(pq)

        # Skip if we've already found a better path to this state
        key = tuple(voltages)
        if key in seen and seen[key] < moves:
            continue

        if voltages == target:
            return moves

        for option in switch_options:
            new_voltages = voltages[:]

            # Calculate the maximum increment possible for this option
            needed = [target[idx] - new_voltages[idx] for idx in option]
            increment = min(needed)

            # Skip if increment is non-positive (no progress)
            if increment <= 0:
                continue

            # Apply increment
            for idx in option:
                new_voltages[idx] += increment

            new_key = tuple(new_voltages)
            next_moves = moves + increment

            # Only explore if this is a better path to this state
            if new_key not in seen or seen[new_key] > next_moves:
                seen[new_key] = next_moves
                heappush(pq, (next_moves, new_voltages))

    return float("inf")  # No solution found


def switch_lights(
    current_lights: list[int],
    target: list[int],
    switch_options: list[list[int]],
) -> int:
    """
    Iterative BFS to find the minimum number of moves required to reach the
    target configuration from the current configuration using the available
    switch options. This avoids recursion depth issues and returns the minimal
    moves.
    """
    if current_lights == target:
        return 0

    seen: dict[tuple[int], int] = {tuple(current_lights): 0}
    q = deque()
    q.append((current_lights, 0))

    while q:
        lights, moves = q.popleft()
        for option in switch_options:
            new_lights = lights[:]
            for idx in option:
                new_lights[idx] = 1 - new_lights[idx]
            key = tuple(new_lights)
            next_moves = moves + 1
            if key in seen and seen[key] <= next_moves:
                continue
            if new_lights == target:
                return next_moves
            seen[key] = next_moves
            q.append((new_lights, next_moves))

    return None


def solve_part1(lights_requirements: list[list[int]], change_options: list[list[int]]):
    """
    Solves Part 1.
    """
    total_moves = 0
    for i in range(len(lights_requirements)):
        lights_req = lights_requirements[i]
        options = change_options[i]
        starting_lights = [0] * len(lights_req)
        moves = switch_lights(starting_lights, lights_req, options)
        if moves is not None:
            total_moves += moves

    return total_moves


def solve_part2(
    joltages_requirements: list[list[int]], change_options: list[list[int]]
):
    """
    Solves Part 2.
    """
    total_moves = 0
    for i in range(len(joltages_requirements)):
        joltages_req = joltages_requirements[i]
        options = change_options[i]
        starting_voltages = [0] * len(joltages_req)
        moves = increment_voltages(starting_voltages, joltages_req, options)
        if moves is not None:
            total_moves += moves

    return total_moves


def main():
    with open("day-10.input.txt", "r") as f:
        data = f.read()

    parsed = parse_input(data)
    structured = structure_data(parsed)

    part1_result = solve_part1(
        structured["lights_requirements"], structured["change_options"]
    )
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(
        structured["joltages_requirements"], structured["change_options"]
    )

    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
