import numpy as np

# each index corresponds to each board cell's index
# X - player X owns the cell
# O - player O owns the cell
# 0 - No player owns the cell
# Xwin - player X won that tictactoe sub-board
# Owin - player O won that tictactoe sub-board
# Xtie - the sub-board is tied but this cell contains X
# Otie - the sub-board is tied but this cell contains O
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
                if "win" in str(board[board_position]):
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
                        if board[board_position] != 0:
                            lower_line += "({}) ".format(board[board_position][0])
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
                    if "win" in str(board[board_position]):
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
def complete_subboard(board, subidx, player, result):
    n = int(len(board) ** 0.25)
    for i in range(subidx, subidx + n**2):
        # result will be either "win" or "tie"
        if result == "tie":
            board[i] = "{}{}".format(board[i], result)
        else:
            board[i] = "{}{}".format(player, result)
    return board

# check if the specified indices all contain the same thing
def check_line_for_win(board, indices, big_win = False):
    for i in range(len(indices)):
        if (board[indices[i]] == 0 or
            ("win" in str(board[indices[i]]) and not big_win) or
            ("win" not in str(board[indices[i]]) and big_win) or
            board[indices[i]] != board[indices[0]]):
            return False
    return True

# used to determine if there's a tie
# if all lines are unwinnable then there must be a tie
def check_if_line_unwinnable(state, indices, small = False):
    _, board, _ = state
    seenX = 0
    seenO = 0
    # if we see both X and O in the line then it's unwinnable
    if small:
        for i in range(len(indices)):
            if "X" in str(board[indices[i]]):
                seenX = 1
            elif "O" in str(board[indices[i]]):
                seenO = 1
    else:
        for i in range(len(indices)):
            if "Xwin" in str(board[indices[i]]):
                seenX = 1
            elif "Owin" in str(board[indices[i]]):
                seenO = 1
            elif "tie" in str(board[indices[i]]):
                return True
    return seenX + seenO > 1

# check if anyone has won a small board
# move = cell_idx
def check_for_small_winner(state):
    player, board, move = state
    n = int(len(board) ** 0.25)
    # get first index of cell in sub-board
    subidx = get_subboard_from_index(move, n)
    idx_lists_to_check = []
    # diagonal checks
    diag1_lst = []
    diag2_lst = []
    for i in range(n):
        # horizontal and vertical checks
        hor_lst = []
        vert_lst = []
        for j in range(n):
            hor_lst.append(subidx + n * i + j)
            vert_lst.append(subidx + n * j + i)
        idx_lists_to_check.append(hor_lst)
        idx_lists_to_check.append(vert_lst)
        # diagonal checks
        diag1_lst.append(subidx + n * i + i)
        diag2_lst.append(subidx + n * (n - (i + 1)) + i)
    idx_lists_to_check.append(diag1_lst)
    idx_lists_to_check.append(diag2_lst)
    # check each potential win
    unwinnables = 0
    for line in idx_lists_to_check:
        if check_line_for_win(board, line):
            # update the board to reflect the win
            board = complete_subboard(board, subidx, board[move], "win")
            return (player, board, move), ("X" if player == "O" else "O")
        elif check_if_line_unwinnable(state, line, small=True):
            unwinnables += 1
    if unwinnables == len(idx_lists_to_check):
        board = complete_subboard(board, subidx, board[move], "tie")
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
    diag1_lst = []
    diag2_lst = []
    for i in range(n):
        # horizontal and vertical
        hor_lst = []
        vert_lst = []
        for j in range(n):
            hor_lst.append(i * n**3 + j * n**2)
            vert_lst.append(j * n**3 + i * n**2)
        idx_lists_to_check.append(hor_lst)
        idx_lists_to_check.append(vert_lst)
        # diagonal
        diag1_lst.append(n**3 * i + n**2 * i)
        diag2_lst.append(n**3 * (n - (i + 1)) + n**2 * i)
    idx_lists_to_check.append(diag1_lst)
    idx_lists_to_check.append(diag2_lst)
    # check each potential win
    unwinnables = 0
    for line in idx_lists_to_check:
        if check_line_for_win(board, line, big_win=True):
            return True, ("X" if player == "O" else "O")
        elif check_if_line_unwinnable(state, line):
            unwinnables += 1
    # tied
    if unwinnables == len(idx_lists_to_check):
        return True, "tied"
    return False, None

# Returns all cells that haven't been claimed in the range
def get_open_cells(board, range):
    idx_lst = []
    for i in range:
        if board[i] == 0:
            idx_lst.append(i)
    return idx_lst

# Returns a list of the valid indices that the player can play
def valid_actions(state):
    _, board, move = state
    n = int(len(board) ** 0.25)
    # if it's the first move return whole board
    if move is None:
        return get_open_cells(board, range(len(board)))
    subidx = get_subboard_from_index(move, n)
    new_subidx = n**2 * (move - subidx)
    # if the previous player chose a cell that would direct
    # the other player to a subboard that's already
    # been won or there are no available cells,
    # then they get to pick any cell
    if "win" in str(board[new_subidx]) or "tie" in str(board[new_subidx]):
        return get_open_cells(board, range(len(board)))
    # Otherwise it'll be the open cells in the corresponding
    # sub-board
    return get_open_cells(board, range(new_subidx, new_subidx + n**2))

# How the game starts
def initial_state(n):
    player = "X"
    board = [0] * n**4
    move = None
    return (player, board, move)

# performs the given action
def perform_action(action, state):
    player, board, move = state
    board = board.copy()
    board[action] = player
    move = action
    player = "X" if player == "O" else "O"
    return (player, board, move)
