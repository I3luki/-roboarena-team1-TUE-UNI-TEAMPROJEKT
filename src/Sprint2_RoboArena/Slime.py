from Enemy import Enemy
import math
from Status_Effects import Slow_DebuffPlayer



class Slime(Enemy):

    def __init__(self, arena, x, y, wave):
        health= 150 + wave * 30
        super().__init__(
            arena,
            x,
            y,
            health,
            0
        )
        self.color = (0, 200, 255)
        self.speed = 0.5
        self.slow_cooldown = 0
        self.slow_cooldown_max = 120

        self.damage_radius = 70 + 2 * wave
    def check_damage_player(self, robot, health):

        if self.slow_cooldown > 0:
            self.slow_cooldown -= 1
            return

        dx = robot.x - self.x
        dy = robot.y - self.y
        distance = math.hypot(dx, dy)

        if distance < self.damage_radius:
            robot.add_status_effect(Slow_DebuffPlayer(5*60, 0.5))
            self.slow_cooldown = self.slow_cooldown_max