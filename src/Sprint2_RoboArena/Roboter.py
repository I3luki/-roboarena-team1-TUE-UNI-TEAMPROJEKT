import pygame

class Robot:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 2
        self.aabb = [(self.x, self.y), (self.x + self.width, self.y + self.height)]

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

    