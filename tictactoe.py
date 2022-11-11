import numpy as np

# each index corresponds to each board cell's index
# X - player X owns the cell
# O - player O owns the cell
# 0 - No player owns the cell
# Xwin - player X won that tictactoe sub-board
# Owin - player O won that tictactoe sub-board
def string_of(board):
    # dimension of individual tic tac toe board
    n = int(len(board) ** 0.25)
    # number of cells in an individual tic-tac-toe board
    sub_board_size = n ** 2
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
                        upper_line += "{:<4}".format(board_position)
                        if board[board_position] != 0:
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
                    board_position = i + n**2 * j + k * n + l * n**3
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
def get_subboard_from_index(idx):
    subidx = 0
    while (n ** 2) * (subidx + 1) <= idx:
        subidx += 1
    return subidx * n**2

# Mark a sub-board as having been won by a player
def win_subboard(board, subidx, player):
    print(subidx)
    for i in range(subidx, subidx + n**2):
        board[i] = "{}win".format(player)
    return board

# check if the specified indices all contain the same thing
def check_subboard_line(board, indices):
    for i in range(len(indices)):
        if board[indices[i]] != board[indices[0]]:
            return False
    return True

# check if anyone has won a small board
# move = cell_idx
def check_for_small_winner(board, move):
    # get first index of cell in sub-board
    subidx = get_subboard_from_index(move)
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
    for line in idx_lists_to_check:
        if check_subboard_line(board, line):
            # update the board to reflect the win
            board = win_subboard(board, subidx, board[move])
            return True, board
    return False, board

# check if anyone has won the entire board
def check_for_big_winner(board):
    # TODO
    return None

n = 3
test_board = [0] * n**4
for i in range(51,54):
    test_board[i] = "O"
_, test_board = check_for_small_winner(test_board, 53)

print(string_of(test_board))
