import pygame


class Level:

    def __init__(self, screen, x=10, y=75):

        self.screen = screen

        self.current_level = 1

        # aktuelle eingesammelte Orbs im aktuellen Level
        self.current_orbs = 0

        # benötigte Orbs fürs nächste Level
        self.orbs_needed = 3

        self.font = pygame.font.SysFont(None, 36)

        self.x = x
        self.y = y


    def collect_orb(self):

        self.current_orbs += 1

        # wenn genug Orbs gesammelt wurden
        if self.current_orbs >= self.orbs_needed:
            self.level_up()


    def level_up(self):

        self.current_level += 1

        # nächstes Level braucht mehr Orbs
        self.orbs_needed += 1

        # Fortschritt zurücksetzen
        self.current_orbs = 0

    # Zeichnet die Anzeige
    def draw(self):

        text = self.font.render(
            f"Level: {self.current_level}  Orbs: {self.current_orbs}/{self.orbs_needed}",
            True,
            (255,255,255)
        )

        self.screen.blit(text, (self.x, self.y))