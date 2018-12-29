import numpy as np
import random

from layer import Layer


class Network:
    def __init__(self, layer_nums:list):
        self.layer_nums = layer_nums
        self.layers = []
        self.volatility = random.random() * 5
        for i in range(len(layer_nums) - 1):
            self.layers.append(Layer(layer_nums[i], layer_nums[i+1]))
        
    
    def forward_propagate(self, input_vals:np.ndarray):
        activation = self.layers[0].activate(input_vals)
        for i in range(len(self.layers)-1):
            activation = self.layers[i+1].activate(activation)
        return activation
        
        
    def reproduce(self):
        new_network = Network(self.layer_nums)
        for i in range(len(self.layers)):
            new_network.layers[i].weights = np.copy(self.layers[i].weights)
            new_network.layers[i].weights += (
                (np.random.rand(*new_network.layers[i].weights.shape)-0.5)
                * self.volatility)
            new_network.volatility = random.random() * self.volatility
        return new_network
