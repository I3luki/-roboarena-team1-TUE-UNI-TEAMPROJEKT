import pygame



class Level:

    def __init__(self, screen):

        self.screen = screen

        self.current_level = 1

        # aktuelle eingesammelte Orbs im aktuellen Level
        self.current_orbs = 0

        # benötigte Orbs fürs nächste Level
        self.orbs_needed = 3

        self.font = pygame.font.SysFont(None, 36)

        self.x = screen.get_width() - 270
        self.y = 10


    
    def collect_orb(self, buff_manager, game):

        self.current_orbs += 1
        game.orbs += 1

        # wenn genug Orbs gesammelt wurden
        if self.current_orbs >= self.orbs_needed:
         
            self.level_up(buff_manager, game)


    def level_up(self, buff_manager, game):

        self.current_level += 1
        game.score += 1
        # nächstes Level braucht mehr Orbs
        self.orbs_needed += 1

        # Fortschritt zurücksetzen
        self.current_orbs = 0

        #Buffmanger aufrufen

        buff_manager.generate_choices()

    # Zeichnet die Anzeige
    def draw(self):

        text = self.font.render(
            f"Level: {self.current_level} ",
            True,
            (255,255,255)
        )

        self.screen.blit(text, (self.x, self.y))

    def reset(self):
        self.current_level=1
        self.current_orbs = 0
        bar_x = self.x
        bar_y = self.y + 35
        bar_width = 250
        bar_height = 20

        # Hintergrund
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            (bar_x, bar_y, bar_width, bar_height)
        )

        # Füllstand
        fill_width = int(bar_width * (self.current_orbs / self.orbs_needed))

        pygame.draw.rect(
            self.screen,
            (0, 200, 255),
            (bar_x, bar_y, fill_width, bar_height)
        )

        # Rahmen
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (bar_x, bar_y, bar_width, bar_height),
            1
        )
