import sys, argparse
from tictactoe import *

def get_user_action(state):
    actions = list(map(str, valid_actions(state)))
    player, board, move = state
    prompt = "Player %s, choose an action (%s): " % (player, ",".join(actions))
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
        print("Game over, player %d wins." % winner)

def play_against_computer(n):
    max_depth = 1
    state = initial_state(n)
    while not game_over(state)[0]:

        player, board, move = state
        print(string_of(state))
        if player == "O":
            action = get_user_action(state)
            state = perform_action(action, state)
        else:
            print("--- AI's turn --->")
           # state, _ = mcts(state, max_depth, simple_evaluate)
    
    state
    print(string_of(state))
    game_result = game_over(state)[1]
    if game_result == "tied":
        print("Game over, it is tied.")
    else:
        winner = game_result
        print("Game over, player %d wins." % winner)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Ultimate Tic Tac Toe",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--player", action="store_true", help="play against a human player instead of the computer")
    parser.add_argument("n-size", help="width (or length) of n by n board, must be at least 3")
    args = parser.parse_args()
    config = vars(args)
    n = int(config['n-size'])
    if n < 3:
        print("Invalid n-size. n-size must be at least 3")

    if config['player']:
        play_against_player(n)
    else:
        play_against_computer(n)
    
    
    