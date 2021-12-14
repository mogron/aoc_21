def fold(f, p):
    return min(p, 2 * f - p)


def apply(instruction, points):
    axis, val = instruction
    if axis == "x":
        return set((fold(val, x), y) for x, y in points)
    else:
        return set((x, fold(val, y)) for x, y in points)


def main():
    with open("input.txt") as f:
        inp = f.readlines()
    points = set()
    instructions = []
    for line in inp:
        line = line.strip()
        if "," in line:
            x, y = map(int, line.split(","))
            points.add((x, y))
        if "fold" in line:
            axis, val = line[11:].split("=")
            val = int(val)
            instructions.append((axis, val))
    for instruction in instructions:
        points = apply(instruction, points)
        print(len(points))
    max_x = max(x for x, _ in points) + 1
    max_y = max(y for _, y in points) + 1
    grid = [[" "] * max_x for i in range(max_y)]
    for x, y in points:
        grid[y][x] = "#"
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    main()
