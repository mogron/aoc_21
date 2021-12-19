from dataclasses import dataclass
from math import sin, cos, pi
from itertools import product, combinations


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash(self.x) + hash(self.y) + hash(self.z)


def subtract(a: Point, b: Point):
    return Point(a.x - b.x, a.y - b.y, a.z - b.z)


def add(a: Point, b: Point):
    return Point(a.x + b.x, a.y + b.y, a.z + b.z)


def l1(a: Point, b: Point):
    """Compute L1/Manhattan distance between a and b"""
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def rotation_fun(a, b, c):
    # a, b, c = rotation angles
    # matrix from here: https://de.wikipedia.org/wiki/Roll-Nick-Gier-Winkel
    ca = cos(a)
    cb = cos(b)
    cc = cos(c)
    sa = sin(a)
    sb = sin(b)
    sc = sin(c)
    m11 = ca * cb
    m12 = ca * sb * sc - sa * cc
    m13 = ca * sb * cc + sa * sc
    m21 = sa * cb
    m22 = sa * sb * sc + ca * cc
    m23 = sa * sb * cc - ca * sc
    m31 = -sb
    m32 = cb * sc
    m33 = cb * cc

    def rotate(p):
        x = p.x * m11 + p.y * m12 + p.z * m13
        y = p.x * m21 + p.y * m22 + p.z * m23
        z = p.x * m31 + p.y * m32 + p.z * m33
        return Point(round(x), round(y), round(z))

    return rotate


def make_rotation_functions():
    u = pi / 2
    rotations = []
    for a_rot in range(4):
        for b_rot in range(4):
            for c_rot in range(4):
                rfun = rotation_fun(a_rot * u, b_rot * u, c_rot * u)
                rotations.append(rfun)

    # filter out equivalent rotations
    ref_points = [Point(1, 0, 0), Point(0, 1, 0), Point(0, 0, 1)]
    reduced_rotations = []
    for i, rf1 in enumerate(rotations):
        redundant = False
        for rf2 in rotations[i + 1 :]:
            if all(rf1(p) == rf2(p) for p in ref_points):
                redundant = True
                break
        if not redundant:
            reduced_rotations.append(rf1)
    return reduced_rotations


def parse_scanner(inp):
    beacons = []
    # skip first line
    try:
        next(inp)
    except StopIteration:
        return None
    for line in inp:
        if line == "":
            break

    return beacons


def parse_scanners(inp):
    scanners = []
    beacons = set()
    for line in inp:
        if line == "" or line.startswith("---"):
            if beacons:
                scanners.append(beacons)
                beacons = set()
            continue
        x, y, z = map(int, line.split(","))
        p = Point(x, y, z)
        beacons.add(p)
    if beacons:
        scanners.append(beacons)
    return scanners


def compute_pairwise_distances(scanner):
    return set([l1(a, b) for a, b in combinations(scanner, 2)])


def maybe_match(scanner_a, scanner_b):
    """By comparing intra-scanner pairwise distances, check if there is any chance that scanner_a and scanner_b match."""
    dists_a = compute_pairwise_distances(scanner_a)
    dists_b = compute_pairwise_distances(scanner_b)
    # if a and b match, at least 12 of their beacons will have the same pairwise distances.
    # so dists_a and dists_b must have at least 1 + 2 + 3 + ... + 11 = 66 elements in common.
    common = dists_a.intersection(dists_b)
    n_common = len(common)
    n_required = 66
    return n_common >= n_required


def find_next_match(q, scanners, rotations):
    # find next scanner that matches one of the solved scanners
    for scanner_a in q:
        for scanner_b_idx, scanner_b in enumerate(scanners):
            if not maybe_match(scanner_a, scanner_b):
                continue
            # try all rotations
            for rotation in rotations:
                scanner_b_rotated = [rotation(beacon) for beacon in scanner_b]
                # how many matches if the i-th beacon of scanner_a was the j-th beacon of scanner_b
                for beacon_a, beacon_b in product(scanner_a, scanner_b_rotated):
                    dist = subtract(beacon_a, beacon_b)
                    t_beacons = set([add(b, dist) for b in scanner_b_rotated])
                    inter = t_beacons.intersection(scanner_a)
                    if len(inter) >= 12:
                        # found a match
                        return scanner_b_idx, t_beacons, dist
    # no match shouldn't happen, given the problem specification
    exit(1)


def process(scanners):
    rotations = make_rotation_functions()
    # scanner 0 is the reference scanner, first find a match with this one
    q = [scanners[0]]
    scanner_positions = []
    del scanners[0]
    while scanners:
        match_idx, t_beacons, scanner_pos = find_next_match(q, scanners, rotations)
        scanner_positions.append(scanner_pos)
        print("found match")
        del scanners[match_idx]
        q.append(t_beacons)
    print(
        "Max distance between scanners:",
        max(l1(a, b) for a, b in combinations(scanner_positions, 2)),
    )
    return q


def main():
    with open("input.txt") as f:
        inp = f.read().splitlines()
    scanners = parse_scanners(inp)
    res = process(scanners)
    beacons = set()
    for scanner in res:
        beacons = beacons.union(scanner)
    print("number of beacons:", len(beacons))


if __name__ == "__main__":
    main()
