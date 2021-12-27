import minesweeper

from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_integer('width', 32,
                     'The width of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('height', 16,
                     'The height of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('num_mines', 99,
                     'The number of mines in the field.',
                     lower_bound=0)

def print_usage():
    """Prints a usage error message to stdout."""
    print("""
    Commands:
       sweep <x> <y>     - Sweep a location for mines.
       flag <x> <y>      - Flag a location as being a mine.
       exit              - Exit the game
    """);

def run_sweep(input_pieces: list[str],
              field: minesweeper.Field):
    """Runs the 'sweep' command.

    Raises:
      ValueError: If `input_pieces` is malformed.
    """
    x = int(input_pieces[1])
    y = int(input_pieces[2])
    field.Sweep(x, y)

def run_flag(input_pieces: list[str],
             field: minesweeper.Field):
    """Runs the 'flag' command.

    Raises:
      ValueError: If `input_pieces` is malformed.
    """
    x = int(input_pieces[1])
    y = int(input_pieces[2])
    field.Flag(x, y)

def main(argv):
    width = FLAGS.width
    height = FLAGS.height
    num_mines = FLAGS.num_mines

    field = minesweeper.Field(width, height, num_mines)
    field.pretty_print()

    while not field.IsCompleted():
        input_pieces = input("Enter command: ").split(' ')
        if not input_pieces:
            print('Invalid command')
            print_usage()

        try:
            if input_pieces[0] == 'sweep':
                run_sweep(input_pieces, field)
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

        field.pretty_print()
        print('')
    termination_state_color = 'red' if field.state == minesweeper.FieldState.FAILED else 'green'
    print(termcolor.colored(field.state, termination_state_color))

if __name__ == "__main__":
    app.run(main)
