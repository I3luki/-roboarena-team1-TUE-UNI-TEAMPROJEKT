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

          self.surface = pygame.Surface((width, height))
          self.surface.fill(self.COLOR)


    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        self.screen.blit(self.surface,
                          (x_screen, y_screen))
        

class Speedtile:
    COLOR  = (255, 255, 0) #yellow
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        self.screen.blit(self.surface,
                          (x_screen, y_screen))
    
     

class Healthtile:
    COLOR  = (255, 105, 180) # pink
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        self.screen.blit(self.surface,
                          (x_screen, y_screen))
     

class Surprisetile:
    COLOR  = (128, 0, 128) # purple
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)


    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        self.screen.blit(self.surface,
                          (x_screen, y_screen))