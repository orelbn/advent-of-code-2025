"""
Advent of Code 2025 - Day 8
"""

from collections import Counter
import heapq
import math


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


def structure_data(parsed: list[str]) -> list[tuple[int, int, int]]:
    """
    Structures the parsed input data into a more usable format.

    Args:
        parsed: The parsed input data.

    Returns:
        Structured data.
    """
    junction_boxes = []
    for line in parsed:
        x, y, z = map(int, line.split(","))
        junction_boxes.append((x, y, z))
    return junction_boxes


def calculate_3d_euclidan_distance(p: tuple[int, int, int], q: tuple[int, int, int]):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2) ** 0.5


# Might be able to use disjoint sets here.
def solve_part1(junction_boxes: list[tuple[int, int, int]], closest_n: int):
    """
    Solves Part 1.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 1.
    """
    closet = []
    n = len(junction_boxes)
    for i in range(n - 1):
        for j in range(i + 1, n):
            distance = math.dist(junction_boxes[i], junction_boxes[j])
            if len(closet) < closest_n:
                heapq.heappush(closet, (-distance, (i, j)))
            else:
                furthest_in_heap = closet[0][0]
                if -furthest_in_heap < distance:
                    continue
                heapq.heappop(closet)
                heapq.heappush(closet, (-distance, (i, j)))

    clusters = {}
    while closet:
        distance, idx = heapq.heappop(closet)
        if idx[0] in clusters and not idx[1] in clusters:
            clusters[idx[1]] = clusters[clusters[idx[0]]]
        elif idx[1] in clusters and not idx[0] in clusters:
            clusters[idx[0]] = clusters[clusters[idx[1]]]
        elif idx[1] in clusters and idx[0] in clusters:
            curr = idx[0]
            while clusters[curr] != curr:
                curr = clusters[curr]
            root1 = curr
            curr = idx[1]
            while clusters[curr] != curr:
                curr = clusters[curr]
            root2 = curr
            clusters[root2] = root1

        else:
            clusters[idx[0]] = idx[0]
            clusters[idx[1]] = idx[0]

    def update_root(key: int) -> int:
        if key == clusters[key]:
            return key

        clusters[key] = update_root(clusters[key])
        return clusters[key]

    for key in clusters.keys():
        update_root(key)

    values_count = Counter(clusters.values())
    counts = list(values_count.values())
    counts.sort()
    top_3 = counts[-3:]
    return math.prod(top_3)


def solve_part2(junction_boxes: list[tuple[int, int, int]]):
    """
    Solves Part 2.

    Args:
        data: The structured input data.

    Returns:
        Solution to Part 2.
    """
    closet = []
    n = len(junction_boxes)
    for i in range(n - 1):
        for j in range(i + 1, n):
            distance = math.dist(junction_boxes[i], junction_boxes[j])
            heapq.heappush(closet, (distance, (i, j)))

    clusters = {}

    def update_root(key: int) -> int:
        if key == clusters[key]:
            return key

        clusters[key] = update_root(clusters[key])
        return clusters[key]

    last_joined = None

    while len(clusters) != len(junction_boxes) or len(set(clusters.values())) != 1:
        distance, idx = heapq.heappop(closet)
        last_joined = idx
        if idx[0] in clusters and not idx[1] in clusters:
            clusters[idx[1]] = clusters[clusters[idx[0]]]
        elif idx[1] in clusters and not idx[0] in clusters:
            clusters[idx[0]] = clusters[clusters[idx[1]]]
        elif idx[1] in clusters and idx[0] in clusters:
            curr = idx[0]
            while clusters[curr] != curr:
                curr = clusters[curr]
            root1 = curr
            curr = idx[1]
            while clusters[curr] != curr:
                curr = clusters[curr]
            root2 = curr
            clusters[root2] = root1
            for key in clusters.keys():
                update_root(key)
        else:
            clusters[idx[0]] = idx[0]
            clusters[idx[1]] = idx[0]

    return junction_boxes[last_joined[0]][0] * junction_boxes[last_joined[1]][0]


def main():
    with open("day-8.input.txt", "r") as f:
        data = f.read()

    parsed = parse_input(data)
    # Junction boxes POS (X,Y,Z) in 3d space
    # Want closet possible in 3D euclidan distance
    junction_boxes = structure_data(parsed)

    part1_result = solve_part1(junction_boxes, 1000)
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(junction_boxes)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
