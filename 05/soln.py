class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def is_straight(self):
        return self.x1 == self.x2 or self.y1 == self.y2


class Grid:
    def __init__(self, width, height):
        self.grid = [[0 for _ in range(height)] for _ in range(width)]

    def cover(self, line):
        x1, x2, y1, y2 = line.x1, line.x2, line.y1, line.y2
        if x1 == x2:
            y1, y2 = sorted([y1, y2])
            for y in range(y1, y2 + 1):
                self.grid[x1][y] += 1
        if y1 == y2:
            x1, x2 = sorted([x1, x2])
            for x in range(x1, x2 + 1):
                self.grid[x][y1] += 1

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
        if line.is_straight():
            grid.cover(line)
    print(grid.count_overlaps())


if __name__ == "__main__":
    main()

