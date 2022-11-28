import numpy as np

# each index corresponds to each board cell's index
# x (lower case) - player X owns the cell
# o (lower case) - player O owns the cell
# _ - No player owns the cell
# X (capitalized) - player X won that tictactoe sub-board
# O (capitalized) - player O won that tictactoe sub-board
def string_of(state):
    valid_action_lst = valid_actions(state)
    _, board, _ = state
    n = int(len(board) ** 0.25)
    # number of characters in a line of the string representation of the board
    str_line_len = ((4 * n + n - 1) * n + 2 * (n - 1))
    
    board_string = ""
    board_position = 0
    for l in range(n):
        for k in range(n):
            upper_line = ""
            lower_line = ""
            for j in range(n):
                board_position = n**2 * j + k * n + l * n ** 3
                # Handle if someone's won the whole sub-board
                if str(board[board_position]) in ["X", "O"]:
                    winner = board[board_position][0]
                    upper_line += " "
                    lower_line += " "
                    upper_line += "{} ".format(winner) * int((n * 4 + n - 2) / 2)
                    lower_line += " {}".format(winner) * int((n * 4 + n - 2) / 2)
                    if n % 2 == 1:
                        upper_line += " "
                        lower_line += " "
                else:
                    for i in range(n):
                        board_position = i + n**2 * j + k * n + l * n**3
                        if board_position in valid_action_lst:
                            upper_line += "{:<4}".format(board_position)
                        else:
                            upper_line += "    "
                        if board[board_position] != "_":
                            lower_line += "({}) ".format(board[board_position])
                        else:
                            lower_line += "    "
                        if i < n - 1:
                            upper_line += "|"
                            lower_line += "|"
                if j < n - 1:
                    upper_line += "//"
                    lower_line += "//"
                else:
                    upper_line += "\n"
                    lower_line += "\n"
            board_string += upper_line
            board_string += lower_line
            if k < n - 1:
                for j in range(n):
                    board_position = n**2 * j + k * n + l * n**3
                    if str(board[board_position]) in ["X", "O"]:
                        winner = board[board_position][0]
                        board_string += "  "
                        board_string += "{} ".format(winner) * int((n * 4 + n - 2) / 2 - 1)
                        board_string += "  " if n % 2 == 1 else " "
                    else:
                        for i in range(n):
                            board_string += "----"
                            if i < n - 1:
                                board_string += "|"
                    if j < n - 1:
                        board_string += "//"
                    else:
                        board_string += "\n"
        if l < n - 1:
            board_string += "/" * str_line_len
            board_string += "\n"
    return board_string

# Return the first index of the sub-board that contains the specified index
def get_subboard_from_index(idx, n):
    return (idx // (n**2)) * (n ** 2)

# Mark a sub-board as having been won by a player
def win_subboard(board, subidx, player):
    n = int(len(board) ** 0.25)
    board[subidx:subidx + n**2] = player.capitalize()
    return board

# check if the specified indices all contain the same thing
def check_line_for_win(board, indices, big_win = False):
    if not big_win:
        return np.all(board[indices] == "x") or np.all(board[indices] == "o")
    else:
        return np.all(board[indices] == "X") or np.all(board[indices] == "O")

# used to determine if there's a tie
# if all lines are unwinnable then there must be a tie
def check_if_line_unwinnable(state, indices, small = False):
    player, board, _ = state
    # if we see both X and O in the line then it's unwinnable
    if small:
        return "o" in board[indices] and "x" in board[indices]
    else:
        if "O" in board[indices] and "X" in board[indices]:
            return True
        for i in range(len(indices)):
            if check_for_small_winner((player, board, indices[i]))[1] == "tied":
                return True
    return False

# check if anyone has won a small board
# move = cell_idx
def check_for_small_winner(state):
    player, board, move = state
    n = int(len(board) ** 0.25)
    # get first index of cell in sub-board
    subidx = get_subboard_from_index(move, n)
    idx_lists_to_check = []
    # diagonal checks
    diag1_lst = np.zeros(n, dtype=int)
    diag2_lst = np.zeros(n, dtype=int)
    """for i in range(n):
        # horizontal and vertical checks
        hor_lst = np.zeros(n, dtype=int)
        vert_lst = np.zeros(n, dtype=int)
        for j in range(n):
            hor_lst[j] = subidx + n * i + j
            vert_lst[j] = subidx + n * j + i
        idx_lists_to_check.append(hor_lst)
        idx_lists_to_check.append(vert_lst)
        # diagonal checks
        diag1_lst[i] = subidx + n * i + i
        diag2_lst[i] = subidx + n * (n - (i + 1)) + i
    idx_lists_to_check.append(diag1_lst)
    idx_lists_to_check.append(diag2_lst)"""
    i = np.arange(n).reshape(n,1)
    j = i.T
    hor_lsts = subidx + n * i + j
    vert_lsts = subidx + n * j + i
    diag1_lst = subidx + n * j + j # j, not i, to keep it as a row vector
    diag2_lst = subidx + n * (n - (j + 1)) + j
    itlv = np.concatenate((hor_lsts, vert_lsts), axis=1).reshape(-1, n)
    idx_lists_to_check = list(np.concatenate((itlv, diag1_lst, diag2_lst), axis=0))
    
    # check each potential win
    unwinnables = 0
    for line in idx_lists_to_check:
        if check_line_for_win(board, line):
            # update the board to reflect the win
            board = win_subboard(board, subidx, board[move])
            return (player, board, move), ("x" if player == "o" else "o")
        elif check_if_line_unwinnable(state, line, small=True):
            unwinnables += 1
    if unwinnables == len(idx_lists_to_check):
        return (player, board, move), "tied"
    return (player, board, move), None

# check if anyone has won the entire board or if there is a tie
def game_over(state):
    if state[2] is not None:
        (player, board, _), _ = check_for_small_winner(state)
    else:
        player, board, _ = state 
    n = int(len(board) ** 0.25)
    idx_lists_to_check = []
    diag1_lst = np.zeros(n, dtype=int)
    diag2_lst = np.zeros(n, dtype=int)
    for i in range(n):
        # horizontal and vertical
        hor_lst = np.zeros(n, dtype=int)
        vert_lst = np.zeros(n, dtype=int)
        for j in range(n):
            hor_lst[j] = i * n**3 + j * n**2
            vert_lst[j] = j * n**3 + i * n**2
        idx_lists_to_check.append(hor_lst)
        idx_lists_to_check.append(vert_lst)
        # diagonal
        diag1_lst[i] = n**3 * i + n**2 * i
        diag2_lst[i] = n**3 * (n - (i + 1)) + n**2 * i
    idx_lists_to_check.append(diag1_lst)
    idx_lists_to_check.append(diag2_lst)
    # check each potential win
    unwinnables = 0
    for line in idx_lists_to_check:
        if check_line_for_win(board, line, big_win=True):
            return True, ("x" if player == "o" else "o")
        elif check_if_line_unwinnable(state, line):
            unwinnables += 1
    # tied
    if unwinnables == len(idx_lists_to_check):
        return True, "tied"
    return False, None

# Returns all cells that haven't been claimed in the range
def get_open_cells(board, range):
    return np.argwhere(board[range[0]:range[1]] == "_").flatten() + range[0]

# Returns a list of the valid indices that the player can play
def valid_actions(state):
    _, board, move = state
    n = int(len(board) ** 0.25)
    # if it's the first move return whole board
    if move is None:
        return get_open_cells(board, (0,len(board)))
    subidx = get_subboard_from_index(move, n)
    new_subidx = n**2 * (move - subidx)
    # if the previous player chose a cell that would direct
    # the other player to a subboard that's already
    # been won or there are no available cells,
    # then they get to pick any cell
    if str(board[new_subidx]) in ["X", "O"] or "_" not in board[new_subidx:new_subidx + n**2]:
        return get_open_cells(board, (0,len(board)))
    # Otherwise it'll be the open cells in the corresponding
    # sub-board
    return get_open_cells(board, (new_subidx, new_subidx + n**2))

# How the game starts
def initial_state(n):
    player = "x"
    board = np.full(n**4, "_")
    move = None
    return (player, board, move)

# performs the given action
def perform_action(action, state):
    player, board, move = state
    board = board.copy()
    board[action] = player
    move = action
    player = "x" if player == "o" else "o"
    return (player, board, move)


"""
n = 3
test_board = [0] * n**4
for i in range(51,54):
    test_board[i] = "O"
(_,test_board,_), winner = check_for_small_winner(("O",test_board, 53))
print(winner)
for i in range(39,42):
    test_board[i] = "O"
(_,test_board,_), winner = check_for_small_winner(("O",test_board, 41))
print(winner)
for i in range(33,36):
    test_board[i] = "X"
(_,test_board,_), winner = check_for_small_winner(("X",test_board, 35))
print(winner)
for i in range(63,72):
    test_board[i] = "X"
(_,test_board,_), winner = check_for_small_winner(("X",test_board, 71))
print(winner)
for i in range(18,27):
    test_board[i] = "X"
(_,test_board,_), winner = check_for_small_winner(("X",test_board, 26))
print(winner)
for i in range(0,9):
    test_board[i] = "O"
(_,test_board,_), winner = check_for_small_winner(("O",test_board, 8))
print(winner)
for i in range(54,63):
    test_board[i] = "O"
(_,test_board,_), winner = check_for_small_winner(("X",test_board, 62))
for i in range(72,81):
    test_board[i] = "O"
(_,test_board,_), winner = check_for_small_winner(("O",test_board, 62))
print(winner)
test_board[12] = "O"
test_board[13] = "X"
test_board[14] = "O"
test_board[9] = "X"
test_board[17] = "O"
test_board[11] = "X"
test_board[15] = "O"
test_board[16] = "X"
test_board[10] = "O"
state = ("O", test_board, 1)

print(game_over(state))
print(valid_actions(state))
print(string_of(state))
"""