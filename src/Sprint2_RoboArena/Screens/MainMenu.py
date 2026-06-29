import pygame
from sys import exit


class MainMenu:

    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(
            "Sprites/Mainmenu_Background.png"
            ).convert()

        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )

        self.options = [
            "Spiel starten",
            "Shop",
            "Statistiken",
            "Spiel beenden"
        ]

        self.selected = 0

        self.title_font = pygame.font.SysFont(None, 100)
        self.option_font = pygame.font.SysFont(None, 60)

    def handle_event(self, event, game):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_s:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:

                if self.selected == 0:
                    game.state = "MAP_SELECT"

                elif self.selected == 1:
                    game.state = "SHOP"

                elif self.selected == 2:
                    game.state = "STATS"

                elif self.selected == 3:
                    pygame.quit()
                    exit()

    def draw(self):

        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((420, 420), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))   # Schwarz mit Transparenz
        self.screen.blit(overlay, (300, 120))

        title = self.title_font.render(
            "ROBO ARENA",
            True,
            (255, 255, 255)
        )

        self.screen.blit(title, (250, 150))

        for i, option in enumerate(self.options):

            color = (255, 255, 0) if i == self.selected else (255, 255, 255)

            text = self.option_font.render(
                option,
                True,
                color
            )

            self.screen.blit(
                text,
                (350, 350 + i * 80)
            )