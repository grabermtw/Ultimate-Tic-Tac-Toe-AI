import numpy as np


class TicTacToe:

    def __init__(self, n, state = None):
        self.tied = []
        self.board = None
        if state is not None:
            self.board = state[0]
        

    # each index corresponds to each board cell's index
    # X - player X owns the cell
    # O - player O owns the cell
    # 0 - No player owns the cell
    # Xwin - player X won that tictactoe sub-board
    # Owin - player O won that tictactoe sub-board
    def string_of(self, state):
        valid_action_lst = self.valid_actions(state)
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
        subidx = 0
        while (n ** 2) * (subidx + 1) <= idx:
            subidx += 1
        return subidx * n**2

    # Mark a sub-board as having been won by a player
    def win_subboard(board, subidx, player):
        n = int(len(board) ** 0.25)
        """
        for i in range(subidx, subidx + n**2):
            board[i] = "{}win".format(player)
        """
        board[subidx:subidx + n**2] = player.capitalize()
        return board

    # check if the specified indices all contain the same thing
    def check_line_for_win(board, indices, big_win = False):
        """
        for i in range(len(indices)):
            if (board[indices[i]] == 0 or
                ("win" in str(board[indices[i]]) and not big_win) or
                ("win" not in str(board[indices[i]]) and big_win) or
                board[indices[i]] != board[indices[0]]):
                return False
        return True
        """
        if not big_win:
            return np.all(board[indices] == "x") or np.all(board[indices] == "o")
        else:
            return np.all(board[indices] == "X") or np.all(board[indices] == "O")



    # used to determine if there's a tie
    # if all lines are unwinnable then there must be a tie
    def check_if_line_unwinnable(self, state, indices, small = False):
        player, board, _ = state
        # if we see both X and O in the line then it's unwinnable
        if small:
            return "o" in board[indices] and "x" in board[indices]
        else:
            if "O" in board[indices] and "X" in board[indices]:
                return True
            for i in range(len(indices)):
                if self.check_for_small_winner((player, board, indices[i]))[1] == "tied":
                    return True
        return False

    # check if anyone has won a small board
    # move = cell_idx
    def check_for_small_winner(self, state):
        player, board, move = state
        n = int(len(board) ** 0.25)
        # get first index of cell in sub-board
        subidx = self.get_subboard_from_index(move, n)
        idx_lists_to_check = []
        # diagonal checks
        diag1_lst = np.zeros(n, dtype=int)
        diag2_lst = np.zeros(n, dtype=int)
        for i in range(n):
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
        idx_lists_to_check.append(diag2_lst)
        # check each potential win
        unwinnables = 0
        for line in idx_lists_to_check:
            if self.check_line_for_win(board, line):
                # update the board to reflect the win
                board = self.win_subboard(board, subidx, board[move])
                return (player, board, move), ("x" if player == "o" else "o")
            elif self.check_if_line_unwinnable(state, line, small=True):
                unwinnables += 1
        if unwinnables == len(idx_lists_to_check):
            return (player, board, move), "tied"
        return (player, board, move), None

    # check if anyone has won the entire board or if there is a tie
    def game_over(self, state):
        if state[2] is not None:
            (player, board, _), _ = self.check_for_small_winner(state)
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
            if self.check_line_for_win(board, line, big_win=True):
                return True, ("x" if player == "o" else "o")
            elif self.check_if_line_unwinnable(state, line):
                unwinnables += 1
        # tied
        if unwinnables == len(idx_lists_to_check):
            return True, "tied"
        return False, None

    # Returns all cells that haven't been claimed in the range
    def get_open_cells(board, range):
        """
        idx_lst = []
        for i in range:
            if board[i] == 0:
                idx_lst.append(i)
        return idx_lst
        """
        return np.argwhere(board[range[0]:range[1]] == "_").flatten() + range[0]

    # Returns a list of the valid indices that the player can play
    def valid_actions(self, state):
        _, board, move = state
        n = int(len(board) ** 0.25)
        # if it's the first move return whole board
        if move is None:
            return self.get_open_cells(board, (0,len(board)))
        subidx = self.get_subboard_from_index(move, n)
        new_subidx = n**2 * (move - subidx)
        # if the previous player chose a cell that would direct
        # the other player to a subboard that's already
        # been won or there are no available cells,
        # then they get to pick any cell
        if str(board[new_subidx]) in ["X", "O"] or "_" not in board[new_subidx:new_subidx + n**2]:
            return self.get_open_cells(board, (0,len(board)))
        # Otherwise it'll be the open cells in the corresponding
        # sub-board
        return self.get_open_cells(board, (new_subidx, new_subidx + n**2))

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

    # return a list of all the children of a state
    def children_of(self, state):
        # no children if the game is over
        if self.game_over(state)[0]:
            return []
        actions = self.valid_actions(state)
        children = []
        for i in range(len(actions)):
            children.append(self.perform_action(actions[i], state))
        return children

    # return the "score" of a state.
    # A win for X is 1, a win for O is -1,
    # and a tie is 0
    def score_of(self, state):
        ended, result = self.game_over(state)
        if ended:
            if result == "x":
                return 1
            elif result == "o":
                return -1
        return 0

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