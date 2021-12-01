import numpy as np


def count_increases(list_of_numbers):
    return np.sum(list_of_numbers[1:] - list_of_numbers[:-1] > 0)


def sliding_window_increases(list_of_numbers):
    return count_increases(np.convolve(list_of_numbers, [1, 1, 1], mode='valid'))


if __name__ == '__main__':
    def _main():
        with open('../inputs/day1.txt', 'r') as f:
            inp = np.array(f.readlines(), dtype=int)
        print(inp)

        print(f"Star 1: {count_increases(inp)}")
        print(f"Star 2: {sliding_window_increases(inp)}")

    _main()
