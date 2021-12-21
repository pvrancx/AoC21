from collections import defaultdict
from itertools import product

import numpy as np


def update_pos(start_pos, move):
    new_pos = (start_pos + move) % 10
    if new_pos == 0:
        return 10
    else:
        return new_pos


def play(start1, start2):
    scores = np.zeros(2)
    pos = np.array([start1, start2])
    die = (np.arange(999).reshape(-1, 3) % 100) + 1
    for turn in range(0, 998, 2):
        throws = np.sum(die[turn:turn+2, :], -1)
        print(throws)
        pos[0] = update_pos(pos[0], throws[0])
        scores[0] += pos[0]
        if np.any(scores >= 1000):
            return scores, (turn + 1) * 3
        pos[1] = update_pos(pos[1], throws[1])
        scores[1] += pos[1]

        if np.any(scores >= 1000):
            return scores, (turn + 2) * 3
    return scores


def get_all_rolls():
    return [sum(rolls) for rolls in product((1,2,3), repeat=3)]


def is_done(state):
    return state[2] >= 21 or state[3] >= 21


def play(state, player):
    pos = state[:2][player]
    score = state[2:][player]
    states = []

    for roll in get_all_rolls():
        new_pos = update_pos(pos, roll)
        new_score = score + new_pos
        if player == 0:
            states.append((new_pos, state[1], new_score, state[3]))
        else:
            states.append((state[0], new_pos, state[2], new_score))
    return states


def play_all_games(start1, start2):
    state_count = {(start1, start2, 0, 0): 1}
    player = 0
    done = False

    while not done:
        next_state_count = defaultdict(lambda: 0)
        for state, count in state_count.items():
            if is_done(state):
                next_state_count[state] += count
            else:
                next_states = play(state, player)
                for nstate in next_states:
                    next_state_count[nstate] += count
        state_count = next_state_count
        player = (player + 1) % 2
        done = True
        for state in state_count:
            if not is_done(state):
                done = False
                break

    wins = [0, 0]
    for state, val in state_count.items():
        assert is_done(state)
        if state[2] >= 21:
            wins[0] += val
        if state[3] >= 21:
            wins[1] += val
    return wins


if __name__ == '__main__':
    def _main():
        print(play_all_games(4,5))
    _main()
