from typing import List

import numpy as np


def init_state(list_of_fish: List[int]) -> np.ndarray:
    # only store number of each counter value
    state = np.zeros(9, dtype=np.int64)  # int64 to avoid overflow star 2
    for fish in list_of_fish:
        state[fish] += 1
    return state


def simulate(state: np.ndarray, n_days: int)-> int:
    for _ in range(n_days):
        # spawning fish
        n_zeros = state[0]
        # decrement all counters
        state[0:8] = state[1:9]
        # spawn new fish
        state[8] = n_zeros
        # reset spawning fish
        state[6] += n_zeros
    return np.sum(state)


if __name__ == '__main__':
    def _main():
        with open('../inputs/day6.txt', 'r') as f:
            inp = f.readline().strip().split(',')
        inp = [int(s) for s in inp]

        print(f"Star 1: {simulate(init_state(inp), 80)}")
        print(f"Star 2: {simulate(init_state(inp), 256)}")

    _main()

