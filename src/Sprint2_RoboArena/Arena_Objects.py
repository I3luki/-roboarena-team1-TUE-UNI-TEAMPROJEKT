import pygame
from Collision import AABB
from Status_Effects import Speed_Buff, Healthgen_Buff

# zeichnet die gegebene Instanz
def draw(rect):
        rect.aabb.update(rect.x, rect.y,
                         rect.x + rect.width, rect.y + rect.height)
        x_screen, y_screen = rect.camera.global_to_screen(rect)
        rect.screen.blit(rect.surface,
                         (x_screen, y_screen))
        
# Zeichnet die AABB der gegeben Instanz:        
def draw_aabb(rect):
        # berechne screen Koordinaten
        x_min_screen, y_min_screen = rect.camera.global_to_screen(rect)  

        rect.aabb.draw_at(rect.arena, x_min_screen, y_min_screen)
        



class Wall: 
    COLOR = (0,0,255)
     
    def __init__(self, arena, x, y, width, height):
          self.arena = arena
          self.screen = arena.screen
          self.camera = arena.camera
          self.x = x
          self.y = y
          self.width = width
          self.height = height
          self.aabb = AABB(x,y,
                           x + self.width, y + self.height)

          self.surface = pygame.Surface((width, height))
          self.surface.fill(self.COLOR)
             

    def draw(self):
        draw(self) # globale Methode

    def draw_aabb(self):
         draw_aabb(self) # globale Methode

        

class Speedtile:
    COLOR  = (255, 255, 0) #yellow
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.aabb = AABB(x,y,
                         x + self.width, y + self.height)
        
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    # applies the unique effect to the given robot
    def apply_to(self, robot):
         status_effect = Speed_Buff()
         robot.add_status_effect(status_effect)
         

    def draw(self):
        draw(self) # globale Methode
    
    def draw_aabb(self):
         draw_aabb(self) # globale Methode
    
     

class Healthtile:
    COLOR  = (255, 105, 180) # pink
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.aabb = AABB(x,y,
                         x + self.width, y + self.height)        

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def apply_to(self, robot):
         status_effect = Healthgen_Buff()
         robot.add_status_effect(status_effect)

    def draw(self):
        draw(self) # globale methode

    def draw_aabb(self):
         draw_aabb(self) # globale Methode
     

class Surprisetile:
    COLOR  = (128, 0, 128) # purple
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.aabb = AABB(x,y,
                         x + self.width, y + self.height)
        
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        draw(self) # globale Methode

    def draw_aabb(self):
         draw_aabb(self) # globale Methode