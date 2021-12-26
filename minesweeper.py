import numpy as np
import random
import termcolor

from enum import Enum

class FieldState(Enum):
    """The state of the Minesweeper field."""
    UNSOLVED = 1
    SOLVED = 2
    FAILED = 3

class Field:
    """A field containing mines.

    Attributes:
      width: The width of the field.
      height: The height of the field.
      mask: A 2D array indicating revealed portions of the field. 0 indicates a cell
            is hidden. 1 indicates a cell is revealed. 2 indicates a cell is flagged.
      proximity: A 2D array indicating proximity to mines. Positive values indicate
                 adjacent mines. -1 indicates a mine.
      state: The current state of the field.
    """
    def __init__(self, width: int, height: int, num_mines: int):
        self.width = width
        self.height = height
        self.mask = np.zeros((height, width), np.int8)
        self.proximity = np.zeros((height, width), np.int8)
        self.state = FieldState.UNSOLVED

        # Generate mines.
        for _ in range(num_mines):
            x = None
            y = None
            while True:
                x = random.randrange(0, width)
                y = random.randrange(0, height)
                if (self.proximity[y][x] != -1):
                    break;
            self.proximity[y][x] = -1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < width and 0 <= ny < height and self.proximity[ny][nx] != -1:
                        self.proximity[ny][nx] += 1

    def IsCompleted(self) -> bool:
        """Returns whether the field is in a terminal state."""
        return self.state == FieldState.SOLVED or self.state == FieldState.FAILED

    def RandomSafeCell(self) -> (int, int):
        """Returns a random covered safe cell.

        Raises:
          ValueError: If the field is in a completed state.
        """
        if self.IsCompleted():
            raise ConnectionError("There are no remaining covered safe cells")
        candidate_cells = []
        for i, row in enumerate(self.proximity):
            for j, value in enumerate(row):
                if value != -1 and self.mask[i][j] == 0:
                    candidate_cells.append((j, i))
        return candidate_cells[random.randrange(0, len(candidate_cells))]

    def Sweep(self, x: int, y: int):
        """Sweep a cell in the field for mines."""
        mask = self.mask[y][x]
        proximity = self.proximity[y][x]

        if self.state == FieldState.SOLVED or self.state == FieldState.FAILED:
            # The field is already in a finished state.
            return self.state
        if mask == 2:
            # Flags can't be clicked.
            return self.state

        if proximity == -1:
            # A mine has been hit.
            self.mask[y][x] = 1
            self.state = FieldState.FAILED
        elif mask == 0:
            # Expand the mask via flood-fill.
            queue = [(x, y)]
            visited = np.zeros((self.height, self.width), np.bool_)
            while queue:
                (fx, fy) = queue.pop()
                visited[fy][fx] = True

                self.mask[fy][fx] = 1
                if self.proximity[fy][fx] == 0 or (self.proximity[fy][fx] != -1 and fx == x and fy == y):
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            nx = fx + dx
                            ny = fy + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height and self.proximity[ny][nx] != -1 and not visited[ny][nx]:
                                queue.append((nx, ny))

            solved = True
            for i, row in enumerate(self.proximity):
                for j, value in enumerate(row):
                    if value != -1 and self.mask[i][j] == 0:
                        solved = False
                        break
                if not solved:
                    break
            if solved:
                self.state = FieldState.SOLVED

    def Flag(self, x: int, y: int):
        """Flags a cell as a mine."""
        mask = self.mask[y][x]

        if mask == 0:
            self.mask[y][x] = 2
        elif mask == 2:
            self.mask[y][x] = 0

    def pretty_print(self):
        """Print the field with colors."""
        proximity_colors = [
            'cyan',    # 1
            'green',   # 2
            'blue',    # 3
            'magenta', # 4
            'yellow',  # 5
            'white',   # 6
            'white',   # 7
            'white',   # 8
        ]
        out_str = ''
        for i, row in enumerate(self.proximity):
            for j, value in enumerate(row):
                mask = self.mask[i][j]
                if mask == 0:
                    print(termcolor.colored('X', 'grey'), end=' ')
                elif mask == 2:
                    print(termcolor.colored('F', 'red'), end=' ')
                elif value == -1:
                    print(termcolor.colored('*', 'red'), end=' ')
                elif value == 0:
                    print(' ', end=' ')
                else:
                    print(termcolor.colored(value, proximity_colors[value - 1]), end=' ')
            print('')
