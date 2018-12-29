import pygame
import sys

pygame.init()

class Killbox(pygame.sprite.Sprite):
    def __init__(self, start, end, width, color):
        pygame.sprite.Sprite.__init__(self)
        self.start = start
        self.width = width
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect = self.get_rect(start)
        self.color = color
        
        
    def get_rect(self, end):
        if end[0] == self.start[0] and end[1] == self.start[1]:
            rect = pygame.Rect(self.start, (0, 0))
            rect.centerx = self.start[0]
            rect.centery = self.start[1]
            return rect
        elif end[0] == self.start[0]:
            self.rect.width = self.width
            if self.start[1] < end[1]:
                self.rect.height = end[1] - self.start[1]
            else:
                self.rect.height = self.start[1] - end[1]
                self.rect.top = end [1]
            self.rect.centerx = self.start[0]
        elif end[1] == self.start[1]:
            self.rect.height = self.width
            if self.start[0] < end[0]:
                self.rect.width = end[0] - self.start[0]
            else:
                self.rect.width = self.start[0] - end[0]
                self.rect.left = end[0]
            self.rect.centery = self.start[1]
            
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
