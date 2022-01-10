import numpy as np


def bits2int(bitstr):
    return int(bitstr, 2)


def enhance(im, lookup, padding=3, pad_val=0):

    rows, cols = im.shape
    padded_im = np.ones((rows + 2*padding, cols+2*padding), dtype=int) * pad_val
    padded_im[padding:rows+padding, padding:cols+padding] = im[:, :]
    assert np.all(padded_im[padding:rows+padding, padding:cols+padding] == im)
    result = np.zeros_like(padded_im, dtype=int)
    for r in range(padding-1, rows+padding+1):
        for c in range(padding-1, cols+padding+1):
            #assert padded_im[r, c] == im[r-padding, c-padding]
            nrs = padded_im[r-1:r+2, c-1:c+2].flatten()
            bitstr = ''.join([str(i) for i in nrs])
            idx = bits2int(bitstr)
            val = 0 if lookup[idx] == '.' else 1
            result[r, c] = val
    return result[padding-1: rows+padding+1, padding-1:cols+padding+1]


def enhance_steps(im, lookup, n_steps, padding=3, pad_val=0):
    padvals=[0, 511]
    for _ in range(n_steps):
        im = enhance(im, lookup, padding, pad_val)
        pad_val = 1 if lookup[padvals[pad_val]] == '#' else 0
        print(pad_val)
    return im


if __name__ == '__main__':
    def _main():
        with open('../inputs/day20.txt', 'r') as f:
            lookup = f.readline().strip()
            f.readline()
            inp = np.array([[0 if s =='.' else 1 for s in line.strip()] for line in f], dtype=int)

            print(inp[0:3, 0:3])
            #print(enhance(inp, lookup))
            pad_val1 = 0
            pad_val2 = 1 if lookup[pad_val1] == '#' else 0
            res = enhance(enhance(inp, lookup, pad_val=pad_val1), lookup, pad_val=pad_val2)
            res2 = enhance_steps(inp, lookup, 50, 3, pad_val=pad_val1)
            print(res)
            print(res2.shape)
            print(pad_val2)
            print(np.sum(res2))

    _main()
