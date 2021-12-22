from dataclasses import dataclass
from itertools import combinations
from math import floor
from random import randrange

Point = tuple[int, int, int]


@dataclass
class Cube:
    p_min: Point
    p_max: Point


@dataclass
class Switch:

    on: bool
    cube: Cube


def point_in(p: Point, cube: Cube):
    return all(cube.p_min[i] <= p[i] <= cube.p_max[i] for i in range(3))


def corners(cube: Cube):
    a = cube.p_min
    b = cube.p_max
    for x in [a[0], b[0]]:
        for y in [a[1], b[1]]:
            for z in [a[2], b[2]]:
                yield (x, y, z)


def intersect(cube, other):
    # two cubes intersect if they overlap on each axis
    for axis in range(3):
        lower = max(cube.p_min[axis], other.p_min[axis])
        upper = min(cube.p_max[axis], other.p_max[axis])
        if lower > upper:
            return False
    return True


def slice_cube(cube, axis, val) -> tuple[Cube, Cube]:
    # lower cube
    p_max = tuple(
        [
            cube.p_max[ax] if ax != axis else min(cube.p_max[ax], floor(val))
            for ax in range(3)
        ]
    )
    cube_lower = Cube(p_min=cube.p_min, p_max=p_max)
    # upper cube
    p_min = tuple(
        [
            cube.p_min[ax] if ax != axis else max(cube.p_min[ax], floor(val + 1))
            for ax in range(3)
        ]
    )
    cube_upper = Cube(p_min=p_min, p_max=cube.p_max)
    return cube_lower, cube_upper


def vol(cube) -> int:
    v = 1
    for axis in range(3):
        v *= max(0, 1 + cube.p_max[axis] - cube.p_min[axis])
    return v


def cut(orig_cube, other) -> list[Cube]:
    if intersect(orig_cube, other):
        cubes = [orig_cube]
        for axis in range(3):
            for cut_point in [other.p_min[axis] - 0.5, other.p_max[axis] + 0.5]:
                new_cubes = []
                for cube in cubes:
                    sliced_cubes = slice_cube(cube, axis, cut_point)
                    new_cubes.extend(
                        [
                            sliced_cube
                            for sliced_cube in sliced_cubes
                            if vol(sliced_cube) > 0
                        ]
                    )
                cubes = new_cubes
    non_intersections = [cube for cube in cubes if not intersect(cube, other)]
    return non_intersections


def union(cubes, other):
    new_cubes = [other]
    for cube in cubes:
        if intersect(cube, other):
            # cut other out of cube
            cut_cubes = cut(cube, other)
            new_cubes.extend(cut_cubes)
        else:
            new_cubes.append(cube)
    return new_cubes


def cut_many(cubes, other):
    new_cubes = []
    for cube in cubes:
        if intersect(cube, other):
            # cut other out of cube
            cut_cubes = cut(cube, other)
            new_cubes.extend(cut_cubes)
        else:
            new_cubes.append(cube)
    return new_cubes


def process(switches: list[Switch]):
    cubes: list[Cube] = []
    for i, switch in enumerate(switches):
        print(f"Switch {i}")
        print(f"Cubes: {len(cubes)}")

        if switch.on:
            cubes = union(cubes, switch.cube)
        else:
            cubes = cut_many(cubes, switch.cube)
    return sum(vol(cube) for cube in cubes)


def parse_min_max(s):
    a, b = s[2:].split("..")
    return int(a), int(b)


def naive_range(a, b):
    a += 50
    b += 50
    return range(max(a, 0), min(b, 100) + 1)


def solve_naive(switches: list[Switch]):
    grid = [[[0 for _ in range(101)] for _ in range(101)] for _ in range(101)]
    for switch in switches:
        c = switch.cube
        val = int(switch.on)
        for x in naive_range(c.p_min[0], c.p_max[0]):
            for y in naive_range(c.p_min[1], c.p_max[1]):
                for z in naive_range(c.p_min[2], c.p_max[2]):
                    grid[x - 50][y - 50][z - 50] = val
    total = 0
    for xs in grid:
        for ys in xs:
            total += sum(ys)
    return total


def random_cube():
    a = randrange(-50, 51)
    b = randrange(-50, 51)
    c = randrange(-50, 51)
    x = (a, b, c)
    d = min(a + randrange(101), 50)
    e = min(b + randrange(101), 50)
    f = min(c + randrange(101), 50)
    y = (e, d, f)
    return Cube(x, y)


def test():
    for i in range(500):
        if i % 10 == 0:
            print(i)
        cube_a = random_cube()
        switch_a = Switch(True, cube_a)
        cube_b = random_cube()
        switch_b = Switch(False, cube_b)
        switches = [switch_a, switch_b]
        sol_naive = solve_naive(switches)
        sol = process(switches)
        print(sol)
        print(sol_naive)
        assert sol_naive == sol, switches


def main():
    with open("input.txt") as f:
        inp = f.read().splitlines()
    switches = []
    # test()
    for line in inp:
        s_on, rest = line.split()
        on = s_on == "on"
        x, y, z = map(parse_min_max, rest.split(","))
        p_min = (x[0], y[0], z[0])
        p_max = (x[1], y[1], z[1])
        switch = Switch(on, Cube(p_min, p_max))
        switches.append(switch)
    print(switches)
    print("Full solution:", process(switches))
    print("Init region:", solve_naive(switches))


if __name__ == "__main__":
    main()
