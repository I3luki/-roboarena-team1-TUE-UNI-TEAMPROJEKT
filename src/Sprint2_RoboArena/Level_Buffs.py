class LevelSpeedBuff:

    name = "Mehr Geschwindigkeit"

    def apply_to(self, robot, health):
        robot.speed_base += 0.5
        robot.speed_current += 0.5
        print(f"Buff gewählt: {self.name}")


class LevelDamageBuff:

    name = "Mehr Schaden"

    def apply_to(self, robot, health):
        robot.attack_damage += 5
        print(f"Buff gewählt: {self.name}")


class LevelAttackSpeedBuff:

    name = "Mehr Angriffsgeschwindigkeit"

    def apply_to(self, robot, health):
        robot.attack_cooldown -= 100

        if robot.attack_cooldown < 200:
            robot.attack_cooldown = 200
        print(f"Buff gewählt: {self.name}")


class LevelAttackRangeBuff:

    name = "Mehr Angriffsreichweite"

    def apply_to(self, robot, health):
        robot.attack_radius += 50
        print(f"Buff gewählt: {self.name}")


class LevelHealthBuff:

    name = "Mehr Leben"

    def apply_to(self, robot, health):
        health.max_health += 100
        health.current_health += 20
        print(f"Buff gewählt: {self.name} | "
        f"Current HP: {health.current_health} | "
        f"Max HP: {health.max_health}")