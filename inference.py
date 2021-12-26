import minesweeper
import random
import tensorflow as tf
import termcolor
import tf_utils

from absl import app, flags
from tensorflow.keras import models

FLAGS = flags.FLAGS

flags.DEFINE_integer('num_trials', 100,
                     'The number of trials to run.',
                     lower_bound=0)

flags.DEFINE_integer('width', 32,
                     'The width of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('height', 16,
                     'The height of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('num_mines', 99,
                     'The number of mines in the field.',
                     lower_bound=0)

flags.DEFINE_enum('policy', 'random', ['random', 'nn'],
                  'The inference policy to use.')

flags.DEFINE_string('model_directory', None,
                    'Where to read the model from when using the `nn` --policy.')

def select_sweep_cell_random(field: minesweeper.Field) -> (int, int):
    """Select a random covered cell to sweep."""
    candidate_cells = []
    for i, row in enumerate(field.mask):
        for j, value in enumerate(row):
            if value == 0:
                candidate_cells.append((j, i))
    return candidate_cells[random.randrange(0, len(candidate_cells))]

def select_sweep_cell_nn(model: models.Model,
                         field: minesweeper.Field) -> (int, int):
    """Select a cell to sweep using a nn."""
    input_tensor = tf.stack([tf_utils.create_input_tensor(field)], axis=0)
    probabilities = model.predict(input_tensor)

    # Select the covered cell with the lowest probability.
    x: int = None
    y: int = None
    min_value: float = float('inf')
    for i, row in enumerate(probabilities[0]):
        for j, value in enumerate(row):
            if field.mask[i][j] == 0 and value[0] < min_value:
                min_value = value[0]
                x = j
                y = i
    return (x, y)

def main(argv):
    num_trials = FLAGS.num_trials
    width = FLAGS.width
    height = FLAGS.height
    num_mines = FLAGS.num_mines
    policy = FLAGS.policy
    model_directory = FLAGS.model_directory

    if policy == 'nn':
        assert model_directory, "--model_directory must be specified for 'nn' policy"

    model: models.Model = None
    if model_directory:
        model = models.load_model(model_directory)

    solved_trials = 0
    for trial in range(num_trials):
        field = minesweeper.Field(width, height, num_mines)

        # Start by sweeping a random sage cell to exclude bad
        # guesses at the start, since there's nothing to infer.
        (x, y) = field.RandomSafeCell()
        field.Sweep(x, y)

        while not field.IsCompleted():
            x: int = None
            y: int = None
            if policy == 'random':
                (x, y) = select_sweep_cell_random(field)
            elif policy == 'nn':
                (x, y) = select_sweep_cell_nn(model, field)
            field.Sweep(x, y)
            field.pretty_print()
            print('')
        if field.state == minesweeper.FieldState.SOLVED:
            solved_trials += 1
        termination_state_color = 'red' if field.state == minesweeper.FieldState.FAILED else 'green'
        print('Trial', trial + 1, 'of', num_trials, termcolor.colored(field.state, termination_state_color))
    print('Solved', solved_trials, 'of', num_trials)

if __name__ == "__main__":
    app.run(main)
