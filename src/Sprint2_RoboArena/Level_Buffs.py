from Relics import Ice, Ricochet, Jingu_Bang, Swordmaster_Manual, Hermes_Shoe, Devil_Contract_I, Devil_Contract_II
from Status_Effects import Poison_Debuff


# Frames per second
SECOND = 60 
# Rarities and corresponding probabilites
COMMON = 0.85
RARE = 0.10
EPIC = 0.05




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

    key = "ice_relic"
    shop_locked = True
    cost = 20
    name = "Skadi's Blessing"
    description = "Your attacks slows the enemies on-hit."
    flavor_text = "May Skadi protect you."
    rarity = RARE

    def apply_to(self, robot, health):
        relic = Ice(robot)
        robot.relics.add(relic)


class LevelRicochetRelic:

    key = "ricochet_relic"
    shop_locked = True
    cost = 50
    name = "A Pile of Ricochets."
    description = "Send Ricochets to the nearest few enemies hit."
    flavor_text = "Where do you intend to store all of those?"
    rarity = EPIC

    def apply_to(self, robot, health):
        relic = Ricochet(robot)
        robot.relics.add(relic)


class LevelJinguBangRelic:

    key = "jingu_relic"
    shop_locked = True
    cost = 30
    name = "Fragment of Jingu Bang"
    decription = "Grow your sword temporarily on successfull attack."
    flavor_text = "Size matters."
    rarity = RARE

    def apply_to(self, robot, health):
        relic = Jingu_Bang(robot)
        robot.relics.add(relic)


class LevelSwordmasterManualRelic:

    key = "swordmaster_relic"
    shop_locked = True
    cost = 60
    name = "Manual of a forgotten Swordmaster"
    description = "Every 4th attack the next 3 attacks gain x2 attack-speed."
    flavor_text = "More Hits equals More ouch!  ~Sun Tzu"
    rarity = EPIC

    def apply_to(self, robot, health):
        relic = Swordmaster_Manual(robot)
        robot.relics.add(relic)


class LevelHermesShoe:

    key = "hermes_relic"
    shop_locked = True
    cost = 40
    name = "Shoe of Hermes"
    description = "Gain a short Movementspeed Buff on succesfull attack"
    flavor_text = "It fits. Am i the Princess now?"
    rarity = RARE

    def apply_to(self, robot, health):
        relic = Swordmaster_Manual(robot)
        robot.relics.add(relic)


class LevelDevilContractI:

    key = "devil_I_relic"
    shop_locked = True
    cost = 40
    name = "Devil's Contract I"
    description = "1.7xDMG\n 0.5xRange\n 0.7xMaxHealth\n heal full now"
    flavor_text = "Is it worth it?"
    rarity = RARE

    def apply_to(self, robot, health):
        robot.attack_damage *= 1.7
        robot.attack_radius *= 0.5
        health.max_health *= 0.7
        health.current_health = health.max_health
        relic = Devil_Contract_I(robot)
        robot.relics.add(relic)


class LevelDevilContractII:

    key = "devil_II_relic"
    shop_locked = True
    cost = 70
    name = "Devil's Contract II"
    description = "1.7xDMG\n 0.8xMaxHealth\n get permanantly poisoned\n heal on hit based on missing health\n heal full now\n"
    flavor_text = "YOLO."
    rarity = RARE

    def apply_to(self, robot, health):
        robot.attack_damage *= 1.7
        health.max_health *= 0.8
        health.current_health = health.max_health
        poison = Poison_Debuff(permanent=True)
        robot.status_effects.append(poison)
        relic = Devil_Contract_II(robot)
        robot.relics.add(relic)






# Class to give out all the LevelBuffs easy and centralised
class LevelBuffs:

    # all LevelBuffs
    all = [
        LevelSpeedBuff(),
        LevelDamageBuff(),
        LevelAttackSpeedBuff(),
        LevelAttackRangeBuff(),
        LevelHealthBuff(),
        LevelIceRelic(),
        LevelRicochetRelic(),
        LevelJinguBangRelic(),
        LevelSwordmasterManualRelic(),
        LevelHermesShoe(),
        LevelDevilContractI(),
        LevelDevilContractII()
    ]

    # all ShopLocked LevelBuffs
    all_shop = [item for item in all if getattr(item, "shop_locked", False)]