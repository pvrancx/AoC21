from collections import deque

import numpy as np
import matplotlib.pyplot as plt


def get_lowest(heightmap):
    r, c = heightmap.shape
    padded = np.ones((r+2, c+2)) * np.inf
    padded[1:r+1, 1:c+1] = heightmap[:, ]
    lowest = padded[1:r+1, 1:c+1] < padded[0:r, 1:c+1]  # up
    lowest = np.logical_and(lowest, padded[1:r+1, 1:c+1] < padded[2:r+2, 1:c+1])
    lowest = np.logical_and(lowest, padded[1:r+1, 1:c+1] < padded[1:r+1, 2:c+2])
    lowest = np.logical_and(lowest, padded[1:r+1, 1:c+1] < padded[1:r+1, 0:c])
    return lowest


def star1(heightmap):
    return np.sum(heightmap[get_lowest(heightmap)]+1)


def expand(point, map):
    r, c = map.shape
    neighbs = []
    if point[0] > 0:
        neighbs.append((point[0]-1, point[1]))
    if point[0] < r - 1:
        neighbs.append((point[0] + 1, point[1]))
    if point[1] > 0:
        neighbs.append((point[0], point[1] - 1))
    if point[1] < c - 1:
        neighbs.append((point[0], point[1] + 1))
    return neighbs


def get_basin(map, point):
    agenda = deque()
    agenda.append(point)
    visited = set()
    basin_size = 0
    basin = np.zeros_like(map)
    while len(agenda) > 0:
        current_point = agenda.popleft()
        if current_point in visited:
            continue
        visited.add(current_point)
        if map[current_point[0], current_point[1]] != 9:
            basin_size += 1
            basin[current_point[0], current_point[1]] = 1
            neighbs = expand(current_point, map)
            for neighb in neighbs:
                agenda.append(neighb)

    return basin_size


def star2(heightmap):
    lowest = np.logical_and(get_lowest(heightmap), heightmap != 9)
    rows, cols = lowest.nonzero()
    result = {}
    for point in zip(rows, cols):
        result[point] = get_basin(heightmap, point)

    return np.prod(sorted(list(result.values()), reverse=True)[:3])


if __name__ == '__main__':
    def _main():
        with open('../inputs/day9.txt', 'r') as f:
            inp = f.readlines()
        inp = np.array([list(s.strip()) for s in inp], dtype=int)
        print(inp)
        print(star1(inp))
        print(star2(inp))

    _main()
