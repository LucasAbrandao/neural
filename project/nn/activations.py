# project/nn/activations.py
import numpy as np


class ReLU:
    def forward(self, x):
        return np.maximum(0, x)


class Softmax:
    def forward(self, x):
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / np.sum(e_x, axis=1, keepdims=True)
