"""Less boilerplate"""

def sgn(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


def count_overlaps(grid):
    return sum(covers > 1 for row in grid for covers in row)


def parse_line(s: str) -> tuple[int, int, int, int]:
    start, end = s.split("->")
    x1, y1 = map(int, start.split(","))
    x2, y2 = map(int, end.split(","))
    return x1, y1, x2, y2


def main():
    with open("input.txt") as f:
        inp = f.readlines()
    height = width = 1001
    grid = [[0 for _ in range(height)] for _ in range(width)]
    for inp_line in inp:
        x1, y1, x2, y2 = parse_line(inp_line)
        x_step = sgn(x2 - x1)
        y_step = sgn(y2 - y1)
        while x1 != x2 + x_step or y1 != y2 + y_step:
            grid[x1][y1] += 1
            x1 += x_step
            y1 += y_step
    print(count_overlaps(grid))


if __name__ == "__main__":
    main()

