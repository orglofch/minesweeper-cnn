from enum import Enum
import numpy
import random

class FieldState(Enum):
    UNSOLVED = 1
    SOLVED = 2
    FAILED = 3

class Field:
    """A field containing mines.

    Attributes:
      width: The width of the field.
      height: The height of the field.
      mask: A 2D array indicating revealed portions of the field. False indicates a cell
            is hidden. True indicates a cell is revealed.
      proximity: A 2D array indicating proximity to mines (e.g. a value of 2 indicates
                 2 adjacent mines). -1 indicates a mine.
    """
    def __init__(self, width: int, height: int, num_mines: int):
        self.width = width
        self.height = height
        self.mask = numpy.zeros((height, width), numpy.bool_)
        self.proximity = numpy.zeros((height, width), numpy.int8)

        # Generate mines.
        for _ in range(num_mines):
            x = None
            y = None
            while True:
                x = random.randrange(0, width - 1)
                y = random.randrange(0, height - 1)
                if (self.proximity[y][x] != -1):
                    break;
            self.proximity[y][x] = -1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < width and 0 <= ny < height and self.proximity[ny][nx] != -1:
                        self.proximity[ny][nx] += 1

    def Sweep(self, x: int, y: int) -> FieldState:
        """Sweep a cell in the field for mines.

        Returns:
          The state of the field after the sweep.
        """
        proximity = self.proximity[y][x];
        if proximity == -1:
            # A mine has been hit.
            self.mask[y][x] = 1
            return FieldState.FAILED
        elif not self.mask[x][y]:
            # Expand the mask via flood-fill.
            queue = [(x, y)]
            visited = numpy.zeros((self.height, self.width), numpy.bool_)
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
                if value != -1 and not self.mask[i][j]:
                    solved = False
                    break
            if not solved:
                break
        return FieldState.SOLVED if solved else FieldState.UNSOLVED
