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
        self.aabb = [(self.x, self.y), (self.x + self.width, self.y + self.height)]
        self.angle = 0


    # updatet die axis aligned bounding box
    def update_aabb(self):
         self.aabb = [(self.x, self.y), (self.x + self.width, self.y + self.height)]

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
            center=(self.x + self.width / 2, self.y + self.height / 2)
        )


        self.screen.blit(rotated_surface, rect.topleft)

    # "Zeichnet AAB-Kollisionbox"
    def draw_aabb(self):
        color = (255,0,0)
        min_x, min_y = self.aabb[0]
        max_x, max_y = self.aabb[1]
        width = max_x - min_x
        height = max_y - min_y

        pygame.draw.rect(
            self.screen,
            color,
            (min_x, min_y, width, height),
            width=1   # zeichen nur Kontur
        )

    
        # Linie zur Maus,
    def draw_line_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(
            self.screen, 
            (255, 0, 0),
            (self.x + (self.width/2), self.y + (self.height/2)),
            (mouse_x, mouse_y), 2)

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
    def update_rotation(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - (self.x + self.width / 2)
        dy = mouse_y - (self.y + self.height / 2)

        target_angle = math.degrees(math.atan2(-dy, dx))

        # Smooth Rotation
        angle_difference = (target_angle - self.angle + 180) % 360 - 180

        self.angle += angle_difference * 0.1
