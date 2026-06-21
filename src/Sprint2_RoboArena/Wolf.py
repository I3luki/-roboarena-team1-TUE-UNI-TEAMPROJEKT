from Enemy import Enemy
from Collision import AABB
import math


class Wolf(Enemy):

    def __init__(self, arena, x, y, wave):

        health = 200 + wave * 20
        damage = 3 + wave * 0.7

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
        self.dash_range = 225          # Spieler muss näher als 250 Pixel sein
        self.dash_distance = 200       # wie weit der Wolf nach vorne springt
        self.dash_cooldown = 4*60       # Frames Cooldown, ca. 5 Sekunden bei 60 FPS
        self.dash_timer = 0
        self.charge_time = 60* 0.3      #Wie viele Sekuden vorbereitung
        self.charge_timer = 0
        self.is_charging = False

        self.dash_direction_x = 0
        self.dash_direction_y = 0

    def start_charging(self, robot):
        dx = robot.x - self.x
        dy = robot.y - self.y

        distance = math.hypot(dx, dy)

        if distance == 0:
            return

        self.dash_direction_x = dx / distance
        self.dash_direction_y = dy / distance

        self.is_charging = True
        self.charge_timer = self.charge_time

        # Verändert farbe als vorwarnung^^
        self.color = (180, 180, 180)


    def dash_attack(self):
        self.x += self.dash_direction_x * self.dash_distance
        self.y += self.dash_direction_y * self.dash_distance

        self.aabb = AABB(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )

        self.is_charging = False
        self.charge_timer = 0
        self.dash_timer = self.dash_cooldown

        # Farbe wieder gleich
        self.color = (120, 120, 120)

    def update(self, robot, budget_available):
        dx = robot.x - self.x
        dy = robot.y - self.y
        distance = math.hypot(dx, dy)


        if self.dash_timer > 0:
            self.dash_timer -= 1


        if self.is_charging:
            self.charge_timer -= 1

            # Während des Aufladens bewegt er sich nicht normal weiter zeigt also dash an
            if self.charge_timer <= 0:
                self.dash_attack()

            return budget_available

        # Dash starten, wenn Spieler nah genug und Cooldown auf 0
        if distance <= self.dash_range and self.dash_timer <= 0:
            self.start_charging(robot)
            return budget_available

        # Normale Bewegung nur, wenn nicht gecharged wird
        return super().update(robot, budget_available)