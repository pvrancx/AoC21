from collections import deque, defaultdict
from math import floor


class Alu:
    def __init__(self, inputs):
        self._vars = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
        self._inps = deque([int(i) for i in inputs])

    def clear(self, inp):
        self._vars = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
        self._inps = deque([int(i) for i in inp])

    def inp(self, name):
        self._vars[name] = self._inps.popleft()

    def add(self, v1, v2):
        val = self._vars[v2] if v2 in self._vars else int(v2)
        self._vars[v1] += val

    def mul(self, v1, v2):
        val = self._vars[v2] if v2 in self._vars else int(v2)
        self._vars[v1] *= val

    def div(self, v1, v2):
        val = self._vars[v2] if v2 in self._vars else int(v2)
        self._vars[v1] = int(floor(self._vars[v1] / val))

    def mod(self, v1, v2):
        val = self._vars[v2] if v2 in self._vars else int(v2)
        self._vars[v1] = self._vars[v1] % val

    def eql(self, v1, v2):
        val = self._vars[v2] if v2 in self._vars else int(v2)
        self._vars[v1] = int(self._vars[v1] == val)

    def process(self, list_of_inst):
        for inst in list_of_inst:
            # print(f"{self._vars['w']}-{self._vars['x']}-{self._vars['y']}-{self._vars['z']}")
            # print(inst)
            getattr(self, inst[0])(*inst[1:])
        return self._vars['z']


def split_inputs(list_of_inst):
    blocks = []
    current_block = []
    for inst in list_of_inst:
        if inst[0] == 'inp' and len(current_block) > 0:
            blocks.append(current_block)
            current_block = [inst]
        else:
            current_block.append(inst)
    blocks.append(current_block)
    return blocks


def solve_block(block, target):
    solutions = []
    alu = Alu('0')
    print(get_z_range(block))
    for z in range(get_z_range(block)+1):
        for w in range(1, 10):
            alu.clear(str(w))
            alu._vars['z'] = z
            res = alu.process(block)
            #print(f"{w} - {z} - {res}")
            if res == target:
                solutions.append((w, z))
    return solutions


def sim_block(z, w, a, b, c):
    if (z % 26 + a) == w:
        return z // c
    else:
        return (z//c) * 26 + w + b


def solve_block_ct(target, a, b, c):
    sol = []
    for w in range(1, 10):
        # branch1
        b1 = target * c
        for offs in range(0, c):
            z = b1 + offs
            if z % 26 == (w-a) and z // c == target:
                sol.append((w, z))
        # branch 2
        b2 = round((target - w - b)/26) * c
        for offs in range(0, c):
            z = b2 + offs
            if z % 26 != (w-a) and ((z//c) * 26 + w + b) == target:
                sol.append((w, z))
    return sol


def get_z_range(block):
    for inst in block:
        if inst[0] == 'div' and inst[1] == 'z' and inst[2] == '26':
            return 27 * 27
    return 27


def reduce_states_max(agenda):
    result = defaultdict(int)
    for state, val in agenda:
        if int(val) > int(result[state]):
            result[state] = val
    return list(result.items())


def reduce_states_min(agenda):
    result = defaultdict(lambda: '99999999999999')
    for state, val in agenda:
        if int(val) < int(result[state]):
            result[state] = val
    return list(result.items())


def get_cts(block):
    return int(block[5][2]), int(block[15][2]), int(block[4][2])


def reverse_engineer_max(program):
    blocks = split_inputs(program)
    agenda = [(0, '')]
    for idx, block in enumerate(reversed(blocks)):
        print(f"block {idx} - targets {len(agenda)}")
        new_agenda = []
        for node in agenda:
            sols = solve_block_ct(node[0], *get_cts(block))
            for inp, state in sols:
                new_agenda.append((state, str(inp) + node[1]))
        agenda = reduce_states_max(new_agenda)
        #print(agenda)
    max_node = max(agenda, key=lambda n: int(n[1]))
    return max_node[1]


def reverse_engineer_min(program):
    blocks = split_inputs(program)
    agenda = [(0, '')]
    for idx, block in enumerate(reversed(blocks)):
        print(f"block {idx} - targets {len(agenda)}")
        new_agenda = []
        for node in agenda:
            sols = solve_block_ct(node[0], *get_cts(block))
            for inp, state in sols:
                new_agenda.append((state, str(inp) + node[1]))
        agenda = reduce_states_min(new_agenda)
        print(agenda)
    min_node = min(agenda, key=lambda n: int(n[1]))
    return min_node[1]


if __name__ == '__main__':
    def _main():
        with open('../inputs/day24.txt', 'r') as f:
            program = [tuple(s.strip().split()) for s in f]

        print(reverse_engineer_max(program))
        print(reverse_engineer_min(program))

    _main()
