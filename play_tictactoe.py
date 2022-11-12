from tictactoe import *

def get_user_action(state):
    actions = list(map(str, valid_actions(state)))
    player, board, move = state
    prompt = "Player %d, choose an action (%s): " % (player, ",".join(actions))
    while True:
        action = input(prompt)
        if action in actions: return int(action)
        print("Invalid action, try again.")

if __name__ == "__main__":

    max_depth = 1
    state = initial_state()
    while not game_over(state)[0]:

        player, board, move = state
        print(string_of(state))
        if player == "O":
            action = get_user_action(state)
            state = perform_action(action, state)
        else:
            print("--- AI's turn --->")
            state, _ = mcts6(state, max_depth, simple_evaluate)
    
    state
    print(string_of(state))
    game_result = game_over(state)[1]
    if game_result == "tied":
        print("Game over, it is tied.")
    else:
        winner = game_result
        print("Game over, player %d wins." % winner)