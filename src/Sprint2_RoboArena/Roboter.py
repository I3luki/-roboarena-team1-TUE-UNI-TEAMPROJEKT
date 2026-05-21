import pygame
import math
from Collision import AABB


class Robot:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.camera = arena.camera
        self.screen = arena.screen
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 2
        self.aabb = AABB(self.x,
                         self.y,
                         self.x + self.width,
                         self.y + self.height)
        self.angle = 0



    # updatet die axis aligned bounding box
    def update_aabb(self):
         self.aabb.update(self.x, 
                          self.y,
                          self.x + self.width,
                          self.y + self.height)

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
        self.update_aabb()



    def draw(self):

        # lokale Koordinaten
        x_screen, y_screen = self.camera.global_to_screen(self)

        # Eigene Fläche
        robot_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Körper
        pygame.draw.rect(
            robot_surface,
            (120, 120, 120),
            (0, 0, self.width, self.height)
        )

        # Kopf
        pygame.draw.circle(
            robot_surface,
            (0, 255, 0),
            (35, 25),
            8
        )

        # Rotieren
        rotated_surface = pygame.transform.rotate(robot_surface, self.angle)

        # Mittelpunkt setzen
        rect = rotated_surface.get_rect(
            center=(x_screen + self.width/2, y_screen + self.height/2)
        )

        # zeichen in screen
        self.screen.blit(rotated_surface, rect.topleft)

    # "Zeichnet AAB-Kollisionbox"
    def draw_aabb(self):
        color = (255,0,0)
        x_min = self.aabb.x
        y_min = self.aabb.y
        x_max = self.aabb.x_max
        y_max = self.aabb.y_max
        width  = x_max - x_min
        height = y_max - y_min

        pygame.draw.rect(
            self.screen,
            color,
            (x_min, y_min, width, height),
            width=1   # Zeichne nur die Kontur
        )

    
    # Linie zur Maus,
    def draw_line_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_screen, y_screen = self.camera.global_to_screen(self)
        pygame.draw.line(
            self.screen, 
            (255, 0, 0),
            (x_screen + (self.width/2), y_screen + (self.height/2)),
            (mouse_x, mouse_y), 2)
        

    # holt den Vektor zur Maus
    def get_direction_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_x, screen_y = self.camera.global_to_screen(self)
        #Berechnet Abstand von Mauszeiger zu sich selbst
        dx = mouse_x -  screen_x
        dy = mouse_y -  screen_y

        distance = math.hypot(dx, dy)
        #Return Abstand
        if distance !=0:
            return dx / distance, dy / distance

        return 0,0
    
    # updatet den Rotationswinkel
    def update_rotation(self):
        direction_x, direction_y = self.get_direction_to_mouse()

        target_angle = math.degrees(math.atan2(-direction_y, direction_x)
        )

        # Smooth Rotation
        angle_difference = (target_angle - self.angle + 180) % 360 - 180

        self.angle += angle_difference * 0.1
