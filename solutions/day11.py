from collections import deque
from typing import Set, Tuple, List

import numpy as np


def get_neighbours(point: Tuple[int, int], grid: np.ndarray) -> List[Tuple[int, int]]:
    r, c = grid.shape
    rs = [point[0] - 1, point[0], point[0] + 1]
    cs = [point[1] - 1, point[1], point[1] + 1]
    neighbr, neighbc = np.meshgrid(rs, cs)
    # filter points outside of grid and original point
    valid = ((neighbr >= 0) & (neighbr < r) & (neighbc >= 0) &
             (neighbc < c) & ((neighbr != point[0]) | (neighbc != point[1])))
    return list(zip(neighbr[valid], neighbc[valid]))


def step(grid: np.ndarray) -> Tuple[np.ndarray, int]:
    grid += 1
    flash = grid > 9
    agenda = deque()
    flashed = set()
    for point in zip(*flash.nonzero()):
        flashed.add(point)
        grid[point[0], point[1]] = 0
        agenda.extend(get_neighbours(point, grid))

    while len(agenda) > 0:
        point = agenda.pop()
        if point in flashed:
            continue
        grid[point[0], point[1]] += 1
        if grid[point[0], point[1]] > 9:
            grid[point[0], point[1]] = 0
            flashed.add(point)
            agenda.extend(get_neighbours(point, grid))
    return grid, len(flashed)


def star1(grid: np.array) -> int:
    total = 0
    for _ in range(100):
        grid, steps = step(grid)
        total += steps
    return total


def star2(grid):
    n_steps = 0
    while not np.all(grid == 0):
        grid, _ = step(grid)
        n_steps += 1
    return n_steps


if __name__ == '__main__':
    def _main():
        with open('../inputs/day11.txt', 'r') as f:
            inp = f.readlines()
        inp = np.array([list(s.strip()) for s in inp], dtype=int)

        print(star1(inp.copy()))  # don't change input for star 2
        print(star2(inp))

    _main()
