"""
Advent of Code 2025 - Day X
"""

from collections import deque


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
        joltages_requirements.append(items[-1])

    return {
        "lights_requirements": lights_requirements,
        "change_options": change_options,
        "joltages_requirements": joltages_requirements,
    }


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


def solve_part1(lights_requirements: list[int], change_options: list[list[int]]):
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


def solve_part2(data):
    """
    Solves Part 2.
    """
    pass


def main():
    with open("day-10.input.txt", "r") as f:
        data = f.read()

    parsed = parse_input(data)
    structured = structure_data(parsed)

    part1_result = solve_part1(
        structured["lights_requirements"], structured["change_options"]
    )
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(structured)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
