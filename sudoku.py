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

    def load_grid(self, puzzle: Iterable[Iterable]) -> None:
        """Make a list in list format form the sting in list format"""
        for puzzle_row in puzzle:
            row = [int(x) for x in puzzle_row]
            self._grid.append(row)

    def load_row_columns(self) -> None:
        """Loading the row and column dictionaries and the empty value list"""
        for y in range(9):
            for x in range(9):
                value = self._grid[y][x]

                # append row values to row
                self._dict_rows[y].append(value)

                # append column value to column
                self._dict_columns[x].append(value)

    def load_blocks(self) -> None:
        """Make a list of all the blocks and put these lists in a dictionary"""
        for i in range(9):
            x_start = (i // 3) * 3
            y_start = (i % 3) * 3

            for x in range(x_start, x_start + 3):
                for y in range(y_start, y_start + 3):
                    self._dict_blocks[i].append(self._grid[x][y])

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        # update grid
        self._grid[y][x] = value

        # update row-dictionary
        self._dict_rows[y][x] = value

        # update column-dictionary
        self._dict_columns[x][y] = value

        # update block-dictionary
        block = (y // 3) * 3 + x // 3
        index = (x % 3) * (y % 3) + (x % 3) + (y % 3)
        self._dict_blocks[block][index] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self.place(0, x, y)

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        block = (y // 3) * 3 + x // 3
        used = set(self._dict_blocks[block]) | set(self._dict_rows[y]) | set(self._dict_columns[x])

        return [x for x in values if x not in used]

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            for x in range(9):
                if self._grid[y][x] == 0:
                    return(x, y)

        return (-1, -1)

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for i in range(9):
            if set(self._dict_rows[i]) != values:
                return False

            if set(self._dict_columns[i]) != values:
                return False

            if set(self._dict_blocks[i]) != values:
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
