import minesweeper

def print_field(field: minesweeper.Field):
    for i, row in enumerate(field.proximity):
        for j, value in enumerate(row):
            if not field.mask[i][j]:
                print(' ', end=' ')
            elif value == -1:
                print('*', end=' ')
            else:
                print(value, end=' ')
        print('')

def main():
    field = minesweeper.Field(100, 50, 500)

    while True:
        x = None
        y = None
        try:
            coords = input("Enter coordinates 'x y':")
            x, y = [int(v) for v in coords.split(' ')]
        except ValueError:
            print('Invalid input')
            continue
        if not 0 <= x < field.width or not 0 <= y < field.height:
            print('Invalid coordinates')
            continue;

        field_state = field.Sweep(x, y)
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
