import enum
from dataclasses import dataclass
from typing import Tuple, List


class Command(enum.Enum):
    FORWARD = 1
    UP = 2
    DOWN = 3


@dataclass
class Position:
    horizontal: int = 0
    depth: int = 0
    aim: int = 0

    def get_result(self) -> int:
        return self.horizontal * self.depth


def parse_cmd(cmd_str: str) -> Tuple[Command, int]:
    cmd, val = cmd_str.split()
    return Command[cmd.upper()], int(val)


def execute(list_of_commands: List[Tuple[Command, int]]) -> Position:
    pos = Position(0, 0, 0)
    for cmd, val in list_of_commands:
        if cmd is Command.FORWARD:
            pos.horizontal += val
        elif cmd is Command.UP:
            pos.depth -= val
        elif cmd is Command.DOWN:
            pos.depth += val
        else:
            raise RuntimeError('unknown command')
    return pos


def execute_aim(list_of_commands: List[Tuple[Command, int]]) -> Position:
    pos = Position(0, 0, 0)
    for cmd, val in list_of_commands:
        if cmd is Command.FORWARD:
            pos.horizontal += val
            pos.depth += val * pos.aim
        elif cmd is Command.UP:
            pos.aim -= val
        elif cmd is Command.DOWN:
            pos.aim += val
        else:
            raise RuntimeError('unknown command')
    return pos


if __name__ == '__main__':
    def _main():
        with open('../inputs/day2.txt', 'r') as f:
            inp = f.readlines()
        cmds = [parse_cmd(s) for s in inp]
        pos1 = execute(cmds)
        pos2 = execute_aim(cmds)
        print(f"Star 1: {pos1.get_result()}")
        print(f"Star 2: {pos2.get_result()}")

    _main()
