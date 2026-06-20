from Enemy import Enemy
from Collision import AABB
import math


class Wolf(Enemy):

    def __init__(self, arena, x, y, wave):

        health = 200 + wave * 20
        damage = 3 + wave * 3

        super().__init__(
            arena,
            x,
            y,
            health,
            damage
        )

        self.speed_base = 2.2
        self.speed_current = self.speed_base
        self.color = (120, 120, 120)

        # Dash-Einstellungen
        self.dash_range = 250          # Spieler muss näher als 250 Pixel sein
        self.dash_distance = 150       # wie weit der Wolf nach vorne springt
        self.dash_cooldown = 5*60       # Frames Cooldown, ca. 2 Sekunden bei 60 FPS
        self.dash_timer = 0

    def dash_attack(self, robot):
        dx = robot.x - self.x
        dy = robot.y - self.y

        distance = math.hypot(dx, dy)

        if distance == 0:
            return

        # Richtung zum Spieler normalisieren
        direction_x = dx / distance
        direction_y = dy / distance

        # Neue Position berechnen
        self.x += direction_x * self.dash_distance
        self.y += direction_y * self.dash_distance

        # AABB aktualisieren
        self.aabb = AABB(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )

        # Cooldown starten
        self.dash_timer = self.dash_cooldown

    def update(self, robot, budget_available):
        dx = robot.x - self.x
        dy = robot.y - self.y
        distance = math.hypot(dx, dy)

        # Cooldown runterzählen
        if self.dash_timer > 0:
            self.dash_timer -= 1

        # Dash benutzen, wenn Spieler nah genug ist und Dash bereit ist
        if distance <= self.dash_range and self.dash_timer <= 0:
            self.dash_attack(robot)

        return super().update(robot, budget_available)