# Ultimate Tic Tac Toe AI
## CIS667
### Matt Graber

#### Quick start
To play a 2-player game (human vs. human) on a 3x3 board:

`python3 play_tictactoe.py 3 -p`

To play a 1-player game (human vs. Monte Carlo Tree Search AI) on a 3x3 board:

`python3 play_tictactoe.py 3 -c`

To play a 0-player game (Monte Carlo Tree Search AI vs. random-choice AI) on a 3x3 board with the board visible:

`python3 play_tictactoe.py 3 -v`

#### Full details
```
usage: play_tictactoe.py [-h] [-p] [-c] [-v] n-size

Play Ultimate Tic Tac Toe

positional arguments:
  n-size          width (or length) of n by n board, must be at least 3 and no greater than 7

optional arguments:
  -h, --help      show this help message and exit
  -p, --player    play against a human player (default: False)
  -c, --computer  play against the computer (default: False)
  -v, --verbose   display each board if running the computer vs. computer simulation (default: False)
```

#### Dependencies

- [NumPy](https://numpy.org/)
