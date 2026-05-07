import pygame

class Arena:
    def __init__(self, screen):
        self.screen = screen
        self.width = 1000        
        self.height = 1000

        # Surfaces erstellen
        self.background_surf = pygame.Surface(screen.get_size())
        self.background_surf.fill((200, 200, 200))

        self.wall_surf = pygame.Surface((50, 50))
        self.wall_surf.fill((44, 44, 44))

        self.red_surf = pygame.Surface((50, 50))
        self.red_surf.fill((255, 0, 0))

        self.blue_surf = pygame.Surface((50, 50))
        self.blue_surf.fill((0, 0, 255))

        self.green_surf = pygame.Surface((50, 50))
        self.green_surf.fill((0, 255, 0))

        self.yellow_surf = pygame.Surface((50, 50))
        self.yellow_surf.fill((255, 255, 0))

    def draw(self):
        self.screen.blit(self.background_surf, (0, 0))

        # Wände
        for x in range(0, 1000, 50):
            self.screen.blit(self.wall_surf, (x, 0))
            self.screen.blit(self.wall_surf, (x, 950))
        for y in range(0, 1000, 50):
            self.screen.blit(self.wall_surf, (0, y))
            self.screen.blit(self.wall_surf, (950, y))

        # Blaue Hindernisse
        for x in range(200, 400, 50):
            self.screen.blit(self.blue_surf, (x, 200))
            self.screen.blit(self.blue_surf, (x, 750))
        for x in range(600, 800, 50):
            self.screen.blit(self.blue_surf, (x, 200))
            self.screen.blit(self.blue_surf, (x, 750))
        for y in range(200, 400, 50):
            self.screen.blit(self.blue_surf, (200, y))
            self.screen.blit(self.blue_surf, (750, y))
        for y in range(600, 800, 50):
            self.screen.blit(self.blue_surf, (200, y))
            self.screen.blit(self.blue_surf, (750, y))

        # Gelb, Rot, Grün
        self.screen.blit(self.yellow_surf, (475, 475))

        self.screen.blit(self.red_surf, (50, 50))
        self.screen.blit(self.red_surf, (50, 900))
        self.screen.blit(self.red_surf, (900, 50))
        self.screen.blit(self.red_surf, (900, 900))

        self.screen.blit(self.green_surf, (350, 350))
        self.screen.blit(self.green_surf, (600, 350))
        self.screen.blit(self.green_surf, (350, 600))
        self.screen.blit(self.green_surf, (600, 600))