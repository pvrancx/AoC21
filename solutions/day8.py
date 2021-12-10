
def find_4(patterns):
    for s in patterns:
        if len(s) == 4:
            return s


def find_1(patterns):
    for s in patterns:
        if len(s) == 2:
            return s


def find_8(patterns):
    for s in patterns:
        if len(s) == 7:
            return s


def find_7(patterns):
    for s in patterns:
        if len(s) == 3:
            return s


def find_6(patterns, decoded):
    p8 = set(list(decoded[8]))
    p1 = set(list(decoded[1]))

    for s in patterns:
        if len(s) == 6:
            diff8 = p8 - set(list(s))
            if diff8.issubset(p1):
                return s


def find_0(patterns, decoded):
    p8 = set(list(decoded[8]))
    p41 = set(list(decoded[4])) - set(list(decoded[1]))

    for s in patterns:
        if len(s) == 6 and s != decoded[6]:
            diff8 = p8 - set(list(s))
            if diff8.issubset(p41):
                return s


def find_9(patterns, decoded):
    for s in patterns:
        if len(s) == 6 and s != decoded[6] and s != decoded[0]:
            return s


def find_2(patterns, decoded):
    p8 = set(list(decoded[8]))
    p4 = set(list(decoded[4]))
    for s in patterns:
        if len(s) == 5:
            diff8 = p8 - set(list(s))
            if diff8.issubset(p4):
                return s


def find_3(patterns, decoded):
    p6 = set(list(decoded[6]))
    for s in patterns:
        if len(s) == 5 and s != decoded[2]:
            ps = set(list(s))
            if not ps.issubset(p6):
                return s


def find_5(patterns, decoded):
    for s in patterns:
        if len(s) == 5 and s != decoded[3] and s != decoded[2]:
            return s


def decode_unique(list_of_patterns):
    decoded = {}
    decoded[8] = find_8(list_of_patterns)
    decoded[1] = find_1(list_of_patterns)
    decoded[4] = find_4(list_of_patterns)
    decoded[7] = find_7(list_of_patterns)
    decoded[6] = find_6(list_of_patterns, decoded)
    decoded[0] = find_0(list_of_patterns, decoded)
    decoded[9] = find_9(list_of_patterns, decoded)
    decoded[2] = find_2(list_of_patterns, decoded)
    decoded[3] = find_3(list_of_patterns, decoded)
    decoded[5] = find_5(list_of_patterns, decoded)
    print(decoded)
    return {v: k for k, v in decoded.items()}


def decode_value(lookup, value):
    value_set = set(list(value))
    for k, v in lookup.items():
        if set(list(k)) == value_set:
            return v
    raise RuntimeError('uhoh')


def star2(list_of_patterns, list_of_outputs):
    total = 0
    for pattern, output in zip(list_of_patterns, list_of_outputs):
        lookup = decode_unique(pattern)
        print(pattern)
        print(output)
        print(lookup)
        decoded_output = int(''.join([str(decode_value(lookup, s)) for s in output]))
        total += decoded_output
    return total


def count_unique(list_of_outputs):
    count = 0
    for output in list_of_outputs:
        for s in output:
            if len(s) in [2, 3, 4, 7]:
                count += 1
    return count


if __name__ == '__main__':
    def _main():
        patterns = []
        outputs = []
        with open('../inputs/day8.txt', 'r') as f:
            for line in f:
                pattern, output = line.strip().split('|')
                patterns.append(pattern.split())
                outputs.append(output.split())
        print(patterns)
        print(outputs)
        print(count_unique(outputs))
        print(star2(patterns, outputs))

    _main()
