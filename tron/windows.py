import pygame
import sys

from tron.constants import CANCEL_KEY, PAUSE_KEY, State
from tron.controls import Label, Button
from tron.player import Player, HumanPlayer, Direction

pygame.init()
pygame.font.init()

class Window:
    def __init__(self, controls, players, screen, size):
        self.size = size
        self.controls = controls
        self.players = players
        self.screen = screen
        self.done = False
        self.next_state = None
        
    
    def check_quit(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            
    
    def check_controls(self, event):
        for control in self.controls:
            if control.test is not None:
                control.test(event)
    
    
    def draw_controls(self):
        for control in self.controls:
            control.draw(self.screen)
        

class LobbyWindow(Window):
    def __init__(self, screen, size):
        
        self.button_width = 100
        self.button_height = 50
        self.button_text_size = 30
        self.button_color = (0, 153, 255) # Light teal
        self.button_text_color = (255, 255, 255)
        self.button_text_size = 20
        self.background_color = (0, 0, 0)
        self.size = screen.get_size()
        # Create title that blends into background with teal text.
        # Bold and center the title.
        self.title = Label(top=self.size[1]//15, left=0, 
            width=200, height=100, color=self.background_color,
            text_color=(66, 244, 197), text="TRON", size=20)
        self.title.center_horizontally(screen)
        self.title.bold()
        
        # Create play and instruction buttons
        self.num_buttons = 2
        self.play_button = Button(top=self.size[1]/2, 
            left=(self.size[0]-self.num_buttons*self.button_width)//3,
            width=self.button_width, height=self.button_height,
            color=self.button_color, text="PLAY", 
            text_color=self.button_text_color, callback=self.go_to_play,
            size=self.button_text_size)
        self.help_button = Button(top=self.size[1]/2, 
            left=2*(self.size[0]-(self.num_buttons-1)*self.button_width)//3,
            width=self.button_width, height=self.button_height,
            color=self.button_color, text="HELP", 
            text_color=self.button_text_color, callback=self.go_to_help,
            size=self.button_text_size)
        super().__init__(
            [
                self.title,
                self.play_button,
                self.help_button,
            ]
            , [], screen, size
        )
    
    
    def loop(self):
        self.done = False
        while not self.done:
            self.screen.fill(self.background_color)
            for event in pygame.event.get():
                self.check_controls(event)
                self.check_quit(event)
            self.draw_controls()
            
            pygame.display.flip()
            
    
    def go_to_play(self):
        self.next_state = State.PLAY
        self.done = True
        
    
    def go_to_help(self):
        self.next_state = State.HELP
        self.done = True


class HelpWindow(Window):
    def __init__(self, screen, size):
        size = screen.get_size()
        self.background_color = (0, 0, 0)
        self.instructions = Label(top=10, left=10, width=9*size[0]//10,
            height=30, size=20, color=self.background_color, 
            text="HOW TO PLAY", text_color=(255,255,255), centered=False)
        self.back_button = Button(top=7*size[1]//10, width=100,
            height=50, size=20, color=(0, 153, 255), # Light teal
            text="BACK", text_color=(255,255,255), callback=self.go_to_lobby)
        self.back_button.center_horizontally(screen)
        super().__init__(
            [
                self.instructions,
                self.back_button,
            ], [], screen, size
        )
            
    
    def loop(self):
        self.done = False
        while not self.done:
            self.screen.fill(self.background_color)
            for event in pygame.event.get():
                self.check_quit(event)
                self.check_controls(event)
            self.draw_controls()
            
            pygame.display.flip()
        
        
    def go_to_lobby(self):
        self.next_state = State.LOBBY
        self.done = True


class PlayWindow(Window):
    def __init__(self, screen, framerate, players, render, size, training):
        width, height = size
        self.background_color = (10,10,10)
        self.framerate = framerate
        self.render = render
        self.training = training
        if training:
            self.frames = [0, 0]
        super().__init__(
            [],
            players,
            screen,
            size
        )
        
        
    def draw(self):
        self.screen.fill(self.background_color)
        for player in self.players:
            player.draw(self.screen)
        pygame.display.flip()
       
        
    def loop(self):
        self.done = False
        clock = pygame.time.Clock()
        loser = None
        width, height = self.size
        frame = 0
        while not self.done:
            frame += 1
            clock.tick(self.framerate)
            #print(clock.get_fps())
            for event in pygame.event.get():
                self.check_quit(event)
                for player in self.players:
                    player.control(event=event)
                if event.type == pygame.KEYDOWN:
                    if event.key == CANCEL_KEY:
                        self.done = True
                        self.next_state = State.LOBBY
                        break;
                    elif event.key == PAUSE_KEY:
                        # Go back to lobby for now
                        # TODO: Implement pausing
                        self.done = True
                        self.next_state = State.LOBBY
                        break;
            #print("Setting all_killboxes")
            all_killboxes = pygame.sprite.Group()
            for player in self.players:
                player.move()
                all_killboxes.add(player.kill_boxes)
                all_killboxes.add(player.current_kill_box)
            #print("Getting game state")
            i = 0
            while i < len(self.players):
                #print(player)
                sense_directions = []
                tests = (
                    Player(
                        "test1", 
                        (255,255,255), 
                        self.players[i].rect.left, 
                        self.players[i].rect.top, 
                        self.players[i].size, 
                        self.players[i].direction
                    ),
                    Player(
                        "test2", 
                        (255,255,255), 
                        self.players[i].rect.left, 
                        self.players[i].rect.top, 
                        self.players[i].size, 
                        self.players[i].direction.next()
                    ),
                    Player(
                        "test3", 
                        (255,255,255), 
                        self.players[i].rect.left, 
                        self.players[i].rect.top, 
                        self.players[i].size, 
                        self.players[i].direction.prev()
                    )
                )
                for player_test in tests:
                    while not player_test.check_die(all_killboxes, (width, height)):
                        player_test.move()
                    sense_directions.append(
                        (self.players[i].rect.centerx-player_test.rect.centerx)**2 
                        + (self.players[i].rect.centery-player_test.rect.centery)**2
                    )
                game_state = [
                    self.players[i].rect.left,
                    self.players[i].rect.top,
                    self.players[i].rect.width,
                    self.players[i].rect.height,
                    self.players[i].direction.value,
                    self.players[i].speed,
                    width,
                    height,
                ]
                game_state.extend(sense_directions)
                #print(game_state)
                self.players[i].control(game_state=game_state)
                #print("executed control")
                if self.players[i].check_die(all_killboxes, (width, height)):
                    if not self.training:
                        #print("checked for death")
                        loser = self.players[i]
                        self.done = True
                        break
                    else:
                        #print("deleting player")
                        del self.players[i]
                        i -= 1
                        self.frames[i] = frame
                        if len(self.players) == 0:
                            self.done = True
                i += 1
            if self.render:
                #print("rendering")
                self.draw()
        if loser is not None and self.render:
            self.done = False
            disappear_rate = 1
            loser.rect.height *= 2
            loser.rect.centery -= loser.rect.height//4
            while not self.done:
                clock.tick(20)
                self.screen.fill(self.background_color)
                for event in pygame.event.get():
                    self.check_quit(event)
                for player in self.players:
                    player.draw(self.screen)
                if loser.rect.width <= 0:
                    if loser.rect.height <= 0:
                        self.done = True
                        self.next_state = State.LOBBY
                        break
                    else:
                        pt = (loser.rect.centerx, loser.rect.centery)
                        loser.rect.height -= disappear_rate
                        loser.rect.centerx, loser.rect.centery = pt
                else:
                    pt = (loser.rect.centerx, loser.rect.centery)
                    loser.rect.width -= disappear_rate
                    loser.rect.centerx, loser.rect.centery = pt
                pygame.display.flip()
        if self.training:
            return self.frames
            

