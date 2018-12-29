import numpy as np
import datetime
import pygame
import random

from network import Network
from tron.game import Game, GameType


pygame.init()


class Generation:
    def __init__(self, 
        size:int, 
        network_layer_nums:list, 
        survival_rate:float, 
        random_generation:int):
        
        self.age = 0
        self.players = []
        self.survival_rate = survival_rate
        self.size = size
        self.random_generation = random_generation
        self.network_layer_nums = network_layer_nums
        for i in range(size):
            self.players.append(Network(network_layer_nums))
    
    
    def do_generation(self, render=False):
        self.age += 1
        players = {}
        for i in range(len(self.players)//2):
            if render:
                print("Evaluating matchup {} of {}".format(i+1, self.size//2))
            # result[0] = winner, [1] = loser
            result = self.evaluate(
                self.players[i], 
                self.players[len(self.players)//2 + i],
                render=render
            )
            players[self.players[i]] = result[0]
            players[self.players[len(self.players)//2 + i]] = result[1]
        players = sorted(players.items(), key=lambda kv: kv[1], reverse=True)
        self.players = [item[0] for item in players]
        self.players = self.players[:int(len(self.players)*self.survival_rate)]
        """losers = losers[:int(len(losers)*self.survival_rate)]
        self.players = winners
        self.players.extend(losers)"""
        i = 0
        while i < self.random_generation and len(self.players) < self.size:
            self.players.append(Network(self.network_layer_nums))
            i += 1
        for i in range(self.size - len(self.players)):
            self.players.append(random.choice(self.players).reproduce())
        if render:
            pygame.display.quit()
            pygame.display.init()
            
    
    def evaluate(self, player1, player2, render=False):
        game = Game(
            (400, 400), 
            framerate=200, 
            game_type=GameType.CC,
            network1=player1,
            network2=player2,
            render=render,
            training=True
        )
        return game.play_window.loop()
            
