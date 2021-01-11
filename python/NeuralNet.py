__version__ = '0.2.0'

import os
import sys
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import load_model

import Config as cfg

"""
Input file format
output, input1, input2, ..., inputN
"""

class NeuralNet(object):
    def __init__(self, layers = cfg.net_layers,
                       learnrate = cfg.net_learnrate,
                       epochs = cfg.net_learnrate,
                       in_len = cfg.in_len,
                       out_len = cfg.out_len,
                       model_path = cfg.model_path):
        self.layers = layers
        self.epochs = epochs
        self.learn_rate = learnrate
        self.model_path = model_path
        self.in_len = in_len
        self.out_len = out_len
        self.BuildModel(in_len, out_len)

    def BuildModel(self, Xlen, Ylen):
        self.model = Sequential()
        self.model.add(Dense(Xlen, input_dim = Xlen, activation = 'relu'))
        for lay in self.layers:
            self.model.add(Dense(lay, activation = 'sigmoid'))
        self.model.add(Dense(Ylen, activation = 'sigmoid'))
        sgd = SGD(lr=self.learn_rate)
        self.model.compile(loss = "MSE", optimizer = sgd, metrics = ['accuracy'])
    
    def TrainModel(self, X, Y):
        self.model.fit(X, Y, epochs = self.epochs, batch_size = None)

    def TestModel(self, X, Y):
        return self.model.evaluate(X, Y)

    def ImportData(self, filepath):
        with open(filepath, 'r') as f:
            data = np.genfromtxt(f, dtype=str, delimiter=',', skip_header=0)
        y = data[:,:self.out_len]
        y = [[int(r) for r in v] for v in y]
        x = data[:, self.out_len:]
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

    def save_model(self):
        self.model.save(self.model_path)

    def load_model(self):
        self.model = load_model(self.model_path)

    def load_weights(self, weight_path=None):
        if weight_path is None:
            weight_path = self.model_path

        self.model.load_weights(weight_path)


def main(in_args):
    # Check that in and out lengths add up <- I wrote this comment a long time ago but wtf does this mean...?
    NNET = NeuralNet()
    # NNET.load_model()
    # NNET.PrintWeights()
    NNET.TrainModelByPath(in_args[0])
    NNET.save_model()
    if len(in_args) > 1:
        score = NNET.TestModelByPath(in_args[1])
        print("score:", score)


if __name__ == '__main__':
    main(sys.argv[1:])
