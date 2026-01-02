"""
Advent of Code 2025 - Day 11: Reactor
Count paths through a directed graph with optional required waypoints.
"""


class Graph:
    """Represents a directed graph using an adjacency list."""

    def __init__(self):
        self.adjacency_list = {}

    def add_edges(self, from_node: str, to_nodes: list[str]) -> None:
        """
        Adds directed edges from one node to multiple destination nodes.

        Args:
            from_node: The source node.
            to_nodes: List of destination nodes.
        """
        if from_node not in self.adjacency_list:
            self.adjacency_list[from_node] = []
        self.adjacency_list[from_node].extend(to_nodes)

    def dfs(
        self, start_node: str, target_node: str, cache: dict[str, int], seen: set[str]
    ) -> int:
        """
        Counts all simple paths from start_node to target_node using DFS with memoization.

        A simple path is one that doesn't visit any node more than once.
        Uses backtracking DFS with a cache to avoid recomputing paths from the same node.

        Args:
            start_node: Starting node for the path search.
            target_node: Destination node.
            cache: Memoization cache mapping nodes to path counts.
            seen: Set of nodes already visited in the current path.

        Returns:
            Number of distinct simple paths from start_node to target_node.
        """
        if start_node == target_node:
            return 1

        if start_node in cache:
            return cache[start_node]

        seen.add(start_node)
        total_paths = 0

        for neighbor in self.adjacency_list.get(start_node, []):
            if neighbor not in seen:
                total_paths += self.dfs(neighbor, target_node, cache, seen)

        seen.remove(start_node)
        cache[start_node] = total_paths
        return total_paths

    def dfs_with_must_visit(
        self,
        start_node: str,
        target_node: str,
        cache: dict[tuple[str, bool, bool], int],
        seen: set[str],
        must_visit1: str,
        must_visit2: str,
    ) -> int:
        """
        Counts simple paths from start_node to target_node that pass through two required nodes.

        This variant of DFS requires that both must_visit1 and must_visit2 are visited
        somewhere along the path (in any order). The cache key includes the current node
        and the state of which required nodes have been visited to correctly memoize
        partial paths.

        Args:
            start_node: Starting node for the path search.
            target_node: Destination node.
            cache: Memoization cache with keys of (node, visited_must1, visited_must2).
            seen: Set of nodes already visited in the current path.
            must_visit1: First required waypoint node.
            must_visit2: Second required waypoint node.

        Returns:
            Number of distinct simple paths from start_node to target_node
            that pass through both must_visit1 and must_visit2.
        """
        if start_node == target_node:
            return 1 if must_visit1 in seen and must_visit2 in seen else 0

        cache_key = (start_node, must_visit1 in seen, must_visit2 in seen)
        if cache_key in cache:
            return cache[cache_key]

        seen.add(start_node)
        total_paths = 0

        for neighbor in self.adjacency_list.get(start_node, []):
            if neighbor not in seen:
                total_paths += self.dfs_with_must_visit(
                    neighbor,
                    target_node,
                    cache,
                    seen,
                    must_visit1,
                    must_visit2,
                )

        cache[cache_key] = total_paths
        seen.remove(start_node)
        return total_paths


def setup(data: str) -> Graph:
    """
    Parses the reactor device connection map into a directed graph.

    Each line in the input has the format "device: output1 output2 ..."
    representing directed edges from a device to its output connections.

    Args:
        data: Raw puzzle input containing device connections.

    Returns:
        Graph representing the reactor's device network.
    """
    lines = data.strip().splitlines()
    graph = Graph()

    for line in lines:
        parts = line.split(":")
        from_node = parts[0]
        to_nodes = parts[1].split() if len(parts) > 1 else []
        graph.add_edges(from_node, to_nodes)

    return graph


def solve_part1(graph: Graph) -> int:
    """
    Counts all possible paths from 'you' to 'out' in the reactor network.

    Args:
        graph: The reactor device connection graph.

    Returns:
        Total number of distinct paths from 'you' to 'out'.
    """
    return graph.dfs("you", "out", {}, set())


def solve_part2(graph: Graph) -> int:
    """
    Counts paths from 'svr' to 'out' that pass through both 'dac' and 'fft'.

    This solves the problem of finding paths that visit specific devices
    (a digital-to-analog converter and fast Fourier transform device)
    to identify the problematic data path.

    Args:
        graph: The reactor device connection graph.

    Returns:
        Number of paths from 'svr' to 'out' that visit both 'dac' and 'fft'.
    """
    return graph.dfs_with_must_visit("svr", "out", {}, set(), "dac", "fft")


def main():
    """Main entry point."""
    with open("day-11.input.txt", "r") as f:
        data = f.read()

    graph = setup(data)

    part1_result = solve_part1(graph)
    print(f"Part 1: {part1_result}")

    part2_result = solve_part2(graph)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
