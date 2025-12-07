# Advent of Code 2025

My solutions for [Advent of Code 2025](https://adventofcode.com/2025) in Python.

## Progress

| Day | Part 1       | Part 2       |
|-----|--------------|--------------|
| 1   | ⭐ 0.70 ms   | ⭐ 0.95 ms   |
| 2   | ⭐ 17.6 ms   | ⭐ 38.3 ms   |
| 3   | ⭐ 1.39 ms   | ⭐ 2.84 ms   |
| 4   | ⭐ 13.1 ms   | ⭐ 24.8 ms   |
| 5   | ⭐ 0.25 ms   | ⭐ 0.01 ms   |
| 6   | ⭐ 1.58 ms   | ⭐ 1.30 ms   |
| 7   | ⭐ 0.37 ms   | ⭐ 0.62 ms   |

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
