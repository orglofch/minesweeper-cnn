import matplotlib.pyplot as plt
import minesweeper
import numpy as np
import random
import tensorflow as tf
import tf_utils

from absl import app, flags
from tensorflow.keras import layers, losses, models

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

flags.DEFINE_string('output_directory', None,
                    'Where to write the output model.')

def create_random_field(width: int,
                        height: int,
                        num_mines: int) -> minesweeper.Field:
    """Create a random field with some areas revealed."""
    field = minesweeper.Field(width, height, num_mines)

    # Sweep a random number of safe cells.
    num_sweeps = random.randrange(5, 25)
    for _ in range(num_sweeps):
        (x, y) = field.RandomSafeCell()
        field.Sweep(x, y)
        if field.IsCompleted():
            break
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

    (train_inputs, train_outputs) = create_examples(width, height, num_mines, 5096)
    (test_inputs, test_outputs) = create_examples(width, height, num_mines, 512)

    input = layers.Input(shape=(height, width, 11))
    model = layers.Conv2D(64, (5, 5),
                          activation='relu',
                          padding='same')(input)
    model = layers.Conv2D(64, (5, 5),
                          activation='relu',
                          padding='same')(model)
    model = layers.BatchNormalization()(model)
    model = layers.Dropout(0.5)(model)
    output = layers.Conv2D(1, 1, padding='same')(model)

    model = models.Model(inputs=input, outputs=output)

    model.summary()

    model.compile(optimizer='adam',
                  loss=losses.MeanSquaredError(),
                  metrics=['accuracy'])

    history = model.fit(train_inputs, train_outputs, epochs=100,
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
