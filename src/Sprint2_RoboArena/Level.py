import pygame



class Level:

    def __init__(self, screen):
        self.screen = screen
        self.current_level = 1
        # aktuelle eingesammelte Orbs im aktuellen Level
        self.current_xp = 0
        # benötigte Orbs fürs nächste Level
        self.base_xp_needed = 10 # XP Startwert
        self.xp_needed = self.base_xp_needed
        self.font = pygame.font.SysFont(None, 36)
        self.x = screen.get_width() - 270
        self.y = 10
        # sound played on lvlup
        self.sound = pygame.mixer.Sound("SFX/lvlup-1.wav")


    
    def collect_orb(self, buff_manager, game, xp_value):

        self.current_xp += xp_value
        game.orbs += 1

        # wenn genug Orbs gesammelt wurden
        if self.current_xp >= self.xp_needed:
         
            self.level_up(buff_manager, game)


    def level_up(self, buff_manager, game):

        self.sound.play()
        self.current_level += 1
        game.score += 1

        # Überschüssige XP in das nächste Level mitnehmen!
        remainder = self.current_xp - self.xp_needed
        self.current_xp = max(0, remainder)

        # --- DYNAMISCHE XP-KURVE ---
        # Level 2 braucht 15, Level 5 braucht 33, Level 10 braucht 88...
        self.xp_needed = int(self.base_xp_needed * (self.current_level ** 1.35))

        buff_manager.generate_choices(game)

    # Zeichnet die Anzeige
    def draw(self):

        text = self.font.render(
            f"Level: {self.current_level} ",
            True,
            (255,255,255)
        )

        self.screen.blit(text, (self.x, self.y))


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
        fill_width = int(bar_width * (self.current_xp / self.xp_needed))

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
    def reset(self):
        self.current_level=1
        self.current_xp = 0
        self.xp_needed = self.base_xp_needed