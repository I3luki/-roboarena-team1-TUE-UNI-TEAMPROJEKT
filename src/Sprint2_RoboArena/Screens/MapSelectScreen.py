import pygame

class MapSelectScreen:

    def __init__(self, screen):
        self.screen = screen

        self.background = pygame.image.load(
            "Sprites/Mainmenu_Background.png"
            ).convert()

        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )

        self.font_title = pygame.font.SysFont(None, 80)
        self.font_text = pygame.font.SysFont(None, 50)

    def draw(self, game):
        self.screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((420, 420), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))   # Schwarz mit Transparenz
        self.screen.blit(overlay, (300, 120))

        #Mit oder ohne freischaltung der 2 map
        if game.is_map_unlocked("labyrinth_map"):
            map2_text = "2 - Labyrinth Map"
        else:
            map2_text = "2 - Labyrinth Map (GESPERRT)"


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
            map2_text,
            True,
            (255, 255, 255)
        )
        esc_text = self.font_text.render(
            "ESC - Zurueck zum Hauptmenue",
            True,
            (200, 200, 200)
        )

        self.screen.blit(esc_text, (320, 650))
        self.screen.blit(title, (250, 200))
        self.screen.blit(map1, (320, 400))
        self.screen.blit(map2, (320, 500))

    #keypress
    def handle_event(self, event, game):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                game.selected_map = 1
                game.state = "PLAYING"

            elif event.key == pygame.K_2:
                if game.is_map_unlocked("labyrinth_map"):
                    game.selected_map = 2
                    game.state = "PLAYING"
                else:
                    print("Labyrinth Map ist noch gesperrt.")

            elif event.key == pygame.K_ESCAPE:
                game.state = "MENU"