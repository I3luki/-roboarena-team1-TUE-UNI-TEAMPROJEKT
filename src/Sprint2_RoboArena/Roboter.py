import pygame
import math

class Robot:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 2

    def move(self, keys):
        if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

    def draw(self):
        # Körper
        pygame.draw.rect(
            self.screen,
            (120, 120, 120),
            (self.x, self.y, self.width, self.height)
        )

        # Kopf / Sensor
        pygame.draw.circle(
            self.screen,
            (0, 255, 0),
            (self.x + 25, self.y + 15),
            8
        )
        # Linie zur Maus,
        # Zieht eine Linie von Roboter zur Maus(Erstmal auskommentiert nur zum testen Aktivieren.)
        '''
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(
            self.screen, 
            (255, 0, 0),
            (self.x + (self.width/2), self.y + (self.height/2)),
            (mouse_x, mouse_y), 2)
        '''
    def get_direction_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #Berechnet Abstand von Mauszeiger zu sich selbst
        dx = mouse_x -  self.x
        dy = mouse_y -  self.y

        distance = math.hypot(dx, dy)
        #Return Abstand
        if distance !=0:
            return dx / distance, dy / distance

        return 0,0
