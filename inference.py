import minesweeper
import random
import tensorflow as tf
import tf_utils

from absl import app, flags
from tensorflow.keras import datasets, layers, models

FLAGS = flags.FLAGS

flags.DEFINE_integer('num_trials', 100,
                     'The number of trials to run.',
                     lower_bound=0)

flags.DEFINE_integer('width', 16,
                     'The width of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('height', 8,
                     'The height of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('num_mines', 30,
                     'The number of mines in the field.',
                     lower_bound=0)

flags.DEFINE_enum('policy', 'random', ['random', 'nn'],
                  'The inference policy to use.')

flags.DEFINE_string('model_directory', None,
                    'Where to read the model from when using the `nn` --policy.')

def select_sweep_cell_random(field: minesweeper.Field) -> (int, int):
    """Select a random covered cell to sweep."""
    covered_cells = []
    for i, row in enumerate(field.proximity):
        for j, value in enumerate(row):
            if field.mask[i][j] == 0:
                covered_cells.append((j, i))
    return covered_cells[random.randrange(0, len(covered_cells) - 1)]

def select_sweep_cell_nn(model: models.Model, field: minesweeper.Field) -> (int, int):
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

    model: models.Model = None
    if model_directory:
        model = models.load_model(model_directory)

    solved_trials = 0
    for i in range(num_trials):
        field = minesweeper.Field(16, 8, 20)

        field_state = minesweeper.FieldState.UNSOLVED
        while field_state == minesweeper.FieldState.UNSOLVED:
            x: int = None
            y: int = None
            if policy == 'random':
                (x, y) = select_sweep_cell_random(field)
            elif policy == 'nn':
                (x, y) = select_sweep_cell_nn(model, field)
            field_state = field.Sweep(x, y)
            print(field)
        if field_state == minesweeper.FieldState.SOLVED:
            solved_trials += 1
        print('Trial', i, 'of', num_trials, field_state)
    print('Solved', solved_trials, 'of', num_trials)

if __name__ == "__main__":
    app.run(main)
