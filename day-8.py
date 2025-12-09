"""
Advent of Code 2025 - Day 8: Playground
Connect the closest junction boxes in 3D space.
"""

from collections import Counter
import heapq
import math


def parse_input(data: str) -> list[tuple[int, int, int]]:
    """
    Parses raw input lines into 3D coordinates.

    Args:
        data: Raw puzzle input.

    Returns:
        List of (x, y, z) tuples representing junction boxes.
    """
    boxes = []
    for line in data.strip().splitlines():
        x, y, z = map(int, line.split(","))
        boxes.append((x, y, z))
    return boxes


def build_k_smallest_edges(
    junction_boxes: list[tuple[int, int, int]],
    k: int,
) -> list[tuple[float, int, int]]:
    """
    Builds only the k smallest edges using a max-heap of size k.

    Args:
        junction_boxes: Coordinates of each junction box.
        k: Number of smallest edges to return.

    Returns:
        List of (distance, i, j) edges sorted by distance.
    """
    n = len(junction_boxes)
    max_heap: list[tuple[float, int, int]] = []

    for i in range(n - 1):
        pi = junction_boxes[i]
        for j in range(i + 1, n):
            dist = math.dist(pi, junction_boxes[j])
            if len(max_heap) < k:
                heapq.heappush(max_heap, (-dist, i, j))
            elif -dist > max_heap[0][0]:
                heapq.heapreplace(max_heap, (-dist, i, j))

    result = [(-d, i, j) for d, i, j in max_heap]
    result.sort(key=lambda x: x[0])
    return result


def find_root(parent: list[int], x: int) -> int:
    """Finds set representative with path compression."""
    if parent[x] != x:
        parent[x] = find_root(parent, parent[x])
    return parent[x]


def union(parent: list[int], size: list[int], a: int, b: int) -> bool:
    """Unites the sets of a and b; returns True if merged."""
    ra, rb = find_root(parent, a), find_root(parent, b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True


def solve_part1(junction_boxes: list[tuple[int, int, int]], closest_n: int) -> int:
    """
    Processes the first `closest_n` closest pairs and returns
    the product of the sizes of the 3 largest resulting circuits.

    Args:
        junction_boxes: Coordinates of each junction box.
        closest_n: Number of closest pairs to consider.

    Returns:
        Product of the sizes of the three largest circuits.
    """
    n = len(junction_boxes)
    parent = list(range(n))
    size = [1] * n

    edges = build_k_smallest_edges(junction_boxes, closest_n)
    for _, a, b in edges:
        union(parent, size, a, b)

    components = Counter(find_root(parent, i) for i in range(n))
    largest = sorted(components.values())[-3:]
    return math.prod(largest)


def solve_part2(junction_boxes: list[tuple[int, int, int]]) -> int:
    """
    Builds MST using Prim's algorithm and returns the product
    of the X coordinates of the final edge added.

    Args:
        junction_boxes: Coordinates of each junction box.

    Returns:
        Product of the X coordinates of the final connection.
    """
    n = len(junction_boxes)
    if n <= 1:
        return 0

    INF = float("inf")
    in_mst = [False] * n
    min_dist = [INF] * n
    min_from = [0] * n

    in_mst[0] = True
    last_edge = (0, 0)
    p0 = junction_boxes[0]

    for j in range(1, n):
        min_dist[j] = math.dist(p0, junction_boxes[j])

    for _ in range(n - 1):
        best_dist = INF
        best_node = -1
        for j in range(n):
            if not in_mst[j] and min_dist[j] < best_dist:
                best_dist = min_dist[j]
                best_node = j

        if best_node == -1:
            break

        in_mst[best_node] = True
        last_edge = (min_from[best_node], best_node)

        pb = junction_boxes[best_node]
        for j in range(n):
            if not in_mst[j]:
                d = math.dist(pb, junction_boxes[j])
                if d < min_dist[j]:
                    min_dist[j] = d
                    min_from[j] = best_node

    ax, _, _ = junction_boxes[last_edge[0]]
    bx, _, _ = junction_boxes[last_edge[1]]
    return ax * bx


def main():
    """Main entry point."""
    with open("day-8.input.txt") as f:
        data = f.read()

    junction_boxes = parse_input(data)

    print(f"Part 1: {solve_part1(junction_boxes, 1000)}")
    print(f"Part 2: {solve_part2(junction_boxes)}")


if __name__ == "__main__":
    main()
