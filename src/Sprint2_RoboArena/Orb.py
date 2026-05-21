import pygame
import random

class Orb:


    def __init__(self, arena, x, y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.radius = 10
        self.aabb = [(self.x - self.radius, self.y - self.radius), 
                     (self.x + self.radius, self.y + self.radius)]
        
        
    # aktualisiert aabb Koordinaten anhand akuteller Koordinaten des Orbs
    def update_aabb(self): 
        self.aabb = [(self.x - self.radius, self.y - self.radius), 
                     (self.x + self.radius, self.y + self.radius)]
        
        
    # setzt Koordinaten auf zufällige Nummer innerhalb des screens
    # und updatet aabb
    def randomize_position(self):  
        # frage screengröße ab, dann erzeuge zufälliges x und y
        screen_width, screen_height = self.screen.get_size()
        x = random.randint(0, screen_width)  
        y = random.randint(0, screen_height)

        # update Orb-Koordinaten
        self.x = x
        self.y = y
        self.update_aabb()


    # zeichnet den Orb
    def draw(self):
        color = (255,64,64)
        screen_x, screen_y = self.camera.global_to_screen(self)
        pygame.draw.circle(
            self.screen,
            color,
            (screen_x,screen_y),
            self.radius
        )


    # zeichnet die AABB (für visuelle Tests)
    def draw_aabb(self):
        color = (100,100,100)
        x_upperleft, y_upperleft   = self.aabb[0]
        x_lowerright, y_lowerright = self.aabb[1]
        width  = x_lowerright - x_upperleft
        height = y_lowerright - y_upperleft

        pygame.draw.rect(
            self.screen,
            color,
            (x_upperleft, y_upperleft, width, height),
            width=1   # Zeichne nur die Kontur
        )