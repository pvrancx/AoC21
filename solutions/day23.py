from heapq import heappop, heappush

import numpy as np
import matplotlib.pyplot as plt

target_rooms = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
step_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def value(world, x, y):
    return world[y][x]


def room_size(world):
    return len(world) - 3


def in_hallway(_, y):
    return y == 1


def in_room(_, y):
    return y > 1


def is_amp(world, x, y):
    return value(world, x, y) in target_rooms.keys()


def room_id(x, y):
    if in_room(x, y):
        return [3, 5, 7, 9].index(x)
    else:
        return -1


def room_x_coord(idx):
    return [3, 5, 7, 9][idx]


def in_target_room(world, x, y):
    return is_amp(world, x, y) \
           and in_room(x, y) \
           and room_id(x, y) == target_rooms[value(world, x, y)]


def in_front_room(x, y):
    return (y == 1) and x in [3, 5, 7, 9]


def is_blocked_in_room(world, x, y):
    return (in_room(x, y) and
            any([is_amp(world, x, yi) for yi in range(y-1, 1, -1)]) or  # amp in room above
            all([is_amp(world, xi, 1) for xi in [x-1, x+1]]))        # amp on both sides of exit


def path_free(world, x1, x2):
    if x1 < x2:
        return all([is_empty(world, x, 1) for x in range(x1, x2+1)])
    else:
        return all([is_empty(world, x, 1) for x in range(x2, x1+1)])


def blocks_other(world,x, y):
    if not is_amp(world, x, y) or not in_room(x, y):
        return False
    for yi in range(y+1, 2+ room_size(world)):
        if is_amp(world, x, yi) and not in_target_room(world, x, yi):
            return True
    return False


def can_move(world, x, y):
    if not is_amp(world, x, y):
        return False
    if in_hallway(x, y):
        target = target_rooms[value(world, x, y)]
        room_x = room_x_coord(target)
        start_x = x + 1 if x < room_x else x -1
        return room_is_free(world, target) and path_free(world, start_x, room_x)
    elif in_room(x, y):
        return not is_blocked_in_room(world, x, y) and (not in_target_room(world, x, y)
                                                        or blocks_other(world, x, y))
    else:
        return False


def is_empty(world, x, y):
    return value(world, x, y) == '.'


def first_free(world, room_idx):
    x = [3, 5, 7, 9][room_idx]
    yi = 1
    while yi < 1 + room_size(world) and is_empty(world, x, yi + 1):
        yi += 1
    if yi == 1:
        return None
    else:
        return x, yi


def room_is_free(world, idx):
    x = room_x_coord(idx)
    room_coords = [(x, y) for y in range(2, 2 + room_size(world))]
    return (any([is_empty(world, *p) for p in room_coords]) and
            not any([is_amp(world, *p) and not in_target_room(world, *p) for p in room_coords]))


def get_amps(world):
    result = []
    for y in range(len(world)):
        for x in range(len(world[y])):
            if is_amp(world, x, y):
                result.append((x, y))
    return result


def move(world, from_x, from_y, to_x, to_y):
    world = [list(line) for line in world]
    world[to_y][to_x] = value(world, from_x, from_y)
    world[from_y][from_x] = '.'
    return (*((*line,) for line in world),)


def path_cost(world, from_x, from_y, to_x, to_y):
    cost = step_cost[value(world, from_x, from_y)]
    if in_room(from_x, from_y) and in_room(to_x, to_y) and from_x != to_x:
        # room to room move
        return (abs(to_x - from_x) + abs(to_y - 1) + abs(from_y - 1)) * cost
    else:
        return (abs(to_x - from_x) + abs(to_y - from_y)) * cost


def is_goal(world):
    amps = get_amps(world)
    return all([in_target_room(world, *amp) for amp in amps])


def hall_coords():
    return [(x, 1) for x in range(1, 12)]


def generate_pos(world, x, y):
    assert can_move(world, x, y)
    target = target_rooms[value(world, x, y)]

    if in_room(x, y):
        pos = [p for p in hall_coords() if not in_front_room(*p) and path_free(world, x, p[0])]
        if room_is_free(world, target) and path_free(world, x, room_x_coord(target)):
            # can move directly into target room
            pos += [first_free(world, target)]
        return pos
    else:
        return [first_free(world, target)]


def expand(world):
    amps = get_amps(world)
    result = []
    for amp in amps:
        if can_move(world, *amp):
            pos = generate_pos(world, *amp)
            for p in pos:
                result.append((path_cost(world, *amp, *p), move(world, *amp, *p)))
    return result


def search(world):
    agenda = [(0, world)]
    visited = set()
    while len(agenda) > 0:
        cost, state = heappop(agenda)
        if is_goal(state):
            return cost
        if state in visited:
            continue
        for new_cost, new_state in expand(state):
            heappush(agenda, (cost + new_cost, new_state))
        visited.add(state)
    return -1


def print_state(world):
    for line in world:
        print(''.join(line[:-1]))


if __name__ == '__main__':
    def _main():
        with open('../inputs/day23.txt', 'r') as f:
            world = (*((*line,) for line in f),)
            #world = [list(line) for line in f]

        # print_state(world)
        #
        # nstates = expand(world)
        # nstate = nstates[16][-1]
        # print_state(nstate)
        # nnstates = expand(nstate)
        #
        #
        # for idx, state in enumerate(nnstates):
        #     print(f"--------------{idx}:{state[0]}--------------")
        #     print_state(state[-1])
        print(search(world))
        #
        # print(value(nstate, 3, 3))
        # print(in_room(3,3))
        # print(room_id(3,3))
        # print(target_rooms[value(world, 3, 3)])
        # print(in_target_room(nstate, 3, 3))



    _main()
