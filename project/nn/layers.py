# project/nn/layers.py
import numpy as np


class Dense:
    """
    Camada totalmente conectada (y = xW + b)
    """
    def __init__(self, in_features, out_features):
        # Xavier/Glorot initialization
        limit = np.sqrt(6 / (in_features + out_features))
        self.W = np.random.uniform(-limit, limit, (in_features, out_features))
        self.b = np.zeros((1, out_features))

    def forward(self, x):
        return np.dot(x, self.W) + self.b
