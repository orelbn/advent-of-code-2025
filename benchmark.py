"""
Benchmark utilities for Advent of Code solutions.
"""

import time
from collections.abc import Callable
from typing import Any


def benchmark(
    name: str,
    func: Callable[..., Any],
    *args,
    runs: int = 100,
    setup: Callable[[], tuple] | None = None,
) -> Any:
    """
    Benchmarks a function and prints the results.

    Args:
        name: Label for the benchmark (e.g., "Part 1").
        func: The function to benchmark.
        *args: Positional arguments to pass to the function.
        runs: Number of times to run the function.
        setup: Optional function that returns args for func. Called each run.

    Returns:
        The result of the function.
    """
    times = []
    result = None

    for _ in range(runs):
        start = time.perf_counter()
        if setup:
            run_args = setup()
            result = func(*run_args)
        else:
            result = func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)

    avg_ms = sum(times) / len(times)

    print(f"{name}: {result} (Average: {avg_ms:.3f} ms, {runs} runs)")

    return result
