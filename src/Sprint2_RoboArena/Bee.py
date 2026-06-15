from Enemy import Enemy
import math
from Status_Effects import Poison_Debuff

class Bee(Enemy):

    def __init__(self, arena, x, y,wave):
        health= 50 + wave * 10
        damage = 10 + wave * 10
        super().__init__(
            arena,
            x,
            y,
            health,
            damage
        )

        self.speed = 2
        self.damage_radius = 30
        self.color = (255, 255, 0)
        self.attack_cooldown_max = 120
        self.attack_cooldown = 0

    def update(self, robot, budget_available):

        dx = robot.x - self.x
        dy = robot.y - self.y

        distance = math.hypot(dx, dy)

        if distance > 0:

            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

        self.aabb.update(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )

        return False

    def check_damage_player(self, robot, health):

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return

        dx = robot.x - self.x
        dy = robot.y - self.y
        distance = math.hypot(dx, dy)


        if distance < self.damage_radius:

            robot.add_status_effect(
                Poison_Debuff(3*60,0.5)
            )
            self.attack_cooldown = self.attack_cooldown_max