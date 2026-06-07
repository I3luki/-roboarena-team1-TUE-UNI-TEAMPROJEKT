import random
import pygame
from Level_Buffs import (
    LevelSpeedBuff,
    LevelDamageBuff,
    LevelAttackSpeedBuff,
    LevelAttackRangeBuff,
    LevelHealthBuff
)

class BuffManager:

    def __init__(self):

        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 60)

        self.available_buffs = [
            LevelHealthBuff(),
            LevelSpeedBuff(),
            LevelDamageBuff(),
            LevelAttackSpeedBuff(),
            LevelAttackRangeBuff()
        ]

        self.current_choices = []
        self.active = False

    def generate_choices(self):

        self.current_choices = random.sample(self.available_buffs, 2)
        self.active = True

    def apply_buff(self, index, robot, health):

        selected_buff = self.current_choices[index]
        selected_buff.apply_to(robot, health)

        self.active = False
        self.current_choices = []

    def draw(self, screen):

        if not self.active:
            return

        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = self.big_font.render(
            "LEVEL UP!",
            True,
            (255, 255, 255)
        )

        option1 = self.font.render(
            f"1 - {self.current_choices[0].name}",
            True,
            (255, 255, 255)
        )

        option2 = self.font.render(
            f"2 - {self.current_choices[1].name}",
            True,
            (255, 255, 255)
        )
        screen.blit(title, (350, 300))
        screen.blit(option1, (350, 400))
        screen.blit(option2, (350, 450))

