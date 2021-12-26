import numpy as np


def step_herd(grid: np.ndarray, herd_type: int):
    herd = (grid == herd_type)
    r, c = herd.nonzero()
    idx = np.ravel_multi_index((r, c), grid.shape, mode='wrap')
    next_idx = np.ravel_multi_index((r + 1, c), grid.shape, mode='wrap') if herd_type == 2 \
        else np.ravel_multi_index((r, c + 1), grid.shape, mode='wrap')
    can_move = grid.flat[next_idx] == 0
    grid.flat[idx[can_move]] = 0
    grid.flat[next_idx[can_move]] = herd_type
    return grid


def step(grid):
    for herd_type in [1, 2]:
        grid = step_herd(grid, herd_type)
    return grid


def multi_step(grid):
    nsteps = 0
    done = False
    while not done:
        nsteps += 1
        next_grid = step(grid.copy())
        done = np.all(next_grid == grid)
        grid = next_grid
    return nsteps


if __name__ == '__main__':
    def _main():
        with open('../inputs/day25.txt', 'r') as f:
            decode = {'.': 0, '>': 1, 'v': 2}
            inp = np.array([[decode[s] for s in line.strip()] for line in f])

        print(multi_step(inp))


    _main()
