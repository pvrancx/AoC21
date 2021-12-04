import numpy as np


def binary_to_int(bit_array):
    return bit_array.dot(2**np.arange(bit_array.shape[-1])[::-1])


def count_bits(bit_array):
    total = np.sum(bit_array, axis=0)
    gamma = total > bit_array.shape[0] // 2
    eps = np.logical_not(gamma)
    return binary_to_int(gamma) * binary_to_int(eps)


def most_common_op(bit_array, bit_id):
    return np.sum(bit_array[:, bit_id]) >= np.ceil(bit_array.shape[0] / 2.)


def least_common_op(bit_array, bit_id):
    return not(most_common_op(bit_array, bit_id))


def reduce_array(bit_array, op):
    for bit in range(bit_array.shape[-1]):
        target = int(op(bit_array, bit))
        bit_array = bit_array[bit_array[:, bit] == target, ]
        if bit_array.shape[0] == 1:
            return bit_array.flatten()
    return bit_array


def star2(bit_array):
    return binary_to_int(reduce_array(bit_array, most_common_op)) *\
           binary_to_int(reduce_array(bit_array, least_common_op))


if __name__ == '__main__':
    with open('../inputs/day3.txt', 'r') as f:
        inp = f.readlines()

    inp = np.array([list(s.strip()) for s in inp], dtype=int)

    test_inp = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010']
    test_inp = np.array([list(s.strip()) for s in test_inp], dtype=int)

    print(count_bits(inp))
    print(star2(inp))

