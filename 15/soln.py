from collections import defaultdict
import heapq
from dataclasses import dataclass, field
from typing import Any


def print_grid(grid):
    print("-" * len(grid[0]))
    print(*["".join(map(str, row)) for row in grid], sep="\n")


def get_neighbours(grid, row_idx, col_idx):
    height = len(grid)
    width = len(grid[0]) if height else 0
    row_min = max(0, row_idx - 1)
    row_max = min(width - 1, row_idx + 1)
    col_min = max(0, col_idx - 1)
    col_max = min(height - 1, col_idx + 1)
    for ri in range(row_min, row_max + 1):
        for ci in range(col_min, col_max + 1):
            if ri == row_idx and ci == col_idx:
                continue
            # exclude diagonals
            if ri != row_idx and ci != col_idx:
                continue
            yield ri, ci


@dataclass(order=True)
class Node:
    # f = g + h
    # g = cost to get here
    # h = heuristic estimate to get from here to target
    # x, y = here, meaning node location
    # pre = predecessor Node
    f: int
    g: int = field(compare=False)
    h: int = field(compare=False)
    x: int = field(compare=False)
    y: int = field(compare=False)
    pre: Any = field(compare=False)


class AStar:
    def __init__(self, rows):
        self.rows = rows
        self.target_y = len(rows) - 1
        self.target_x = len(rows[0]) - 1
        self.q = []
        self.g_map = defaultdict(lambda: 10e9)

    def run(self):
        self.add_node(0, 0, None)
        while self.q:
            cur = heapq.heappop(self.q)
            if cur.x == self.target_x and cur.y == self.target_y:
                print("goal!")
                return cur
            for y, x in get_neighbours(self.rows, cur.y, cur.x):
                self.add_node(x, y, cur)

    def add_node(self, x, y, pre):
        h = abs(self.target_y - y) + abs(self.target_x - x)
        g = pre.g if pre else -self.rows[y][x]
        g += self.rows[y][x]
        if self.g_map[(x, y)] <= g:
            return
        self.g_map[(x, y)] = g
        node = Node(g + h, g, h, x, y, pre)
        heapq.heappush(self.q, node)


def inc(elem, i):
    elem += i
    while elem > 9:
        elem -= 9
    return elem


def tile(rows, width, height):
    tiles = [[] for _ in range(len(rows) * height)]
    for i in range(height):
        h_offset = i * len(rows)
        for j in range(width):
            val = i + j
            for row_idx, row in enumerate(rows):
                tiles[h_offset + row_idx].extend([inc(elem, val) for elem in row])
    return tiles


def main():
    with open("input.txt") as f:
        inp = f.read().splitlines()
    rows = [list(map(int, line)) for line in inp]
    rows = tile(rows, 5, 5)
    astar = AStar(rows)
    target = astar.run()
    print(target.g)


if __name__ == "__main__":
    main()
