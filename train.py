import matplotlib.pyplot as plt
import minesweeper
import numpy as np
import tensorflow as tf
import tf_utils

from absl import app, flags
from tensorflow.keras import layers, losses, models

FLAGS = flags.FLAGS

flags.DEFINE_integer('width', 16,
                     'The width of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('height', 8,
                     'The height of the Minesweeper field.',
                     lower_bound=0)
flags.DEFINE_integer('num_mines', 30,
                     'The number of mines in the field.',
                     lower_bound=0)

flags.DEFINE_string('output_directory', None,
                    'Where to write the output model.')

def create_random_field(width: int,
                        height: int,
                        num_mines: int) -> minesweeper.Field:
    """Create a random field with an area revealed."""
    field = minesweeper.Field(width, height, num_mines)

    # Sweep the first empty cell we find.
    # TODO: Selecting the first one will bias the results.
    for i, row in enumerate(field.proximity):
        for j, value in enumerate(row):
            if value == 0:
                field.Sweep(j, i)
    return field

def create_probability_tensor(field: minesweeper.Field) -> tf.Tensor:
    """Returns a tensor containing probabilities of `field` containing mines."""
    tensor = np.zeros((field.height, field.width), np.float32)

    for i, row in enumerate(field.proximity):
        for j, value in enumerate(row):
            if value == -1:
                tensor[i][j] = 1.0

    tensor = tensor.reshape(field.height, field.width, 1)
    return tf.convert_to_tensor(tensor, dtype=tf.float32)

def create_examples(width: int,
                    height: int,
                    num_mines: int,
                    num_examples: int) -> (tf.Tensor, tf.Tensor):
    """Returns a Tensorflow dataset containing `num_examples`.

    Returns:
      A (input, output) tuple.
    """
    input_tensors = []
    output_tensors = []
    for _ in range(num_examples):
        field = create_random_field(width, height, num_mines)

        input_tensors.append(tf_utils.create_input_tensor(field))
        output_tensors.append(create_probability_tensor(field))
    return (tf.stack(input_tensors, axis=0), tf.stack(output_tensors, axis=0))

def main(argv):
    width = FLAGS.width
    height = FLAGS.height
    num_mines = FLAGS.num_mines
    output_directory = FLAGS.output_directory

    (train_inputs, train_outputs) = create_examples(width, height, num_mines, 1000)
    (test_inputs, test_outputs) = create_examples(width, height, num_mines, 100)

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3),
                            activation='relu',
                            input_shape=(height, width, 1),
                            padding='same'))
    # TODO: Add more complexity.
    model.add(layers.Conv2DTranspose(32, (3, 3), strides=(1, 1), padding='same'))
    model.add(layers.Conv2D(1, 1, padding='same'))

    model.summary()

    model.compile(optimizer='adam',
                  loss=losses.MeanAbsoluteError(),
                  metrics=['accuracy'])

    history = model.fit(train_inputs, train_outputs, epochs=10,
                        validation_data=(test_inputs, test_outputs))

    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc='lower right')
    plt.show()

    _, test_acc = model.evaluate(test_inputs,  test_outputs, verbose=2)

    print('Accuracy', test_acc)

    if output_directory:
        model.save(output_directory)

if __name__ == "__main__":
    app.run(main)
