import sys
import time
from dataclasses import dataclass
from heapq import heapify, heappop, heappush

import numpy as np


@dataclass
class Node:
    dist: np.float
    idx: int


def print_grid(grid, prev):
    sol = np.zeros_like(grid)
    idx = grid.size - 1
    while not idx == 0:
        print(idx)
        sol.flat[idx] = 1
        idx = prev[idx]
    return sol


def get_large_grid(grid):
    result= []
    for c in range(5):
        row = []
        for r in range(5):
            offset = manhattan((r, c), (0, 0))
            g = grid + offset
            g = (g <= 9) * g + (g > 9) * ((g % 10) + 1)
            row.append(g)
        result.append(np.concatenate(row, axis =-1))
    return np.concatenate(result, axis=0)


def get_neighbours(idx, grid):
    neighb = []
    r,c = np.unravel_index(idx, grid.shape)
    if r > 0:
        neighb.append(np.ravel_multi_index((r-1,c), grid.shape))
    if r < grid.shape[0] -1:
        neighb.append(np.ravel_multi_index((r+1,c), grid.shape))
    if c > 0:
        neighb.append(np.ravel_multi_index((r,c-1), grid.shape))
    if c < grid.shape[1] -1:
        neighb.append(np.ravel_multi_index((r,c +1), grid.shape))
    return neighb


def manhattan(point1, point2) -> int:
    return np.abs(point2[1] - point1[1]) + np.abs(point2[0] - point1[0])


def astar(grid, start, end, heuristic=lambda x,y: 0):
    agenda = [(0,  start)]
    costs = np.ones(grid.size, dtype=int) * sys.maxsize
    costs[start] = 0
    visited = set()
    while len(agenda) > 0:
        node = heappop(agenda)
        if node[1] == end:
            return costs[node[1]]
        if node[1] in visited:
            continue

        visited.add(node[1])
        for neighb in get_neighbours(node[1], grid):
            cost = costs[node[1]] + grid.flat[neighb]
            if cost < costs[neighb]:
                costs[neighb] = cost
            heappush(agenda,
                     (costs[neighb] + heuristic(
                         np.unravel_index(node[1], grid.shape),
                         np.unravel_index(end, grid.shape)),
                      neighb))
    return -1


def dijkstra(grid, start, end):

    nodes = []
    prev = np.zeros(grid.size, dtype=int)
    for i in range(grid.size):
        if i == start:
            nodes.append((0, i))
        else:
            nodes.append((np.inf, i))
    heapify(nodes)

    while not len(nodes) == 0:
        node = heappop(nodes)

        if node[1] == end:
            return node[0], prev

        neighb = get_neighbours(node[1], grid)
        changed = False
        for idx, node2 in enumerate(nodes):
            if node2[1] in neighb:
                dist = node[0] + grid.flat[node2[1]]
                if dist < node2[0]:
                    new_node = (dist, node2[1])
                    nodes[idx] = new_node
                    prev[node2[1]] = node[1]
                    changed = True
        if changed:
            heapify(nodes)

    return -1, prev


if __name__ == '__main__':
    def _main():
        with open('../inputs/day15.txt', 'r') as f:
            inp = np.array([[int(x) for x in line.strip()] for line in f], dtype=int)

        start = time.time()

        print(f"Starting...")
        large_inp = get_large_grid(inp)

        print(f"Star 1: {dijkstra(inp, 0, inp.size-1)}")
        print(f"Star 2: {dijkstra(large_inp, 0, large_inp.size-1)}")

        print(f"Finished in: {time.time() - start}s")


    _main()
