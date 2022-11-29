import argparse
import random
from tictactoe import *
from mcts import mcts
import csv

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

def play_against_computer(n, num_rollouts):

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
            state, ended, game_result, _ = mcts(state, num_rollouts)
           
    
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
def compete(n, num_rollouts, verbose=True):
    state = initial_state(n)
    ended = False
    total_nodes = 0
    while not ended:

        player, board, move = state
        playeridx = 0 if player == "X" else 1
        if verbose: print(string_of(state))
        if verbose: print("--- %s's turn --->" % ["Better","Baseline"][playeridx])
        if playeridx == 0:
            state, ended, result, nodes_processed = mcts(state, num_rollouts)
            total_nodes += nodes_processed
        else:
            state = baseline_ai_turn(state)
            ended, result = game_over(state)
    
    score = 1 if result == "X" else 0 if result == "tied" else -1
    player, board, move = state
    if verbose:
        print(string_of(state))
        print("Final score: %d" % score)
    
    return score, total_nodes

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
    parser.add_argument("-i", "--iterations", help="simulate the game for the specified number of times")
    parser.add_argument("-f", "--filename", help="save the results of the simulation in the specified filename suffix. Simulation info will be prepended in the filename.")
    parser.add_argument("n-size", help="width (or length) of n by n board, must be at least 3 and no greater than 7")
    args = parser.parse_args()
    config = vars(args)
    n = int(config['n-size'])
    if n < 3 or n > 7:
        print("Invalid n-size. n-size must be at least 3 and no more than 7.")
        exit(1)
    
    # To keep the max time MCTS takes to decide each action beneath 30 seconds,
    # assign the number of rollouts based on the size of the board
    rollout_mappings = {3: 3500, 4: 350, 5: 35, 6: 3, 7: 1}

    iter = 1
    if config['iterations'] is not None:
        iter = int(config['iterations'])
        if iter < 1:
            print("Invalid number of iterations. Must be greater than 0.")
            exit(1)

    if config['player']:
        play_against_player(n)
    elif config['computer']:
        play_against_computer(n, rollout_mappings[n])
    else:
        if config['filename'] is not None:
            filename = str(n) + "x" + str(n) + "_" + str(rollout_mappings[n]) + "iterations" + "_" + config['filename']
            with open(filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',')
                csvwriter.writerow(["Iteration", "Score", "Nodes Processed"])
                for i in range(iter):
                    print("Iteration", str(i) + ":")
                    score, total_nodes = compete(n, rollout_mappings[n], config["verbose"])
                    csvwriter.writerow([i, score, total_nodes])
                    # flush so that this can be interrupted if needed without losing progress
                    csvfile.flush()
        else:
            for i in range(iter):
                print("Game #", str(i + 1), "of", iter)
                score, total_nodes = compete(n, rollout_mappings[n], config["verbose"])

    