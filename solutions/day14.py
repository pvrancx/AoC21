from collections import defaultdict
from typing import Dict


def step(polymer: str, rules: Dict[str, str]) -> str:
    """naive solution - does not scale to 40 steps"""
    chars = list(polymer)
    result = []
    for idx in range(len(chars) - 1):
        ch1, ch2 = chars[idx], chars[idx + 1]
        ch3 = rules[ch1+ch2]
        result += [ch1, ch3]
    result.append(chars[-1])
    return ''.join(result)


def star(polymer: str, rules: Dict[str, str], nsteps: int) -> int:
    pair_dict = str2dct(polymer)  # only keep pair counts, not entire string
    for _ in range(nsteps):
        pair_dict = step_pairs(pair_dict, rules)
    counts = count_chars(polymer, pair_dict)
    min_el = min(counts, key=counts.get)
    max_el = max(counts, key=counts.get)

    return counts[max_el] - counts[min_el]


def str2dct(polymer: str) -> Dict[str, int]:
    chars = list(polymer)
    counts = defaultdict(lambda: 0)
    for idx in range(len(chars) - 1):
        ch1, ch2 = chars[idx], chars[idx + 1]
        counts[ch1+ch2] += 1
    return counts


def step_pairs(pair_dict: Dict[str, int], rules: Dict[str, str]) -> Dict[str, int]:
    result = defaultdict(lambda: 0)
    for pair, count in pair_dict.items():
        ch = rules[pair]
        result[pair[0] + ch] += count
        result[ch + pair[1]] += count
    return result


def count_chars(polymer: str, pair_dict: Dict[str, int]) -> Dict[str, int]:
    result = defaultdict(lambda: 0)
    for pair, count in pair_dict.items():
        result[pair[0]] += count
        result[pair[1]] += count
    for ch in result.keys():
        result[ch] = result[ch] // 2  # each char is part of 2 pairs so was double counted
        if ch == polymer[0] or ch == polymer[-1]:
            result[ch] += 1  # first and last char are not part of 2 pairs
    return result


if __name__ == '__main__':
    def _main():
        with open('../inputs/day14.txt', 'r') as f:
            polymer = f.readline().strip()
            f.readline()
            rules = {}
            for line in f:
                l, r = line.strip().split(' -> ')
                rules[l] = r

        print(f"Star 1: {star(polymer, rules, 10)}")
        print(f"Star 2: {star(polymer, rules, 40)}")

    _main()
