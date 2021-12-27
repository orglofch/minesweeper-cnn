# Minesweeper-CNN

Created a simple CNN to learn Tensorflow (and a bit of Python on the side).

The CNN takes a partial Minesweeper field as input and predicts the locations of the mines. The CNN based solver then takes this prediction and sweeps the cell with the lowest probability. All input and output is through the consolve (i.e. there's no GUI).

![example_field](https://github.com/orglofch/minesweeper-cnn/blob/main/example_field.png)

# Performance:

- Expert (32 x 16, 99 mines) - solves ~70%
- Intermediate level (16 x 8, 30 mines) - solves ~95%

# Training

Trains a new model.

```
python3 train.py --output_directory=/tmp/model
```

# Evaluation

Evaluates a model, running it through complete Minesweeper problems, counting how many the model finishes without hitting mines.

```
python3 inference.py --policy=nn --model_directory=/tmp/model
```

For comparison, if you want to compare against the performance of just selecting random cells, you can run:

```
python3 inference.py --policy=random
```

The performance will not be good.

# CLI

Supports janky interactive Minesweeper through the command-line.

```
python3 cli.py
```
