import minesweeper
import numpy as np
import tensorflow as tf

def create_input_tensor(field: minesweeper.Field) -> tf.Tensor:
    """Returns a tensor representing the visible `field` state.

    The tensor is equivalent to `field.proximity` except mines are
    replaced with the value 9, and masked cells are replaced by 10.

    The tensor is encoded as a one-hot tensor to prevent the network
    from inferring information from the numeric values. If the network
    is allowed to do this, it tends to simply learn to avoid large
    numbers.
    """
    tensor = np.copy(field.proximity)

    for i, row in enumerate(tensor):
        for j, value in enumerate(row):
            if field.mask[i][j] == 0:
                tensor[i][j] = 10
            elif value == -1:
                tensor[i][j] = 9

    tensor = tensor.reshape(field.height, field.width, 1)
    return tf.one_hot(tf.convert_to_tensor(tensor, dtype=tf.uint8), 11, axis=2)
