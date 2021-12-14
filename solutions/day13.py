import numpy as np
import matplotlib.pyplot as plt


def fold_grid(grid, fold):
    direction, line_nr = fold
    r, c = grid.shape

    new_grid = None
    if direction == 'x':
        new_grid = grid[:, 0:line_nr]
        new_grid[np.flip(grid[:, line_nr+1:c+1], 1)] = 1
    elif direction == 'y':
        new_grid = grid[0:line_nr, :]
        new_grid[np.flip(grid[line_nr+1:r+1, :], 0)] = 1
    else:
        RuntimeError('unknown direction')
    return new_grid


if __name__ == '__main__':
    def _main():
        with open('../inputs/day13.txt', 'r') as f:
            line = f.readline()
            coords = []
            while line != "\n":
                x, y = line.strip().split(',')
                coords.append((int(y), int(x)))
                line = f.readline()

            line = f.readline()
            folds = []
            while line != "":
                direction, nr = line.strip().split()[-1].split('=')
                folds.append((direction, int(nr)))
                line = f.readline()

            rs, cs = zip(*coords)

            grid = np.zeros((895, 1311), dtype=bool)
            np.put(grid, np.ravel_multi_index((rs, cs), grid.shape), 1)

            for idx, fold in enumerate(folds):
                grid = fold_grid(grid, fold)
                if idx == 0:
                    print(f"Star 1: {np.sum(grid)}")

            plt.matshow(grid)
            plt.show()


    _main()

