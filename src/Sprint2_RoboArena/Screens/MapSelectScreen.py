import pygame

class MapSelectScreen:

    def __init__(self, screen):
        self.screen = screen

        self.font_title = pygame.font.SysFont(None, 80)
        self.font_text = pygame.font.SysFont(None, 50)

    def draw(self):

        self.screen.fill((20, 20, 20))

        title = self.font_title.render(
            "Map auswählen",
            True,
            (255, 255, 255)
        )

        map1 = self.font_text.render(
            "1 - Standard Map",
            True,
            (255, 255, 255)
        )

        map2 = self.font_text.render(
            "2 - Labyrinth Map",
            True,
            (255, 255, 255)
        )

        self.screen.blit(title, (250, 200))
        self.screen.blit(map1, (320, 400))
        self.screen.blit(map2, (320, 500))

    def handle_event(self, event, game):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                game.selected_map = 1
                game.state = "PLAYING"

            elif event.key == pygame.K_2:
                game.selected_map = 2
                game.state = "PLAYING"