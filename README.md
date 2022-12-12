# Ultimate Tic Tac Toe AI
## CIS667
### Matt Graber

#### Quick start (standard)

The `play_tictactoe` script takes a mandatory argument of the size of the board and a variety of optional arguments controlling its behavior.

To play a 2-player game (human vs. human) on a 3x3 board:

`python3 play_tictactoe.py 3 -p`

To play a 1-player game (human vs. Monte Carlo Tree Search AI) on a 3x3 board:

`python3 play_tictactoe.py 3 -c`

To play a single 0-player game (Monte Carlo Tree Search AI vs. random-choice AI) on a 3x3 board with the board visible:

`python3 play_tictactoe.py 3 -v`

__For Experimenting:__ To play 100 MCTS AI vs random-choice AI games on a visible 3x3 board and record the results to a CSV ending with `outcomes.csv`:

`python3 play_tictactoe.py 3 -v -i 100 -f outcomes.csv`

This will produce a CSV named `3x3_100iterations_outcomes.csv`.
 The CSV is written to after each game, so you can interrupt the exection before completion without losing all the data from the games that were completed.

#### Quick start (neural network)

To generate training data for the neural network on a 4x4 board by playing 100 games of Monte Carlo Tree Search AI vs. random-choice AI and outputting the data to a file ending with `traindata.csv`:

`python3 play_tictactoe.py 4 -g -i 100 -f traindata.csv`

To play a 1-player 4x4 game (human vs. Monte Carlo Tree Search AI with Neural Network) using training data contained in a file called `4x4_NN_examples_traintest.csv` and output the learning curve results to a file ending in `ourresults.csv`:

`python3 play_tictactoe.py 4 -t 4x4_NN_examples_traintest.csv -c -f ourresults.csv`

__For Experimenting:__ To train a neural network using the data in `4x4_NN_examples_traintest.csv` and then play 100 MCTS + Neural Network AI vs random-choice AI games on a visible 4x4 board and record the results to a CSV ending with `outcomes.csv`:

`python3 play_tictactoe.py 4 -v -i 100 -f outcomes.csv -t 4x4_NN_examples_traintest.csv`

#### Full command details
```
usage: play_tictactoe.py [-h] [-p] [-c] [-v] [-i ITERATIONS] [-f FILENAME] [-g] [-t TRAINING_DATA] n-size  

Play Ultimate Tic Tac Toe

positional arguments:
  n-size                width (or length) of n by n board, must be at least 2 and no greater than 7        

optional arguments:
  -h, --help            show this help message and exit
  -p, --player          play against a human player (default: False)
  -c, --computer        play against the computer (default: False)
  -v, --verbose         display each board if running the computer vs. computer simulation (default: False)
  -i ITERATIONS, --iterations ITERATIONS
                        simulate the game for the specified number of times (default: None)
  -f FILENAME, --filename FILENAME
                        save the results of the simulation (or test/training data generation) in the specified filename suffix.
                        Simulation info will be prepended in the filename. (default: None)
  -g, --generate        generate training/test examples using MCTS (default: False)
  -t TRAINING_DATA, --training_data TRAINING_DATA
                        The filename of the CSV containing the training/testing data to be used. The neural network will be used if      
                        this is specified. (default: None)
```

#### Dependencies

- [NumPy](https://numpy.org/)
- [PyTorch](https://pytorch.org/)

#### Existing Code used in this project

Garrett Katz (2021) MCTS.ipynb (Version 1.0) [Source Code]. https://colab.research.google.com/drive/1JuNdI_zcT35MWSY4-h_2ZgH7IBe2TRYd?usp=sharing
Garrett Katz (2022) ProjectExample.ipynb (Version 1.0) [Source Code]. https://colab.research.google.com/drive/1QF8IJHlZ597esIU-vmW7u9KARhyXIjOY?authuser=3
