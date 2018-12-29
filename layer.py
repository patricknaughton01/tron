import numpy as np

from math import pi


class Layer:
    def __init__(self, nodes:int, next_nodes:int):
        self.nodes = nodes
        self.next_nodes = next_nodes
        self.weights = np.random.rand(
            self.next_nodes,
            self.nodes + 1
        )
        
        
    def activate(self, input_vals:np.ndarray):
        input_vals = np.append(input_vals, [1])
        activation = np.matmul(self.weights, input_vals)
        return 0.5 + np.arctan(activation) / pi
        
