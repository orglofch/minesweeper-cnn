import minesweeper

def print_usage():
    """Prints a usage error message to stdout."""
    print("""
    Commands:
       sweep <x> <y> - Sweep a location for mines.
       flag <x> <y>  - Flag a location as being a mine.
       exit          - Exit the game
    """);

def run_sweep(input_pieces: list[str],
              field: minesweeper.Field) -> minesweeper.FieldState:
    """Runs the 'sweep' command.

    Raises:
      ValueError: If input_pieces is malformed.
    """
    x = int(input_pieces[1])
    y = int(input_pieces[2])
    return field.Sweep(x, y)

def run_flag(input_pieces: list[str],
             field: minesweeper.Field):
    """Runs the 'flag' command.

    Raises:
      ValueError: If input_pieces is malformed.
    """
    x = int(input_pieces[1])
    y = int(input_pieces[2])
    field.Flag(x, y)

def print_field(field: minesweeper.Field):
    """Prints a field to stdout."""
    for i, row in enumerate(field.proximity):
        for j, value in enumerate(row):
            mask = field.mask[i][j]
            symbol: str = None
            if mask == 0:
                symbol = '_'
            elif mask == 2:
                symbol = 'P'
            elif value == -1:
                symbol = '*'
            else:
                symbol = value
            print(symbol, end=' ')
        print('')

def main():
    field = minesweeper.Field(100, 50, 500)

    field_state = minesweeper.FieldState.UNSOLVED
    while field_state == minesweeper.FieldState.UNSOLVED:
        input_pieces = input("Enter command: ").split(' ')
        if not input_pieces:
            print('Invalid command')
            print_usage()

        try:
            if input_pieces[0] == 'sweep':
                field_state = run_sweep(input_pieces, field)
            elif input_pieces[0] == 'flag':
                run_flag(input_pieces, field)
            elif input_pieces[0] == 'exit':
                return
            else:
                print_usage()
                continue
        except ValueError:
            print_usage()
            continue

        print_field(field)
        if field_state == minesweeper.FieldState.FAILED:
            print('Game over')
            break
        elif field_state == minesweeper.FieldState.SOLVED:
            print('Solved')
            break
        print('')

if __name__ == "__main__":
    main()
