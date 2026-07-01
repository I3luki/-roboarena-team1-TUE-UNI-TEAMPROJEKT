import pygame


class StartScreen:

    def __init__(self, screen):
        self.screen = screen

        # Logo
        self.background = pygame.image.load(
            "Sprites/Startscreen.png"
        ).convert_alpha()

        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )

        # Wolken
        self.cloud = pygame.image.load(
            "Sprites/Cloud.png"
        ).convert_alpha()

        self.cloud = pygame.transform.scale(
            self.cloud,
            self.screen.get_size()
        )

        self.cloud_x = 0
        self.cloud_speed = 0.3

        self.font = pygame.font.SysFont(None, 45)

    # Tastendruck
    def handle_event(self, event, game):

        if event.type == pygame.KEYDOWN:
            game.state = "MENU"

    # Wolken bewegen
    def update(self):

        self.cloud_x += self.cloud_speed

        if self.cloud_x >= self.cloud.get_width():
            self.cloud_x = 0

    # Zeichnen
    def draw(self):

        INFO_Y = 800

        # Himmel
        self.screen.fill((90, 170, 255))

        width = self.cloud.get_width()

        # Wolken zweimal zeichnen damit sie transparent durchs bild gehen
        self.screen.blit(self.cloud, (self.cloud_x, 0))
        self.screen.blit(self.cloud, (self.cloud_x - width, 0))

        # Logo
        self.screen.blit(self.background, (0, 0))

        # Hinweis
        info = self.font.render(
            "Druecke eine beliebige Taste",
            True,
            (255, 255, 255)
        )

        info_rect = info.get_rect(
            center=(self.screen.get_width() // 2, INFO_Y)
        )

        self.screen.blit(info, info_rect)