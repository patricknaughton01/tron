import pygame
import sys
import numpy as np

from tron.killbox import Killbox
from enum import Enum

pygame.init()


class Direction(Enum):
    NORTH=0
    EAST=1
    SOUTH=2
    WEST=3
    
    def next(self):
        return Direction((self.value + 1)%len(Direction))
        
    def prev(self):
        return Direction((self.value - 1 + len(Direction))%len(Direction))


class Player(pygame.sprite.Sprite):
    def __init__(self, name, color, left, top, size, direction):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.color = color
        self.size = 10
        self.speed = 3
        self.rect = pygame.Rect(left, top, self.size, self.size)
        self.trail_width = 4
        self.trail_offset = 1
        self.direction = direction
        start_point = (self.rect.centerx, self.rect.centery)
        self.kill_boxes = pygame.sprite.Group();
        self.current_kill_box = Killbox(
            start_point, 
            start_point, 
            self.trail_width,
            self.color
        )
        
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        for box in self.kill_boxes:
            box.draw(surface)
        self.current_kill_box.draw(surface)
        
    
    def turn(self, direction):
        if (self.direction.value - direction.value)%2 != 0:
            self.direction = direction
            self.kill_boxes.add(self.current_kill_box)
            tmp = self.speed
            self.speed = -self.trail_width//2
            self.move()
            point = (self.rect.centerx, self.rect.centery)
            self.current_kill_box = Killbox(
                point,
                point,
                self.trail_width,
                self.color
            )
            # Move us away from the previous killbox so we don't 
            # immediately intersect it. Then reset our speed
            self.speed = self.size//2 + 1 + self.trail_width
            self.move()
            self.speed = tmp
        
        
    def move(self):
        if self.direction == Direction.NORTH:
            self.rect.top -= self.speed
        elif self.direction == Direction.EAST:
            self.rect.left += self.speed
        elif self.direction == Direction.SOUTH:
            self.rect.top += self.speed
        elif self.direction == Direction.WEST:
            self.rect.left -= self.speed
        self.current_kill_box.get_rect(
            (self.rect.centerx, self.rect.centery)
        )
        
        
    def check_die(self, killboxes, size):
        return self.check_collision(killboxes) or self.check_walls(size)
        
        
    def check_collision(self, killboxes):
        # Will always intersect our own current_kill_box,
        # shouldn't result in a loss.
        collisions = pygame.sprite.spritecollide(self, killboxes, False)
        return len(collisions) > 1
        
        
    def check_walls(self, size):
        return (self.rect.left < 0 or self.rect.right > size[0]
            or self.rect.top < 0 or self.rect.bottom > size[1] )
        

class HumanPlayer(Player):
    def __init__(self, name, color, left, top, size, direction, controls):
        super().__init__(name, color, left, top, size, direction)
        self.controls = controls
        
    
    def control(self, event=None, game_state=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key in self.controls:
                    self.turn(self.controls[event.key])
                

class CPUPlayer(Player):
    def __init__(self, name, color, left, top, size, direction, network):
        super().__init__(name, color, left, top, size, direction)
        self.network = network
        self.controls = (
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        )
        
    
    def control(self, event=None, game_state=None):
        # `outputs` is a 4 element column vector representing pressing the 
        # north, east, south, and west buttons. A button is considered pressed
        # if the corresponding output is > 0.5. If multiple buttons are pressed
        # the first one (given the above sequence) is given priority
        if game_state is not None:
            outputs = self.network.forward_propagate(np.asarray(game_state))
            #print("forward propagated")
            for i in range(len(outputs)):
                #print(self.controls[i])
                if outputs[i] > 0.5:
                    self.turn(self.controls[i])
        
