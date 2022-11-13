# Monte Carlo Tree Search
# Adapted from the MCTS implementation used during the CIS667 lecture at
# https://colab.research.google.com/drive/1JuNdI_zcT35MWSY4-h_2ZgH7IBe2TRYd?usp=sharing
# by Prof. Garret Katz

from tictactoe import *

class Node:
    def __init__(self, state):
        self.state = state
        self.visit_count = 0
        self.score_total = 0
        self.score_estimate = 0
        self.child_list = None

    def children(self):
        # Only generate children the first time they are requested and memoize
        if self.child_list == None:
            self.child_list = list(map(Node, children_of(self.state)))
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
    if not np.size(U):
        print("U is empty sequence!")
        print("length of children", len(node.children()))
        print("Q.shape", Q.shape)
        print("N.shape", N.shape)
    return node.children()[np.argmax(U)]

#choose_child = exploit
#choose_child = explore
choose_child = uct

def rollout(node):
    if is_leaf(node.state): result = score_of(node.state)
    else: result = rollout(choose_child(node))
    node.visit_count += 1
    node.score_total += result
    node.score_estimate = node.score_total / node.visit_count
    return result

# gauge sub-optimality with rollouts
def mcts(state):
    num_rollouts = 1400 # don't do more than 1400 to keep AI's turn below 30 seconds
    node = Node(state)
    for r in range(num_rollouts):
        rollout(node)
        if r % (num_rollouts // 10) == 0: print(r, node.score_estimate)
    # return best child
    children = node.children()
    best_child = children[0]
    for i in range(len(children)):
        if children[i].score_estimate > best_child.score_estimate:
            best_child = children[i]
    return best_child.state