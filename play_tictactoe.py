import argparse
import random
from tictactoe import *
from mcts import mcts

def get_user_action(state):
    actions = list(map(str, valid_actions(state)))
    player, board, move = state
    prompt = "Player %s, choose an action from one of the numbered cells: " % (player)
    while True:
        action = input(prompt)
        if action in actions: return int(action)
        print("Invalid action, try again.")

def play_against_player(n):
    state = initial_state(n)
    while not game_over(state)[0]:

        print(string_of(state))
        action = get_user_action(state)
        state = perform_action(action, state)
    
    print(string_of(state))
    game_result = game_over(state)[1]
    if game_result == "tied":
        print("Game over, it is tied.")
    else:
        winner = game_result
        print("Game over, player %s wins." % winner)

def play_against_computer(n):

    state = initial_state(n)
    ended = False
    game_result = None
    while not ended:

        player, board, move = state
        print(string_of(state))
        if player == "O":
            action = get_user_action(state)
            state = perform_action(action, state)
            ended, game_result = game_over(state)
        else:
            print("--- AI's turn --->")
            state, ended, game_result = mcts(state)
           
    
    print(string_of(state))
    game_result = game_result
    if game_result == "tied":
        print("Game over, it is tied.")
    else:
        winner = game_result
        print("Game over, player %s wins." % winner)
        print("You beat the computer!" if winner == "O" else "The computer beat you!")


# runs a competitive game between two AIs:
# better_evaluation (as player 0) vs simple_evaluation (as player 1)
def compete(n, verbose=True):
    state = initial_state(n)
    ended = False
    while not ended:

        player, board, move = state
        playeridx = 0 if player == "X" else 1
        if verbose: print(string_of(state))
        if verbose: print("--- %s's turn --->" % ["Better","Baseline"][playeridx])
        if playeridx == 0:
            state, ended, result = mcts(state)
        else:
            state = baseline_ai_turn(state)
            ended, result = game_over(state)
    
    score = 1 if result == "X" else 0 if result == "tied" else -1
    player, board, move = state
    if verbose:
        print(string_of(state))
        print("Final score: %d" % score)
    
    return score

# the baseline AI chooses valid actions uniformly at random
def baseline_ai_turn(state):
    actions = valid_actions(state)
    chosen_action = actions[random.randint(0, len(actions) - 1)]
    return perform_action(chosen_action, state)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Ultimate Tic Tac Toe",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--player", action="store_true", help="play against a human player")
    parser.add_argument("-c", "--computer", action="store_true", help="play against the computer")
    parser.add_argument("-v", "--verbose", action="store_true", help="display each board if running the computer vs. computer simulation")
    parser.add_argument("n-size", help="width (or length) of n by n board, must be at least 3 and no greater than 7")
    args = parser.parse_args()
    config = vars(args)
    n = int(config['n-size'])
    if n < 3 or n > 7:
        print("Invalid n-size. n-size must be at least 3 and no more than 7.")
        exit(1)
    
    if config['player']:
        play_against_player(n)
    elif config['computer']:
        play_against_computer(n)
    else:
        compete(n, config["verbose"])
    
    
    