__version__ = '0.2.0'

import os
import sys
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from keras.utils import plot_model 

"""
Input file format
output, input1, input2, ..., inputN
"""

class NeuralNet(object):
    def __init__(self, batch_size = 30,
                       layers = [20, 2],
                       learnrate = 0.01,
                       epochs = 1000):
        self.batch_size = batch_size
        self.layers = layers
        self.epochs = epochs
        self.learn_rate = learnrate
        self.model = Sequential()
    
    def TrainModel(self, X, Y):
        in_layer = len(X[0])
        out_layer = len(Y[0])
        self.model.add(Dense(in_layer, input_dim = in_layer, activation = 'relu'))
        for lay in self.layers:
            self.model.add(Dense(lay, activation = 'relu'))
        self.model.add(Dense(out_layer, activation = None))
        sgd = SGD(lr=self.learn_rate)
        self.model.compile(loss = "hinge", optimizer = sgd, metrics = ['accuracy'])
        self.model.fit(X, Y, epochs = self.epochs, batch_size = self.batch_size)

    def TestModel(self, X, Y):
        return self.model.evaluate(X, Y)

    def ImportData(self, filepath):
        with open(filepath, 'r') as f:
            data = np.genfromtxt(f, dtype=str, delimiter=',', skip_header=0)
        y = data[:,0]
        y = [[int(r)] for r in y]
        x = data[:, 1:]
        x = [[int(r, 16) for r in v] for v in x]
        return x, y
    
    def TrainModelByPath(self, filepath):
        x, y = self.ImportData(filepath)
        self.TrainModel(x, y)

    def TestModelByPath(self, filepath):
        x, y = self.ImportData(filepath)
        return self.TestModel(x, y)

    def PrintWeights(self):
        print("Weights:",self.model.get_weights())

    def PlotModel(self, imgpath='model.png'):
        plot_model(self.model, to_file=imgpath)

    def Predict(self, data_in):
        return self.model.predict(data_in)


def main(in_args):
    # Check that in and out lengths add up <- I wrote this comment a long time ago but wtf does this mean...?
    NNET = NeuralNet()
    NNET.TrainModelByPath(in_args[0], N_PARAMS)
    if len(in_args) > 1:
        score = NNET.TestModelByPath(in_args[1], N_PARAMS)
        print("score:", score)


if __name__ == '__main__':
    main(sys.argv[1:])