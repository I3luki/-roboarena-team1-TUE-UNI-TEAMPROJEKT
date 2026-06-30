import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS_FILE = os.path.join(BASE_DIR, "Data", "stats.txt")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "Data", "highscore.txt")

class StatsScreen:

    def __init__(self, screen):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen = screen
        self.background = pygame.image.load(
            "Sprites/Statsmenu-Background.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )
        self.title_font = pygame.font.SysFont(None, 80)
        self.text_font = pygame.font.SysFont(None, 45)
        self.scroll_offset = 0

        # Layout
        self.title_y = self.screen_height * 0.10
        self.stats_y = self.screen_height * 0.22
        self.list_y = self.screen_height * 0.30

        self.bottom_margin = 30
        self.line_spacing = 45

        self.left_margin = self.screen_width * 0.25
    #Keypress handler
    def handle_event(self, event, game):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.state = "MENU"

            elif event.key == pygame.K_r:
                self.clear_stats()

            elif event.key == pygame.K_s:
                self.scroll_offset += 1

            elif event.key == pygame.K_w:
                self.scroll_offset -= 1

                if self.scroll_offset < 0:
                    self.scroll_offset = 0
    # Liest alle gespeicherten Spieldurchläufe aus stats.txt
    def load_runs(self):
        try:
            #r für lesen
            with open(STATS_FILE, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    #Clear von stats
    def clear_stats(self):
        #w für schreiben
        open(STATS_FILE, "w").close()
        self.scroll_offset = 0

    def draw(self):
        overlay = pygame.Surface((420, 420), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))   # Schwarz mit Transparenz
        self.screen.blit(overlay, (300, 120))
        self.screen.blit(self.background, (0, 0))

        title = self.title_font.render(
            "STATISTIKEN",
            True,
            (255, 255, 255)
        )
        title_rect = title.get_rect(
            center=(self.screen_width // 2, self.title_y)
        )

        self.screen.blit(title, title_rect)

        runs = self.load_runs()

        games_text = self.text_font.render(
            f"Spiele gespielt: {len(runs)}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(
            games_text,
            (self.left_margin, self.stats_y)
        )

        max_visible = 10
        max_offset = max(0, len(runs) - max_visible)

        if self.scroll_offset > max_offset:
            self.scroll_offset = max_offset

        visible_runs = runs[self.scroll_offset:self.scroll_offset + max_visible]

        for i, run in enumerate(visible_runs):

            text = self.text_font.render(
                f"Spiel {self.scroll_offset + i + 1}: {run}",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                text,
                (self.left_margin, self.list_y + i * 40)
            )

        info = self.text_font.render(
            "ESC: Zurueck zum Hauptmenue",
            True,
            (255, 255, 0)
        )
        delete_text = self.text_font.render(
            "R: Alle Statistiken loeschen",
            True,
            (0, 0, 0)
        )

        scroll_text = self.text_font.render(
            "w/s: Scrollen",
            True,
            (200, 200, 200)
        )

        bottom_y = self.screen_height - self.bottom_margin

        scroll_rect = scroll_text.get_rect(
            bottomleft=(self.left_margin, bottom_y - self.line_spacing * 2)
        )

        delete_rect = delete_text.get_rect(
            bottomleft=(self.left_margin, bottom_y - self.line_spacing)
        )

        info_rect = info.get_rect(
            bottomleft=(self.left_margin, bottom_y)
        )

        self.screen.blit(scroll_text, scroll_rect)
        self.screen.blit(delete_text, delete_rect)
        self.screen.blit(info, info_rect)