import time
from collections import deque

import numpy as np
from scipy.spatial.distance import pdist, squareform


def get_dists(scanners):
    result = {}
    for scanner, beacons in scanners.items():
        dists = pdist(beacons)
        result[scanner] = dists
    return result


def find_matches(dists, source_scanner):
    source_dists = set(dists[source_scanner])
    matches = []
    for scanner, target_dists in dists.items():
        if source_scanner == scanner:
            continue
        if len(source_dists.intersection(target_dists)) >= 66:
            matches.append(scanner)

    return matches


def count_matches(scanners, dists):
    nscanners = len(scanners)
    result = np.zeros((nscanners,nscanners), dtype=int)

    for scanner1 in scanners:
        source_dists = set(dists[scanner1])

        for scanner2 in scanners:
            if scanner1 == scanner2:
                continue
            target_dists = set(dists[scanner2])
            result[scanner1, scanner2] = len(source_dists.intersection(target_dists))

    return result


def match_beacons(scanner1, scanner2, scanners, dists, nmatches=11):
    beacons1 = scanners[scanner1]
    beacons2 = scanners[scanner2]
    dists1 = squareform(dists[scanner1])
    dists2 = squareform(dists[scanner2])

    matched = [[], []]

    for idx1, b1 in enumerate(beacons1):
        b1dists = set(dists1[idx1, :])
        for idx2, b2 in enumerate(beacons2):
            b2dists = set(dists2[idx2, :])
            if len(b1dists.intersection(b2dists)) >= nmatches:
                matched[0].append(tuple(b1))
                matched[1].append(tuple(b2))
                continue
    return np.array(matched[0], dtype=int), np.array(matched[1], dtype=int)


def transform_beacons(scanner1, scanner2, scanners, dists):
    source, dest = match_beacons(scanner1, scanner2, scanners, dists)
    sol = np.linalg.lstsq(np.hstack([source, np.ones((len(source), 1), dtype=int)]),
                          dest,
                          rcond=None)[0]
    rot = np.rint(sol[:3, :]).astype(int)
    trans = np.rint(sol[3:, :]).astype(int)
    source_beacons = scanners[scanner1]
    return (rot.T@source_beacons.T+trans.T).T, trans


def merge_scanners(scanners):
    dists = get_dists(scanners)

    while len(scanners) > 1:
        visited = set()
        new_scanners = {}
        new_dists = {}
        for scanner, beacons in scanners.items():
            matches = find_matches(dists, scanner)
            if len(matches) == 0:
                new_scanners[scanner] = beacons
                new_dists[scanner] = dists[scanner]
            for match in matches:
                if match in new_scanners:
                    continue
                new_beacons = transform_beacons(match, scanner, scanners, dists)
                beacons = np.vstack([beacons, new_beacons])
            unique_beacons = np.vstack(list({tuple(row) for row in beacons}))
            new_scanners[scanner] = unique_beacons
            new_dists[scanner] = pdist(unique_beacons)
        for scanner in visited:
            dists.pop(scanner)
            scanners.pop(scanner)

    return scanners


def solve_scanners(scanners, start):
    known = []
    agenda = deque([start])
    unknown = set(list(scanners.keys()))
    unknown.remove(start)
    beacons = scanners[start]
    dists = get_dists(scanners)
    offsets = {0: (0,0,0)}
    while len(agenda) > 0:
        scanner = agenda.pop()
        matches = find_matches(dists, scanner)
        current_beacons = scanners[scanner]
        for match in matches:
            if match in unknown:
                unknown.remove(match)
                agenda.append(match)
                new_beacons, offs = transform_beacons(match, scanner, scanners, dists)
                offsets[match] = offs
                scanners[match] = new_beacons
                current_beacons = np.vstack([current_beacons, new_beacons])
                beacons = np.vstack([beacons, new_beacons])
        known.append(scanner)
        if len(unknown) == 0:
            break
    unique_beacons = np.vstack(list({tuple(row) for row in beacons}))
    unique_dists = pdist(unique_beacons)
    new_scanners, new_dists = {}, {}
    new_scanners[start] = unique_beacons
    new_dists[start] = unique_dists
    for scanner in unknown:
        new_scanners[scanner] = scanners[scanner]
        new_dists[scanner] = dists[scanner]
    return new_scanners, new_dists, offsets


def rotation_matrices_z():
    result = []
    for angle in [0, 90, 180, 270]:
        rads = np.radians(angle)
        result.append(
            np.array([
                [np.cos(rads), -np.sin(rads), 0],
                [np.sin(rads), np.cos(rads), 0],
                [0, 0,1]
            ])
        )
    return result


def rotation_matrices_y():
    result = []
    for angle in [0, 90, 180, 270]:
        rads = np.radians(angle)
        result.append(
            np.array([
                [np.cos(rads), 0, np.sin(rads)],
                [0, 1, 0],
                [-np.sin(rads), 0, np.cos(rads)]
            ])
        )
    return result


def rotation_matrices_x():
    result = []
    for angle in [0, 90, 180, 270]:
        rads = np.radians(angle)
        result.append(
            np.array([
                [1, 0, 0],
                [0, np.cos(rads), -np.sin(rads)],
                [0, np.sin(rads), np.cos(rads)]
            ])
        )
    return result


def all_rotations():
    results = []
    for rx in rotation_matrices_x():
        for ry in rotation_matrices_y():
            for rz in rotation_matrices_z():
                rot = tuple(map(tuple, rx @ ry @ rz))
                if rot not in results:
                    results.append(rot)
    return [np.array(r) for r in results]


def brute_force(set1, set2):
    for rot in all_rotations():
        offset = set1 - (rot.T @ set2.T).T
        if np.all([ np.allclose(offset[i], offset[0]) for i in range(1, len(offset))]):
            return rot, offset[0]


def merge_scanners(scanner1, scanner2, scanners):
    dists = {scanner1: pdist(scanners[scanner1]), scanner2: pdist(scanners[scanner2])}
    b1, b2 = match_beacons(scanner1, scanner2, scanners, dists, 5)
    if len(b1) < 2:
        return scanners

    rot, offs = brute_force(b1, b2)
    transformed = np.rint((rot.T @ scanners[scanner2].T + offs[:, None]).T).astype(int)
    new_beacons = np.vstack([scanners[scanner1], transformed])
    unique_beacons = np.vstack(list({tuple(row) for row in new_beacons}))
    scanners[scanner1] = unique_beacons
    scanners.pop(scanner2)
    return scanners


def merge_all(source, scanners):
    all_scanners = list(scanners.keys())
    for scanner in all_scanners:
        if scanner != source:
            scanners = merge_scanners(source, scanner, scanners)
    return scanners


if __name__ == '__main__':
    def _main():
        with open('../inputs/day19.txt', 'r') as f:
            inp = {}
            scanner = -1
            beacons = []
            for line in f:
                if line.startswith('---'):
                    if len(beacons) > 0:
                        inp[scanner] = np.array(beacons, dtype=int)
                    scanner += 1
                    beacons = []
                elif line.strip() == '':
                    continue
                else:
                    beacons.append(tuple(int(s) for s in line.strip().split(',')))
            inp[scanner] = np.array(beacons, dtype=int)  # don't forget last scanner ...

            t = time.time()
            sc, d, o = solve_scanners(inp, 0)
            print(f"Star 1: {len(sc[0])}")

            offs = np.vstack(list(o.values()))
            print(f"Star 2: {int(np.max(pdist(offs, 'cityblock')))}")
            print(time.time() - t)













    _main()
