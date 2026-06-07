import random
import pygame

class BuffManager:

    def __init__(self):

        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 60)

        self.available_buffs = [
            "Mehr Leben",
            "Mehr Geschwindigkeit",
            "Mehr Schaden"
        ]

        self.current_choices = []
        self.active = False

    def generate_choices(self):

        self.current_choices = random.sample(self.available_buffs, 2)
        self.active = True

    def apply_buff(self, index, robot, health):

        buff = self.current_choices[index]

        if buff == "Mehr Leben":
            health.max_health += 20
            health.current_health += 20

        elif buff == "Mehr Geschwindigkeit":
            pass
             # TODO: ADD SPEED_LOGIC

        elif buff == "Mehr Schaden":
            pass
            # TODO: ADD DAMAGE_LOGIC

        self.active = False
        self.current_choices = []

    def draw(self, screen):

        if not self.active:
            return

        title = self.big_font.render(
            "LEVEL UP!",
            True,
            (255, 255, 255)
        )

        option1 = self.font.render(
            f"1 - {self.current_choices[0]}",
            True,
            (255, 255, 255)
        )

        option2 = self.font.render(
            f"2 - {self.current_choices[1]}",
            True,
            (255, 255, 255)
        )
        screen.blit(title, (350, 300))
        screen.blit(option1, (350, 400))
        screen.blit(option2, (350, 450))

