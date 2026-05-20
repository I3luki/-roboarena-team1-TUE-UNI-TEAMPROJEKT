import pygame

class StaminaSystem:
    def __init__(self, screen, max_stamina=100, bar_x=10, bar_y=40, bar_width=400, bar_height=30):
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.bar_x = bar_x
        self.bar_y = bar_y
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.screen = screen

        self.color_bg     = (60, 60, 60)
        self.color_stamina = (255, 255, 0)
        self.color_border = (255, 255, 255)

    def use_stamina(self, amount):
        self.current_stamina = max(0, self.current_stamina - amount)

    def add_stamina(self, amount):
        self.current_stamina = min(0, self.current_stamina + amount)

    def stamina_ratio(self):
        return self.current_stamina / self.max_stamina

    def draw(self):
        # Hintergrund
        pygame.draw.rect(self.screen, self.color_bg,(self.bar_x, self.bar_y, self.bar_width, self.bar_height))

        # Füllstand der Staminaleiste
        fill_width = int(self.bar_width * self.stamina_ratio())
        color = self.color_stamina
        if fill_width > 0:
            pygame.draw.rect(self.screen, color,(self.bar_x, self.bar_y, fill_width, self.bar_height))

        # Rand
        pygame.draw.rect(self.screen, self.color_border,(self.bar_x, self.bar_y, self.bar_width, self.bar_height), 2)