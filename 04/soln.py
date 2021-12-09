from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class BoardElement:
    value: int
    is_marked: bool


class Board:
    def __init__(self, rows: Iterable[Iterable[int]]):
        self.is_complete = False
        self.grid: list[list[BoardElement]] = []
        for row in rows:
            processed_row = [BoardElement(val, False) for val in row]
            self.grid.append(processed_row)

    @property
    def value(self) -> int:
        res = 0
        for row in self.grid:
            for elem in row:
                if not elem.is_marked:
                    res += elem.value
        return res

    def check_row_complete(self, row_idx: int) -> bool:
        row = self.grid[row_idx]
        return all(elem.is_marked for elem in row)

    def check_col_complete(self, col_idx: int) -> bool:
        return all(row[col_idx].is_marked for row in self.grid)

    def mark(self, value: int) -> None:
        for row_idx, row in enumerate(self.grid):
            for col_idx, elem in enumerate(row):
                if elem.value == value:
                    elem.is_marked = True
                    col_complete = self.check_col_complete(col_idx)
                    row_complete = self.check_row_complete(row_idx)
                    self.is_complete = col_complete or row_complete


def parse_input() -> tuple[list[int], list[Board]]:
    with open("input.txt") as f:
        inp = f.readlines()
    numbers = map(int, inp[0].split(","))
    # create boards
    boards: list[Board] = []
    for board_start in range(2, len(inp), 6):
        rows = [map(int, inp[board_start + row_num].split()) for row_num in range(5)]
        boards.append(Board(rows))
    return numbers, boards


def main():
    numbers, boards = parse_input()
    # call out numbers
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.is_complete:
                print(board.value * number)
                return


if __name__ == "__main__":
    main()
