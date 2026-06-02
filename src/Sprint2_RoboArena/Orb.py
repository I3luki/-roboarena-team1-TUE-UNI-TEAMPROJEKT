import pygame
import random
from Collision import AABB

class Orb:

    def __init__(self, arena, x, y):
        self.arena  = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.radius = 10
        self.aabb = AABB(self.x - self.radius, 
                         self.y - self.radius, 
                         self.x + self.radius,
                         self.y + self.radius)
        
        
    # aktualisiert aabb Koordinaten anhand akuteller Koordinaten des Orbs
    def update_aabb(self): 
        self.aabb.update(self.x - self.radius, 
                         self.y - self.radius, 
                         self.x + self.radius,
                         self.y + self.radius)
        
        
    # setzt Koordinaten auf zufällige Nummer innerhalb des screens
    # und updatet aabb
    def randomize_position(self):  
        # frage screengröße ab, dann erzeuge zufälliges x und y
        world_width = self.arena.WIDTH
        world_height = self.arena.HEIGHT
        while True:
            self.x = random.randint(self.radius, world_width - self.radius)
            self.y = random.randint(self.radius, world_height - self.radius)

        # update Orb-Koordinaten
            self.update_aabb()

            collision = False

            for wall in self.arena.walls:
                if self.aabb.check_collision(wall.aabb):
                    collision = True
                    break

            if not collision:
                return


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
        # berechne screen Koordinaten mit Kreis Offset
        x_min_screen, y_min_screen = self.camera.global_to_screen(self)  
        x_min_screen -= self.radius
        y_min_screen -= self.radius

        # Zeichne
        self.aabb.draw_at(self.arena, x_min_screen, y_min_screen)