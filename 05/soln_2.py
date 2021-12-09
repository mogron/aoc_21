class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def sgn(x):
    return 1 if x > 0 else (-1 if x < 0 else 0)


class Grid:
    def __init__(self, width, height):
        self.grid = [[0 for _ in range(height)] for _ in range(width)]

    def cover(self, line):
        x1, x2, y1, y2 = line.x1, line.x2, line.y1, line.y2
        x_step = sgn(x2 - x1)
        y_step = sgn(y2 - y1)
        while x1 != x2 + x_step or y1 != y2 + y_step:
            self.grid[x1][y1] += 1
            x1 += x_step
            y1 += y_step

    def count_overlaps(self):
        return sum(covers > 1 for row in self.grid for covers in row)


def parse_line(s: str) -> Line:
    start, end = s.split("->")
    x1, y1 = map(int, start.split(","))
    x2, y2 = map(int, end.split(","))
    line = Line(x1, y1, x2, y2)
    return line


def main():
    with open("input.txt") as f:
        inp = f.readlines()
    lines = map(parse_line, inp)
    grid = Grid(1001, 1001)
    for line in lines:
        grid.cover(line)
    print(grid.count_overlaps())


if __name__ == "__main__":
    main()

