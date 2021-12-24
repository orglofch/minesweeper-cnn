import minesweeper
import numpy as np
import tensorflow as tf

def create_input_tensor(field: minesweeper.Field) -> tf.Tensor:
    """Returns a tensor representing the visible `field` state.

    The tensor is equivalent to `field.proximity` except masked cells
    are replaced with -2.
    """
    tensor = np.copy(field.proximity)

    for i, row in enumerate(tensor):
        for j, value in enumerate(row):
            if field.mask[i][j] == 0:
                tensor[i][j] = -2

    tensor = tensor.reshape(field.height, field.width, 1)
    return tf.convert_to_tensor(tensor, dtype=tf.int8)
