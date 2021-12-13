from collections import defaultdict, deque, Counter
from typing import Deque, Tuple, Any, List
import numpy as np


class Graph:
    def __init__(self):
        self._neighb = defaultdict(list)

    def get_nodes(self) -> List[str]:
        return list(self._neighb.keys())

    def add_edge(self, node1, node2):
        self._neighb[node1].append(node2)
        self._neighb[node2].append(node1)

    def get_neighbours(self, node) -> List[str]:
        return self._neighb[node]


def enumerate_paths(graph: Graph, allow_doubles: bool = False):
    agenda = deque([('start',)])  # type: Deque(Tuple[str, ...])
    n_paths = 0

    while len(agenda) > 0:
        path = agenda.pop()
        neighb = graph.get_neighbours(path[-1])
        for n in neighb:
            if n == 'end':
                n_paths += 1
            elif n == 'start':
                continue
            elif n not in path or n.isupper():
                agenda.append(path + (n,))
            elif allow_doubles:
                counts = Counter(path)
                no_doubles = np.all([k.isupper() or v < 2 for k, v in counts.items()])
                if no_doubles and n not in ['start', 'end']:
                    agenda.append(path + (n,))
    return n_paths


if __name__ == '__main__':
    def _main():
        with open('../inputs/day12.txt', 'r') as f:
            g = Graph()
            for line in f:
                n1, n2 = line.strip().split('-')
                g.add_edge(n1, n2)

        print(f"Star 1: {enumerate_paths(g, False)}")
        print(f"Star 2: {enumerate_paths(g, True)}")

    _main()
