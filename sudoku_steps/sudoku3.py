from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[list[int]] = []
        self._dict_rows: dict[int, list[int]] = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        self._dict_columns: dict[int, list[int]] = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        self._dict_blocks: dict[int, list[int]] = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}

        self.load_grid(puzzle)
        self.load_row_columns()
        self.load_blocks()

    def load_grid(self, puzzle: Iterable[Iterable]):
        for puzzle_row in puzzle:
            row = [int(x) for x in puzzle_row]
            self._grid.append(row)

    def load_row_columns(self) -> None:
        for y in range(9):
            for x in range(9):
                value = self.value_at(x, y)
                self._dict_rows[y].append(value)
                self._dict_columns[x].append(value)

    def load_blocks(self) -> None:
        for i in range(9):
            x_start = (i // 3) * 3
            y_start = (i % 3) * 3

            for x in range(x_start, x_start + 3):
                for y in range(y_start, y_start + 3):
                    self._dict_blocks[i].append(self._grid[x][y])

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value
        self._dict_rows[y][x] = value
        self._dict_columns[x][y] = value

        block = (y // 3) * 3 + x // 3
        index = (x % 3) * (y % 3) + (x % 3) + (y % 3)
        self._dict_blocks[block][index] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self.place(0, x, y)

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        try:
            return self._grid[y][x]
        except IndexError:
            return -1

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        for y in range(9):
            for x in range(9):
                if self.value_at(x, y) == 0 and next_x == -1 and next_y == -1:
                    next_x, next_y = x, y

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return self._dict_rows[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return self._dict_columns[i]

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        return self._dict_blocks[i]

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for i in range(9):
            if set(self.column_values(i)) != values:
                return False
            if set(self.row_values(i)) != values:
                return False
            if set(self.block_values(i)) != values:
                return False

        return True

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += "".join(str(x) for x in row) + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
