# Monte Carlo Tree Search
# Adapted from the MCTS implementation used during the CIS667 lecture at
# https://colab.research.google.com/drive/1JuNdI_zcT35MWSY4-h_2ZgH7IBe2TRYd?usp=sharing
# by Prof. Garret Katz

from tictactoe import *
from neural_network_tic_tac_toe import encode
import torch as tr

class Node:
    def __init__(self, state):
        self.state = state
        self.visit_count = 0
        self.score_total = 0
        self.score_estimate = 0
        self.child_list = None
        self.ended = False
        self.result = None
        self.parent = None

    def score_of(self):
        if self.ended:
            if self.result == "X":
                return 1
            elif self.result == "O":
                return -1
        return 0

    def children(self):
        # Only generate children the first time they are requested and memoize
        if self.child_list == None:
            # no children if the game is over
            self.ended, self.result = game_over(self.state)
            children = []
            if not self.ended:
                actions = valid_actions(self.state)
                for i in range(len(actions)):
                    children.append(perform_action(actions[i], self.state))
            self.child_list = list(map(Node, children))
        # Return the memoized child list thereafter
        return self.child_list

    # Helper to collect child visit counts into a list
    def N_values(self):
        return [c.visit_count for c in self.children()]

    # Helper to collect child estimated utilities into a list
    # Utilities are from the current player's perspective
    def Q_values(self):
        children = self.children()
        player = self.state[0]
        # negate utilities for min player "O" 
        sign = +1 if player == "X" else -1

        # empirical average child utilities
        # special case to handle 0 denominator for never-visited children
        #Q = [sign * c.score_total / (c.visit_count+1) for c in children]
        Q = [sign * c.score_total / max(c.visit_count, 1) for c in children]

        return Q

# exploit strategy: choose the best child for the current player
def exploit(node):
    return node.children()[np.argmax(node.Q_values())]

# explore strategy: choose the least-visited child
def explore(node):
    return node.children()[np.argmin(node.N_values())] # TODO: replace with exploration

# upper-confidence bound strategy
def uct(node):
    # max_c Qc + sqrt(ln(Np) / Nc)
    Q = np.array(node.Q_values())
    N = np.array(node.N_values())
    U = Q + np.sqrt(np.log(node.visit_count + 1) / (N + 1)) # +1 for 0 edge case
    return node.children()[np.argmax(U)]

choose_child = uct

# choose a child based on the Neural Net's utility prediction
def choose_child_net(node, net):
    max_util = -100000
    max_child = None
    for child in node.children():
        tens = tr.tensor(list(map(float, encode(child.state))))
        pred_util = net(tens.reshape(-1,tens.shape[0]))
        if pred_util > max_util:
            max_util = pred_util
            max_child = child
    return max_child

"""
def rollout(node):
    # return the node's score if it's a leaf
    if len(node.children()) == 0: result = node.score_of()
    else: result = rollout(choose_child(node))
    node.visit_count += 1
    node.score_total += result
    node.score_estimate = node.score_total / node.visit_count
    return result
"""

def rollout(node, net = None):
    node_count = 0
    # descend
    current_node = node
    while len(current_node.children()) != 0:
        if net is None:
            next_node = choose_child(current_node)
        else:
            next_node = choose_child_net(current_node, net)
        next_node.parent = current_node
        current_node = next_node
    result = current_node.score_of()
    # ascend
    while current_node is not None:
        current_node.visit_count += 1
        current_node.score_total += result
        current_node.score_estimate = current_node.score_total / current_node.visit_count
        # Increment the node_count only if this node hasn't been visited already.
        # From the assignment description: We want to report "number of nodes processed,"
        # not the number of times we processed nodes.
        if current_node.visit_count == 1:
            node_count += 1
        current_node = current_node.parent
    return node_count


# gauge sub-optimality with rollouts
def mcts(state, num_rollouts, net = None):
    node = Node(state)
    nodes_processed = 0
    for r in range(num_rollouts):
        nodes_processed += rollout(node, net)
        #if r % (num_rollouts // 10) == 0: print(r, node.score_estimate)
    # return best child
    children = node.children()
    best_child = children[0]
    for i in range(len(children)):
        if children[i].score_estimate > best_child.score_estimate:
            best_child = children[i]
    return best_child.state, best_child.ended, best_child.result, nodes_processed, best_child.score_total