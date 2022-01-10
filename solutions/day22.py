import numpy as np


def check_range(coords):
    x, y, z = coords
    return x[0]< -50 or x[1] > 50 or y[0] < -50 or y[1] > 50 or z[0]< -50 or z[1] > 50


def star1(cmds):
    result = np.zeros((101, 101, 101))
    for cmd in cmds:
        print(cmd)
        turn_on, coords = cmd
        if check_range(coords):
            'range'
            continue
        x, y, z = coords
        print(x)
        print(y)
        print(z)
        print(turn_on)
        if turn_on:
            print('on')
            result[x[0]+50:x[1]+51, y[0]+50:y[1]+51, z[0]+50:z[1]+51] = 1
        else:
            'off'
            result[x[0]+50:x[1]+51, y[0]+50:y[1]+51, z[0]+50:z[1]+51] = 0
    return np.sum(result)


def intersect_range(range1, range2):
    x1, x2 = range1
    y1, y2 = range2
    if x2 < y1 or y2 < x1:
        return None
    coords = [x1, x2, y1, y2]
    coords.sort()
    return coords[1], coords[2]


def intersect_cube(cube1, cube2):
    x1, y1, z1 = cube1
    x2, y2, z2 = cube2
    x_int = intersect_range(x1, x2)
    y_int = intersect_range(y1, y2)
    z_int = intersect_range(z1, z2)
    if not (x_int and y_int and z_int):
        return None
    else:
        return x_int, y_int, z_int


def volume_cube(cube):
    x, y, z = cube
    return (x[1] - x[0] + 1) * (y[1] - y[0] + 1) * (z[1] - z[0] + 1)


class Volume:
    def __init__ (self, cube):
        self._cube = cube
        self._removed = []

    def remove(self, cube):
        # remove the intersection with this cube
        intersection = intersect_cube(cube, self._cube)
        if not intersection:
            return
        for vol in self._removed:
            # make sure we don't remove intersection multiple times
            # |V| - (|A| + |B| - |A int B|)
            vol.remove(intersection)
        self._removed.append(Volume(intersection))

    def get_volume(self):
        total = volume_cube(self._cube)
        for volume in self._removed:
            total -= volume.get_volume()
        return total


def star2(cmds):
    volumes = []
    for cmd in cmds:
        turn_on, cube = cmd
        if turn_on:
            #  add volume, remove intersection from other volumes to prevent double counting
            for vol in volumes:
                vol.remove(cube)
            volumes.append(Volume(cube))
        else:
            for vol in volumes:
                vol.remove(cube)
    return sum([v.get_volume() for v in volumes])


if __name__ == '__main__':
    def _main():
        with open('../inputs/day22.txt', 'r') as f:
            inp = []
            for line in f:
                cmd, coords = line.strip().split()
                x, y, z = coords.split(',')
                xrange = tuple(int(s) for s in x.split('=')[-1].split('..'))
                yrange = tuple(int(s) for s in y.split('=')[-1].split('..'))
                zrange = tuple(int(s) for s in z.split('=')[-1].split('..'))

                inp.append((cmd == 'on', (xrange, yrange, zrange)))

            print(inp)
            print(star1(inp))
            print(intersect_range((-10,-5), (-5,121)))
            print(star2(inp))


    _main()
