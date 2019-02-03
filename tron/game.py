import pygame
import sys

from tron.constants import State
from tron.windows import LobbyWindow, HelpWindow, PlayWindow
from enum import Enum
from tron.player import HumanPlayer, CPUPlayer, Direction

pygame.init()
pygame.font.init()

class GameType(Enum):
    HH = 1
    HC = 2
    CC = 3

size = (640, 480)

class Game:
    def __init__(
        self, 
        size, 
        framerate=25, 
        game_type=GameType.HH, 
        network1=None, 
        network2=None, 
        render=True, 
        initial_state=State.LOBBY,
        training=False
    ):
        self.size = size
        if render:
            self.screen = pygame.display.set_mode(size)
            self.state = initial_state
            self.lobby_window = LobbyWindow(self.screen, size)
            self.help_window = HelpWindow(self.screen, size)
        else:
            self.screen = None
            self.state = State.PLAY
        self.background = (0, 0, 0)
        self.framerate = framerate
        self.render = render
        self.offset = 10
        self.player_size = 10
        self.game_type = game_type
        self.network1 = network1
        self.network2 = network2
        self.training = training
        self.play_window = PlayWindow(self.screen, self.framerate, self.init_players(), self.render, size, training)
        self.done = False
        
        
    def init_players(self):
        width, height = self.size
        player1 = HumanPlayer(
            0,
            (0, 255, 0), 
            self.offset, 
            self.offset, 
            self.player_size,
            Direction.EAST,
            {
                pygame.K_UP: Direction.NORTH,
                pygame.K_RIGHT: Direction.EAST,
                pygame.K_DOWN: Direction.SOUTH,
                pygame.K_LEFT: Direction.WEST
            }
        )
        if self.game_type == GameType.HH:
            players = [
                player1,
                HumanPlayer(
                    1,
                    (0, 0, 255), 
                    width - self.offset - self.player_size,
                    height - self.offset - self.player_size, 
                    self.player_size,
                    Direction.WEST,
                    {
                        pygame.K_w: Direction.NORTH,
                        pygame.K_d: Direction.EAST,
                        pygame.K_s: Direction.SOUTH,
                        pygame.K_a: Direction.WEST
                    }
                )
            ]
        elif self.game_type == GameType.HC:
            players = [
                player1,
                CPUPlayer(
                    1,
                    (255,255,255),
                    width - self.offset - self.player_size,
                    height - self.offset - self.player_size,
                    self.player_size,
                    Direction.WEST,
                    self.network1
                )
            ]
        else:
            players = [
                CPUPlayer(
                    0,
                    (255,255,255),
                    self.offset,
                    self.offset,
                    self.player_size,
                    Direction.EAST,
                    self.network1
                ),
                CPUPlayer(
                    1,
                    (255,0,255),
                    width - self.offset - self.player_size,
                    height - self.offset - self.player_size,
                    self.player_size,
                    Direction.WEST,
                    self.network2
                )
            ]
        return players
        
    
    def mainloop(self):
        while not self.done:
            if self.state == State.LOBBY:
                self.lobby_window.loop()
                self.state = self.lobby_window.next_state
            elif self.state == State.HELP:
                self.help_window.loop()
                self.state = self.help_window.next_state
            elif self.state == State.PLAY:
                self.play_window = PlayWindow(self.screen, self.framerate, self.init_players(), self.render)
                self.play_window.loop()
                self.state = self.play_window.next_state
                    

if __name__ == "__main__":
    game = Game(size)
    game.mainloop()
    
