import minesweeper
import numpy as np
import tensorflow as tf
import tf_utils

from tensorflow.keras import datasets, layers, models

def select_sweep_cell(model: models.Model, field: minesweeper.Field) -> (int, int):
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
