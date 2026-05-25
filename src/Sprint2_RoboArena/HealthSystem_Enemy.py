import pygame


class HealthSystem_Enemy:
    def __init__(self, max_health=100):
        self.max_health = max_health
        self.current_health = max_health
        self.bar_width = 40
        self.bar_height = 6
        self.color_bg = (60, 60, 60)
        self.color_health = (0, 200, 80)
        self.color_low = (200, 50, 50)
        self.color_border = (255, 255, 255)

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def is_dead(self):
        return self.current_health <= 0

    def health_ratio(self):
        return self.current_health / self.max_health

    def draw(self, screen, x_screen, y_screen):
        bar_x = x_screen - self.bar_width // 2
        bar_y = y_screen - 35  # über dem Gegner (radius=20 + 15px Abstand)

        pygame.draw.rect(screen, self.color_bg, (bar_x, bar_y, self.bar_width, self.bar_height))

        fill_width = int(self.bar_width * self.health_ratio())
        color = self.color_low if self.health_ratio() < 0.3 else self.color_health
        if fill_width > 0:
            pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, self.bar_height))

        pygame.draw.rect(screen, self.color_border, (bar_x, bar_y, self.bar_width, self.bar_height), 1)
