# Advent of Code 2025

My solutions for [Advent of Code 2025](https://adventofcode.com/2025) in Python.

## Progress

| Day | Part 1       | Part 2       |
|-----|--------------|--------------|
| 1   | ⭐ 0.77 ms   | ⭐ 1.03 ms   |
| 2   | ⭐ 17.7 ms   | ⭐ 39.2 ms   |
| 3   | ⭐ 1.33 ms   | ⭐ 2.63 ms   |
| 4   | ⭐ 12.2 ms   | ⭐ 24.7 ms   |
| 5   | ⭐ 0.41 ms   | ⭐ 0.11 ms   |
| 6   | ⭐ 2.64 ms   | ⭐ 2.41 ms   |
| 7   | ⭐ 0.38 ms   | ⭐ 0.63 ms   |
| 8   | ⭐ 50.4 ms   | ⭐ 63.4 ms   |
| 9   | ⭐ 18.8 ms   | ⭐ 165.85 ms |
| 10  | ⭐ 16.9 ms   |              |

## Running

I recommend using [uv](https://docs.astral.sh/uv/) to run:

```bash
uv run day-1.py
```

## Notes

- Input files are not included per [Advent of Code guidelines](https://adventofcode.com/2025/about)
- Each solution expects an input file named `day-N.input.txt` in the same directory
- I complete the problems myself, but use AI to optimize documentation and explore possible improvements in code structure and efficiency. 
- I DO NOT recommend copying this code for your own use in Advent of Code, but instead, this can be used as a reference after you have completed the problems yourself.
- If you have any recommendations, feel free to reach me on [LinkedIn](https://www.linkedin.com/in/orelbn/).

## Benchmarking

A simple benchmark utility is included to measure solution performance:

```python
from benchmark import benchmark

benchmark("Part 1", solve_part1, arg1, arg2)
benchmark("Part 1", solve_part1, setup=setup_func, runs=50)
```

The `setup` parameter accepts a function that returns args for the solve function, useful for including preprocessing in the timing.
