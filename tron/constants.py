import pygame

pygame.init()

from enum import Enum

CANCEL_KEY = pygame.K_q
PAUSE_KEY = pygame.K_p

class State(Enum):
    LOBBY=1
    HELP=2
    PAUSE=3
    PLAY=4
