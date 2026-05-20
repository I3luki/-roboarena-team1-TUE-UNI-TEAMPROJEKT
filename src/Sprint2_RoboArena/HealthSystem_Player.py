import pygame

class HealthSystem_Player:
    def __init__(self, screen, max_health=100, bar_x=10, bar_y=10, bar_width=400, bar_height=30):
        self.max_health = max_health
        self.current_health = max_health
        self.bar_x = bar_x
        self.bar_y = bar_y
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.screen = screen

        self.color_bg     = (60, 60, 60)
        self.color_health = (0, 200, 80)
        self.color_low    = (200, 50, 50)
        self.color_border = (255, 255, 255)

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def is_dead(self):
        return self.current_health <= 0

    def health_ratio(self):
        return self.current_health / self.max_health

    def draw(self):
        # Hintergrund
        pygame.draw.rect(self.screen, self.color_bg,(self.bar_x, self.bar_y, self.bar_width, self.bar_height))

        # Füllstand der Lebensleiste
        fill_width = int(self.bar_width * self.health_ratio())
        color = self.color_low if self.health_ratio() < 0.3 else self.color_health
        if fill_width > 0:
            pygame.draw.rect(self.screen, color,(self.bar_x, self.bar_y, fill_width, self.bar_height))

        # Rand
        pygame.draw.rect(self.screen, self.color_border,(self.bar_x, self.bar_y, self.bar_width, self.bar_height), 2)