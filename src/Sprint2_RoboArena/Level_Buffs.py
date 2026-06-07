class LevelSpeedBuff:

    name = "Mehr Geschwindigkeit"

    def apply_to(self, robot, health):
        robot.speed_base += 0.5
        robot.speed_current += 0.5


class LevelDamageBuff:

    name = "Mehr Schaden"

    def apply_to(self, robot, health):
        robot.attack_damage += 5


class LevelAttackSpeedBuff:

    name = "Mehr Angriffsgeschwindigkeit"

    def apply_to(self, robot, health):
        robot.attack_cooldown -= 100

        if robot.attack_cooldown < 200:
            robot.attack_cooldown = 200


class LevelAttackRangeBuff:

    name = "Mehr Angriffsreichweite"

    def apply_to(self, robot, health):
        robot.attack_radius += 50


class LevelHealthBuff:

    name = "Mehr Leben"

    def apply_to(self, robot, health):
        health.max_health += 100
        health.current_health += 20