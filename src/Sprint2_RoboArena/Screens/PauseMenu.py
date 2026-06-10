import pygame
from sys import exit


class PauseMenu:

    def __init__(self, screen):
        self.screen = screen
        self.options = ["Weiter spielen", "Hauptmenü", "Spiel beenden"]
        self.selected = 0

        self.title_font = pygame.font.SysFont(None, 90)
        self.option_font = pygame.font.SysFont(None, 55)

    def handle_event(self,
                     event,
                     game,
                     health,
                     stamina,
                     robot,
                     arena,
                     enemy_manager,
                     orb_list,
                     level):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                game.state = "PLAYING"

            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:

                if self.selected == 0:
                    game.state = "PLAYING"

                elif self.selected == 1:
                    game.reset(
                        health,
                        stamina,
                        robot,
                        arena,
                        enemy_manager,
                        orb_list,
                        level
                    )

                    game.go_to_menu()

                elif self.selected == 2:
                    pygame.quit()
                    exit()

    def draw(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("PAUSE", True, (255, 255, 255))
        self.screen.blit(title, (380, 200))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.option_font.render(option, True, color)
            self.screen.blit(text, (350, 350 + i * 70))