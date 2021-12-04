from typing import List

import numpy as np


class Board:
    def __init__(self, numbers: np.ndarray):
        self.numbers = numbers
        self.marked = np.zeros_like(numbers, dtype=bool)

    def get_score(self, number: int) -> int:
        return np.sum(self.numbers[np.logical_not(self.marked)]) * number

    def play(self, number: int) -> bool:
        in_board = self.numbers == number
        self.marked[in_board] = True
        bingo = np.any(np.all(self.marked, axis=0)) or np.any(np.all(self.marked, axis=1))
        return bingo


def win_bingo(draws: List[int], boards: List[Board]) -> int:
    for number in draws:
        for board in boards:
            bingo = board.play(number)
            if bingo:
                return board.get_score(number)
    return -1


def lose_bingo(draws: List[int], boards: List[Board]) -> int:
    bingos = np.zeros(len(boards), dtype=bool)
    for number in draws:
        for idx, board in enumerate(boards):
            bingo = board.play(number)
            if bingo:
                bingos[idx] = True
                if np.all(bingos):
                    return board.get_score(number)
    return -1


def read_file(f):
    draws = [int(s) for s in f.readline().strip().split(',')]
    boards = []

    board = []
    f.readline()
    for idx, line in enumerate(f):
        if line == '\n':
            boards.append(np.array(board, dtype=int))
            board = []
        else:
            board.append([int(s) for s in line.strip().split()])

    return draws, boards


if __name__ == '__main__':
    def _main():
        with open('../inputs/day4.txt', 'r') as f:
            draws, boards = read_file(f)

        boards = [Board(b) for b in boards]
        print(f"Star 1: {win_bingo(draws, boards)}")
        print(f"Star 2: {lose_bingo(draws, boards)}")

    _main()

