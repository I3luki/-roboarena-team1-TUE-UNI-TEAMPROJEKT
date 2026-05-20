#import pygame


class HealthSystem_Enemy:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health

    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)

    def is_dead(self):
        return self.current_health <= 0
