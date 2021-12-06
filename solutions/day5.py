from typing import NamedTuple, List

import numpy as np
import matplotlib.pyplot as plt


class Point(NamedTuple):
    x: int
    y: int


class Line(NamedTuple):
    start: Point
    end: Point

    def is_vertical(self):
        return self.start.x == self.end.x

    def is_horizontal(self):
        return self.start.y == self.end.y


def count_intersections(lines: List[Line], count_diagonal: bool= False) -> int:
    board = np.zeros((1000, 1000))
    for line in lines:
        if line.is_horizontal():
            startx, endx = min(line.start.x, line.end.x), max(line.start.x, line.end.x)
            board[line.start.y, startx:endx+1] += 1
        elif line.is_vertical():
            starty, endy = min(line.start.y, line.end.y), max(line.start.y, line.end.y)
            board[starty:endy+1, line.start.x] += 1
        else:
            if count_diagonal:
                x_sign = 1 if line.start.x < line.end.x else -1
                y_sign = 1 if line.start.y < line.end.y else -1
                n_steps = np.abs(line.start.x - line.end.x) + 1
                for delta in range(n_steps):
                    board[line.start.y + y_sign * delta, line.start.x + x_sign * delta] += 1

    #plt.imshow(board)
    #plt.show()
    return np.sum(board > 1)


def parse_line(line_str: str) -> Line:
    start = line_str.strip().split()[0].split(',')
    end = line_str.strip().split()[-1].split(',')
    p1 = Point(x=int(start[0]), y=int(start[1]))
    p2 = Point(x=int(end[0]), y=int(end[1]))

    return Line(start=p1, end=p2)


if __name__ == '__main__':
    def _main():
        lines = []
        with open('../inputs/day5.txt', 'r') as f:
            for line in f:
                lines.append(parse_line(line))

        print(f"Star 1: {count_intersections(lines, False)}")
        print(f"Star 2: {count_intersections(lines, True)}")


    _main()
