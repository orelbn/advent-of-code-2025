# Advent of Code 2025

My solutions for [Advent of Code 2025](https://adventofcode.com/2025) in Python.

## Progress

| Day | Part 1 | Part 2 |
|-----|--------|--------|
| 1   | ⭐     | ⭐     |
| 2   | ⭐     | ⭐     |
| 3   | ⭐     | ⭐     |
| 4   | ⭐     | ⭐     |
| 5   | ⭐     | ⭐     |

## Running

I recommend using [uv](https://docs.astral.sh/uv/) to run:

```bash
uv run day-1.py
```

## Notes

- Input files are not included per [Advent of Code guidelines](https://adventofcode.com/2025/about)
- Each solution expects an input file named `day-N.input.txt` in the same directory
- I complete the problems myself, but use AI to optimize documentation, and explore possible improvements in code structure and efficiency. 
- I DO NOT recommend copying this code for your own use in Advent of Code, but instead this can be used as a reference after you have completed the problems yourself, to explore alternative solutions.
- If you have any recommendations, feel free to reach me on [LinkedIn](https://www.linkedin.com/in/orelbn/).

## Benchmarking

A simple benchmark utility is included to measure solution performance:

```python
from benchmark import benchmark

benchmark("Part 1", solve_part1, arg1, arg2)
benchmark("Part 1", solve_part1, setup=setup_func, runs=50)
```

The `setup` parameter accepts a function that returns args for the solve function, useful for including preprocessing in the timing.
