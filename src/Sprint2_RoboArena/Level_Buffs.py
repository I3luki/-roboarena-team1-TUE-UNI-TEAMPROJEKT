from Relics import Ice, Ricochet

# Frames per second
SECOND = 60 
# Rarities and corresponding probabilites
COMMON = 0.55
RARE = 0.3
EPIC = 0.15




class LevelSpeedBuff:

    amount = 0.5
    name = "Mehr Geschwindigkeit"
    description = "+" + str(amount) + " base-speed"
    flavor_text = "Vroom Vroom Vroom!"
    rarity = COMMON

    def apply_to(self, robot, health):
        robot.speed_base += self.amount
        robot.speed_current += self.amount
        print(f"Buff gewählt: {self.name}")


class LevelDamageBuff:

    amount = 5

    name = "Mehr Schaden"
    description = "+" + str(amount) + " attack"
    flavor_text = "Gewalt ist auch eine Lösung."
    rarity = COMMON

    def apply_to(self, robot, health):
        robot.attack_damage += self.amount
        print(f"Buff gewählt: {self.name}")


class LevelAttackSpeedBuff:

    amount = 60

    name = "Mehr Angriffsgeschwindigkeit"
    description = "-" + str(amount/SECOND) + "s attack-cooldown"
    flavor_text = "Swipe that thing."
    rarity = COMMON


    def apply_to(self, robot, health):
        robot.attack_cooldown -= self.amount

        # if min_limit attack_speed, set to under limit
        if robot.attack_cooldown < 200:
            robot.attack_cooldown = 200
        print(f"Buff gewählt: {self.name}")


class LevelAttackRangeBuff:

    amount = 50

    name = "Mehr Angriffsreichweite"
    description = "+" + str(amount) + " attack range"
    flavor_text = "Reach for the stars, my child."
    rarity = COMMON

    def apply_to(self, robot, health):
        robot.attack_radius += self.amount
        print(f"Buff gewählt: {self.name}")


class LevelHealthBuff:

    amount = 100

    name = "Mehr Leben"
    description = "+" + str(amount) + " max health"
    flavor_text = "You getting fat."
    rarity = COMMON

    def apply_to(self, robot, health):
        health.max_health += self.amount
        health.current_health += self.amount/4

        print(f"Buff gewählt: {self.name} | "
        f"Current HP: {health.current_health} | "
        f"Max HP: {health.max_health}")



class LevelIceRelic:

    name = "Skadi's Blessing"
    description = "Your attacks slows the enemies on-hit."
    flavor_text = "May Skadi protect you."
    rarity = RARE

    def apply_to(self, robot, health):
        relic = Ice(robot)
        robot.relics.list.append(relic)


class LevelRicochetRelic:

    name = "A Pile of Ricochets."
    description = "Send Ricochets to the nearest few enemies hit."
    flavor_text = "Where do you intend to store all of those?"
    rarity = EPIC

    def apply_to(self, robot, health):
        relic = Ricochet(robot)
        robot.relics.list.append(relic)
