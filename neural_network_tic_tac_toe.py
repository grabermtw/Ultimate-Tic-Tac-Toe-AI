# Neural Network implementation
# Adapted from the neural network implementation used during the CIS667 lecture at
# https://colab.research.google.com/drive/1QF8IJHlZ597esIU-vmW7u9KARhyXIjOY?authuser=3
# by Prof. Garret Katz

import csv
import random
import ast
import torch as tr

# Defines a network with two fully-connected layers and tanh activation functions
class LinNet(tr.nn.Module):
    def __init__(self, size, hid_features):
        super(LinNet, self).__init__()
        self.to_hidden = tr.nn.Linear(size**4, hid_features)
        self.to_output = tr.nn.Linear(hid_features, 1)
    def forward(self, x):
        gelu = tr.nn.GELU()
        h = gelu(self.to_hidden(x.reshape(x.shape[0],-1)))
        softplus = tr.nn.Softplus()
        y = softplus(self.to_output(h))
        return y

# Used for obtaining the training/testing data
def load_data(filename):
    states = []
    utilities = []
    with open(filename) as datacsv:
        reader = csv.DictReader(datacsv)
        for row in reader:
            states.append(list(map(float, ast.literal_eval(row["State"]))))
            utilities.append(float(row["Utility"]))
    shufflelist = list(zip(states, utilities))
    random.shuffle(shufflelist)
    states, utilities = zip(*shufflelist)
    states, utilities = list(states), list(utilities)
    # split into training and test data (use half for each)
    split_size = int(len(states) / 2)
    training_data = (states[:split_size], utilities[:split_size])
    testing_data = (states[split_size:], utilities[split_size:])
    return training_data, testing_data

# Calculates the error on a batch of training examples
def batch_error(net, batch):
    states, utilities = batch
    u = utilities.reshape(-1,1).float()
    y = net(states)
    e = tr.sum((y - u)**2) / utilities.shape[0]
    return e

def train(training_examples, testing_examples, filename):
    # Make the network and optimizer
    net = LinNet(size=4, hid_features=10)
    optimizer = tr.optim.SGD(net.parameters(), lr=0.001)
    # Convert the states and their minimax utilities to tensors
    states, utilities = training_examples
    training_batch = tr.stack(tuple(map(tr.tensor, states))), tr.tensor(utilities)

    states, utilities = testing_examples
    testing_batch = tr.stack(tuple(map(tr.tensor, states))), tr.tensor(utilities)

    # Run the gradient descent iterations
    curves = [], []
    for epoch in range(50000):
    
        # zero out the gradients for the next backward pass
        optimizer.zero_grad()

        e = batch_error(net, training_batch)
        e.backward()
        training_error = e.item()

        with tr.no_grad():
            e = batch_error(net, testing_batch)
            testing_error = e.item()

        # take the next optimization step
        optimizer.step()    
        
        # print/save training progress
        if epoch % 1000 == 0:
            print("%d: %f, %f" % (epoch, training_error, testing_error))
        curves[0].append(training_error)
        curves[1].append(testing_error)
    
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(["Epoch", "Training Error", "Testing Error"])
        for i in range(len(curves[0])):
            csvwriter.writerow([i, curves[0][i], curves[1][i]])
    return net

# Used to convert a game state to a tensor encoding suitable for NN input
# Uses monotonic encoding
def encode(state):
    board = state[1].copy()
    # 0 for empty cells
    # 1 for cells claimed by X
    # 2 for cells in sub-boards that have been won by X
    # -1 for cells claimed by O
    # -2 for cells in sub-boards claimed by O

    for i in range(len(board)):
        if board[i] in ["X", "Xtie"]:
            board[i] = 1
        elif board[i] in ["O", "Otie"]:
            board[i] = -1
        elif board[i] in ["Xwin"]:
            board[i] = 2
        elif board[i] in ["Owin"]:
            board[i] = -2
        else:
            board[i] = 0
    return board


