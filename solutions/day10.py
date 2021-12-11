
def parse_line(line):
    stack = []
    close_map = {'{':'}', '(':')', '[': ']','<':'>'}
    points_map = {'}':1197, ')': 3, ']': 57, '>': 25137}
    for ch in list(line):
        if ch in '[{(<':
            stack.append(ch)
        elif ch in ']}>)':
            open_ch = stack.pop()
            if close_map[open_ch] != ch:  # corrupt line
                return points_map[ch]
        else:
            raise RuntimeError('unknown char')
    return 0  # valid or incomplete line


def complete_line(line):
    stack = []
    close_map = {'{':'}', '(':')', '[': ']','<':'>'}
    points_map = {'}':3, ')': 1, ']': 2, '>': 4}
    for ch in list(line):
        if ch in '[{(<':
            stack.append(ch)
        elif ch in ']}>)':
            open_ch = stack.pop()
            if close_map[open_ch] != ch:
                return 0  # discard line
        else:
            raise RuntimeError('unknown char')
    score = 0
    while len(stack) != 0:  # incomplete line
        score *= 5
        next_ch = close_map[stack.pop()]
        score += points_map[next_ch]
    return score


def star2(inp):
    points = list(sorted(filter(lambda x: x != 0, [complete_line(line) for line in inp])))
    return points[len(points) // 2]


def star1(inp):
    points = [parse_line(line) for line in inp]
    return sum(points)


if __name__ == '__main__':
    def _main():
        with open('../inputs/day10.txt', 'r') as f:
            inp = f.readlines()
        inp = [s.strip() for s in inp]

        print(star1(inp))
        print(star2(inp))


    _main()

