import numpy as np


def cost1(pos, h):
    return np.abs(pos - h)


def cost2(pos, h):
    cost = cost1(pos, h)
    return cost * (cost + 1) / 2


def get_cost(list_of_ints, cost_fn):
    pos = np.array(list_of_ints)
    best_cost = np.inf
    best = -1
    for h in range(np.min(pos), np.max(pos)):
        cost = int(np.sum(cost_fn(pos, h)))
        if cost < best_cost:
            best_cost = cost
            best = h
    return best, best_cost


if __name__ == '__main__':
    def _main():
        with open('../inputs/day7.txt', 'r') as f:
            inp = f.readline().strip().split(',')
        inp = [int(s) for s in inp]
        print(f" Star 1: {get_cost(inp, cost1)}")
        print(f" Star 2: {get_cost(inp, cost2)}")

    _main()

