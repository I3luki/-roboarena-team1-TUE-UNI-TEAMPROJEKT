import pygame

class Wall:
     
    COLOR = (0,0,255)
     
    def __init__(self, arena, x, y, width, height):
          self.screen = arena.screen
          self.camera = arena.camera
          self.x = x
          self.y = y
          self.width = width
          self.height = height


    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        pygame.draw.rect(
                    self.screen,
                    self.COLOR,
                    (x_screen, y_screen, self.width, self.height)
                )
        

class Speedtile:

    COLOR  = (25,100,25)
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y

    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        pygame.draw.rect(
                    self.screen,
                    self.COLOR,
                    (x_screen, y_screen, self.width, self.height)
                )
    
     

class Healthtile:
    COLOR  = (25,200,25)
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y

    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        pygame.draw.rect(
                    self.screen,
                    self.COLOR,
                    (x_screen, y_screen, self.width, self.height)
                )
     

class Surprisetile:
    COLOR  = (25,100,100)
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y

    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        pygame.draw.rect(
                    self.screen,
                    self.COLOR,
                    (x_screen, y_screen, self.width, self.height)
                )