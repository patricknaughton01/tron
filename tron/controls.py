import pygame
import sys

pygame.init()
pygame.font.init()

class Button:
    """
    Button class. Used to create a rectangular button.
    """
    def __init__(self, top:int=0, left:int=0, width:int=0, 
        height:int=0, color=None, text:str=None, size:int=1, 
        text_color=None, padding:int=5, centered:bool=True,
        callback=None):
        """
        Initializes the Button
        :param int top: y location of top corner
        :param int left: x location of left corner
        :param int width: width of button
        :param int height: height of button
        :param (int, int, int) color: color of button
        :param str text: text to display in button
        :param int size: size of text in button
        :param (int, int, int) text_color: color of text
        :param int padding: padding between edge and text 
            (overriden if centered is True)
        :param bool centered: center text?
        :param func callback: function to call when button is clicked
        """
        
        if color is None:
            self.color = (255, 255, 255)
        else:
            self.color = color
        if text is None:
            self.text = "Control"
        else:
            self.text = text
        self.size = size
        if text_color is None:
            self.text_color = (0, 0, 0)
        else:
            self.text_color = text_color
        self.font_list = "Courier New, Courier, Arial, Helvetica"
        self.font = pygame.font.SysFont(
            self.font_list, 
            self.size
        )
        self.padding = padding
        self.centered = centered
        if callback is None:
            self.callback = self.empty
        else:
            self.callback = callback
        self.rect = pygame.Rect(left, top, width, height)
        self.check_bounds()
        
        
    def set_size(self, size:int):
        """
        Resets the size of the font.
        :param int size: New font size
        """
        self.size = size
        self.font = pygame.font.SysFont(self.font_list, self.size)
        self.check_bounds()
        
    
    def check_bounds(self):
        width, height = self.font.size(self.text)
        if self.rect.width < width + self.padding:
            self.rect.width = width + self.padding
        if self.rect.height < height + self.padding:
            self.rect.height = height + self.padding
    
    
    def bold(self):
        self.font = pygame.font.SysFont(self.font_list, self.size, bold=True)
        
        
    def draw(self, surface):
        """
        Draws the button on the passed in surface
        :param pygame.Surface surface: The surface to draw on
        """
        pygame.draw.rect(
            surface, self.color, 
            self.rect
        )
        padding_left, padding_top = self.padding, self.padding
        if self.centered:
            width, height = self.font.size(self.text)
            padding_left = int((self.rect.width - width)/2)
            padding_top = int((self.rect.height - height)/2)
        surface.blit(
            self.font.render(self.text, False, self.text_color), 
            (self.rect.left + padding_left, self.rect.top + padding_top)
        )
        
        
    def test(self, event):
        """
        Tests the event to determine if it should execute
        its callback.
        :param pygame.Event event: the event to check
        """
        if (event.type == pygame.MOUSEBUTTONUP 
            and self.rect.collidepoint(pygame.mouse.get_pos())):
            self.callback()
        
    
    def center_both(self, surface):
        """
        Centers this button on both axes
        :param pygame.Surface surface: The pygame surface to center on
        """
        self.center_horizontally(surface)
        self.center_vertically(surface)
    
        
    def center_horizontally(self, surface):
        """
        Centers this button horizontally on the passed surface
        :param pygame.Surface surface: The pygame surface to center on
        """
        self.rect.left = surface.get_size()[0]//2 - self.rect.width//2
        
    
    def center_vertically(self, surface):
        """
        Centers this button vertically on the passed surface
        :param pygame.Surface surface: The pygame surface to center on
        """
        self.rect.top = surface.get_size()[1]//2 - self.rect.height//2
    
    
    def empty(self):
        """
        Empty function used as placeholder.
        """
        pass
        
        
class Label(Button):
    def __init__(self, top:int=0, left:int=0, width:int=0, 
        height:int=0, color=None, text:str=None, size:int=1, 
        text_color=None, padding:int=5, centered:bool=True):
        
        super().__init__(top=top, left=left, width=width, 
            height=height, color=color, text=text, size=size,
            text_color=text_color, padding=padding) 


if __name__ == "__main__":
    def test():
        print("Clicked!")
    screen = pygame.display.set_mode([640, 480])
    my_button = Button(
        top=0, 
        left=0, 
        width=200, 
        height=100, 
        size=50, 
        callback=test
    )
    while True:
        for event in pygame.event.get():
            my_button.test(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        my_button.draw(screen)
        pygame.display.flip()
    
    
