"""Advent of Code 2025 - Day 9."""

from __future__ import annotations

from bisect import bisect_left
from collections import defaultdict


def parse_input(data: str) -> list[tuple[int, int]]:
    """
    Parse the raw input into a list of coordinates.

    Args:
        data: The raw input string.

    Returns:
        A list of (x, y) integer coordinates.
    """
    lines = data.strip().splitlines()
    coords = [tuple(map(int, line.split(","))) for line in lines]
    return coords


def rect_area(cord1: tuple[int, int], cord2: tuple[int, int]) -> int:
    """Return the inclusive area of the axis-aligned rectangle between two tiles."""
    return (abs(cord1[0] - cord2[0]) + 1) * (abs(cord1[1] - cord2[1]) + 1)


def solve_part1(coords: list[tuple[int, int]]) -> int:
    """
    Solves Part 1.

    Args:
        data: The structured input data.

    Returns:
        The maximum rectangle area using any two red tiles as opposite corners.
    """
    max_rect_area = 0
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            max_rect_area = max(max_rect_area, rect_area(coords[i], coords[j]))

    return max_rect_area


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge inclusive integer intervals.

    Args:
        intervals: List of (start, end) inclusive intervals.

    Returns:
        A sorted list of merged inclusive intervals.
    """
    if not intervals:
        return []
    intervals = sorted(intervals)
    merged: list[tuple[int, int]] = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def interval_contains(merged: list[tuple[int, int]], value: int) -> bool:
    """Return True if value is contained in any merged inclusive interval."""
    lo = 0
    hi = len(merged) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        start, end = merged[mid]
        if value < start:
            hi = mid - 1
        elif value > end:
            lo = mid + 1
        else:
            return True
    return False


def build_edges(coords: list[tuple[int, int]]):
    """Convert consecutive points into axis-aligned edges.

    Returns:
        (vertical_edges, horizontal_edges)

        vertical_edges: list of (x, y_min, y_max)
        horizontal_edges: list of (y, x_min, x_max)
    """
    vertical_edges: list[tuple[int, int, int]] = []  # (x, y_min, y_max)
    horizontal_edges: list[tuple[int, int, int]] = []  # (y, x_min, x_max)

    n = len(coords)
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        if x1 == x2:
            vertical_edges.append((x1, min(y1, y2), max(y1, y2)))
        elif y1 == y2:
            horizontal_edges.append((y1, min(x1, x2), max(x1, x2)))
        else:
            raise ValueError("Non-orthogonal segment in input")

    return vertical_edges, horizontal_edges


def get_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Return (min_x, max_x, min_y, max_y) across all coordinates."""

    x_coordinates = [x for x, _ in coords]
    y_coordinates = [y for _, y in coords]
    return (
        min(x_coordinates),
        max(x_coordinates),
        min(y_coordinates),
        max(y_coordinates),
    )


def build_edge_interval_maps(
    vertical_edges: list[tuple[int, int, int]],
    horizontal_edges: list[tuple[int, int, int]],
) -> tuple[dict[int, list[tuple[int, int]]], dict[int, list[tuple[int, int]]]]:
    """Build merged inclusive intervals for fast "on boundary" checks.

    Args:
        vertical_edges: list of (x, y_min, y_max)
        horizontal_edges: list of (y, x_min, x_max)

    Returns:
        (vertical_intervals_by_x, horizontal_intervals_by_y)
    """

    vertical_intervals_by_x: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for x, y0, y1 in vertical_edges:
        vertical_intervals_by_x[x].append((y0, y1))
    vertical_intervals_by_x = {
        x: merge_intervals(intervals)
        for x, intervals in vertical_intervals_by_x.items()
    }

    horizontal_intervals_by_y: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for y, x0, x1 in horizontal_edges:
        horizontal_intervals_by_y[y].append((x0, x1))
    horizontal_intervals_by_y = {
        y: merge_intervals(intervals)
        for y, intervals in horizontal_intervals_by_y.items()
    }

    return vertical_intervals_by_x, horizontal_intervals_by_y


def build_compressed_edges(
    coords: list[tuple[int, int]],
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
) -> tuple[list[int], list[int], dict[int, int], dict[int, int]]:
    """Build coordinate-compressed x/y edge arrays and lookup maps.

    We include each coordinate and its neighbors (+/-1) so that polygon boundaries
    and interior/exterior changes occur only on these edges.
    """

    x_coordinates = [x for x, _ in coords]
    y_coordinates = [y for _, y in coords]

    x_edges_set: set[int] = {min_x, max_x + 1}
    y_edges_set: set[int] = {min_y, max_y + 1}

    for x in set(x_coordinates):
        for delta_x in (-1, 0, 1):
            candidate_x = x + delta_x
            if min_x <= candidate_x <= max_x + 1:
                x_edges_set.add(candidate_x)
    for y in set(y_coordinates):
        for delta_y in (-1, 0, 1):
            candidate_y = y + delta_y
            if min_y <= candidate_y <= max_y + 1:
                y_edges_set.add(candidate_y)

    x_edges = sorted(x_edges_set)
    y_edges = sorted(y_edges_set)
    x_edge_to_index = {x: i for i, x in enumerate(x_edges)}
    y_edge_to_index = {y: i for i, y in enumerate(y_edges)}
    return x_edges, y_edges, x_edge_to_index, y_edge_to_index


def build_crossing_x_values_for_row(
    y: int, vertical_edges: list[tuple[int, int, int]]
) -> list[int]:
    """Return sorted x values where a horizontal ray at this y crosses vertical edges.

    Uses a half-open y-range [y_min, y_max) to avoid counting polygon vertices twice.
    """

    crossing_x_values: list[int] = []
    for x, y0, y1 in vertical_edges:
        if y0 == y1:
            continue
        if y0 <= y < y1:
            crossing_x_values.append(x)
    crossing_x_values.sort()
    return crossing_x_values


def tile_is_on_boundary(
    x: int,
    y: int,
    vertical_intervals_by_x: dict[int, list[tuple[int, int]]],
    horizontal_intervals_by_y: dict[int, list[tuple[int, int]]],
) -> bool:
    """Return True if the tile (x, y) lies on the polygon boundary."""

    horizontal_intervals = horizontal_intervals_by_y.get(y)
    if horizontal_intervals is not None and interval_contains(horizontal_intervals, x):
        return True

    vertical_intervals = vertical_intervals_by_x.get(x)
    if vertical_intervals is not None and interval_contains(vertical_intervals, y):
        return True

    return False


def build_prefix_sum_from_scanlines(
    x_edges: list[int],
    y_edges: list[int],
    vertical_edges: list[tuple[int, int, int]],
    vertical_intervals_by_x: dict[int, list[tuple[int, int]]],
    horizontal_intervals_by_y: dict[int, list[tuple[int, int]]],
) -> list[list[int]]:
    """Build 2D prefix sum of allowed tiles using scanline parity and boundary checks."""

    x_cell_widths = [x_edges[i + 1] - x_edges[i] for i in range(len(x_edges) - 1)]
    y_cell_heights = [y_edges[j + 1] - y_edges[j] for j in range(len(y_edges) - 1)]

    column_count = len(x_cell_widths)
    row_count = len(y_cell_heights)
    prefix_sum = [[0] * (column_count + 1) for _ in range(row_count + 1)]

    for row_index in range(row_count):
        y = y_edges[row_index]
        crossing_x_values = build_crossing_x_values_for_row(y, vertical_edges)

        running_row_sum = 0
        for column_index in range(column_count):
            x = x_edges[column_index]

            on_boundary = tile_is_on_boundary(
                x, y, vertical_intervals_by_x, horizontal_intervals_by_y
            )

            if on_boundary:
                inside_or_boundary = True
            else:
                # even/odd rule: crossings strictly to the left of this tile
                inside_or_boundary = (bisect_left(crossing_x_values, x) % 2) == 1

            allowed_tiles = (
                x_cell_widths[column_index] * y_cell_heights[row_index]
                if inside_or_boundary
                else 0
            )

            running_row_sum += allowed_tiles
            prefix_sum[row_index + 1][column_index + 1] = (
                prefix_sum[row_index][column_index + 1] + running_row_sum
            )

    return prefix_sum


def build_allowed_tiles_prefix_sum(coords: list[tuple[int, int]]):
    """Build a fast lookup structure for "allowed" (red/green) tiles.

    The loop described by the red tiles is an orthogonal polygon on integer tile
    coordinates. All tiles on its boundary and strictly inside it are "allowed"
    (red or green).

    This function creates a 2D prefix sum over a *coordinate-compressed* grid of
    tile blocks. Querying a rectangle then becomes O(1): if the number of allowed
    tiles equals the rectangle area, the rectangle is fully allowed.

    Returns:
        (prefix_sum, x_edge_to_index, y_edge_to_index)

        prefix_sum: 2D array where prefix_sum[r][c] is the sum of allowed tiles in
            the region spanning compressed rows < r and columns < c.
        x_edge_to_index: map from x boundary coordinate to compressed index.
        y_edge_to_index: map from y boundary coordinate to compressed index.
    """

    min_x, max_x, min_y, max_y = get_bounding_box(coords)
    vertical_edges, horizontal_edges = build_edges(coords)

    vertical_intervals_by_x, horizontal_intervals_by_y = build_edge_interval_maps(
        vertical_edges, horizontal_edges
    )

    x_edges, y_edges, x_edge_to_index, y_edge_to_index = build_compressed_edges(
        coords, min_x, max_x, min_y, max_y
    )

    prefix_sum = build_prefix_sum_from_scanlines(
        x_edges,
        y_edges,
        vertical_edges,
        vertical_intervals_by_x,
        horizontal_intervals_by_y,
    )

    return prefix_sum, x_edge_to_index, y_edge_to_index


def solve_part2(coords: list[tuple[int, int]]) -> int:
    """
    Solves Part 2.

    Args:
        data: The structured input data.

    Returns:
        The maximum rectangle area with red opposite corners where every tile in
        the rectangle is red or green.
    """
    prefix_sum, x_edge_to_index, y_edge_to_index = build_allowed_tiles_prefix_sum(
        coords
    )

    def count_allowed_tiles_in_rectangle(
        min_x: int, min_y: int, max_x: int, max_y: int
    ) -> int:
        """Count allowed tiles in an inclusive rectangle."""

        left = x_edge_to_index[min_x]
        right = x_edge_to_index[max_x + 1]
        bottom = y_edge_to_index[min_y]
        top = y_edge_to_index[max_y + 1]
        return (
            prefix_sum[top][right]
            - prefix_sum[bottom][right]
            - prefix_sum[top][left]
            + prefix_sum[bottom][left]
        )

    max_rect_area = 0
    n = len(coords)
    for i in range(n):
        x1, y1 = coords[i]
        for j in range(i + 1, n):
            x2, y2 = coords[j]
            min_x = x1 if x1 <= x2 else x2
            max_x = x2 if x1 <= x2 else x1
            min_y = y1 if y1 <= y2 else y2
            max_y = y2 if y1 <= y2 else y1

            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            if area <= max_rect_area:
                continue
            if count_allowed_tiles_in_rectangle(min_x, min_y, max_x, max_y) == area:
                max_rect_area = area

    return max_rect_area


def main():
    with open("day-9.input.txt", "r") as f:
        data = f.read()

    coords = parse_input(data)

    part1_result = solve_part1(coords)
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(coords)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
