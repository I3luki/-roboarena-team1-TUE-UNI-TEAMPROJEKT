from Relics import Ice, Ricochet, Jingu_Bang, Swordmaster_Manual, Hermes_Shoe, Devil_Contract_I, Devil_Contract_II
from Status_Effects import Poison_Debuff
from Textures import Textures


# Frames per second
SECOND = 60 
# Rarities and corresponding probabilites
COMMON = 0.85
RARE = 0.10
EPIC = 0.05




class LevelSpeedBuff:

    amount = 0.35
    name = "Mehr Geschwindigkeit"
    description = "+" + str(amount) + " base-speed"
    flavor_text = "Vroom Vroom Vroom!"
    rarity = COMMON

    def apply_to(self, robot, health):
        robot.speed_base += self.amount
        robot.speed_current += self.amount
        print(f"Buff gewählt: {self.name}")

    def get_icon(self):
        return Textures.STAT_ICON_SPEED
    

class LevelDamageBuff:

    amount = 5

    name = "Mehr Schaden"
    description = "+" + str(amount) + " attack"
    flavor_text = "Gewalt ist auch eine Lösung."
    rarity = COMMON

    def apply_to(self, robot, health):
        robot.attack_damage += self.amount
        print(f"Buff gewählt: {self.name}")

    def get_icon(self):
        return Textures.STAT_ICON_ATTACK


class LevelAttackSpeedBuff:

    amount = 45

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

    def get_icon(self):
        return Textures.STAT_ICON_AS


class LevelAttackRangeBuff:

    amount = 25

    name = "Mehr Angriffsreichweite"
    description = "+" + str(amount) + " attack range"
    flavor_text = "Reach for the stars, my child."
    rarity = COMMON

    def apply_to(self, robot, health):
        robot.attack_radius += self.amount
        print(f"Buff gewählt: {self.name}")

    def get_icon(self):
        return Textures.STAT_ICON_RANGE


class LevelHealthBuff:

    amount = 50

    name = "Mehr Leben"
    description = "+" + str(amount) + " max health"
    flavor_text = "You getting fat."
    rarity = COMMON

    def apply_to(self, robot, health):
        health.max_health += self.amount
        health.current_health += self.amount

        if health.current_health > health.max_health:
            health.current_health = health.max_health

        print(f"Buff gewählt: {self.name} | "
        f"Current HP: {health.current_health} | "
        f"Max HP: {health.max_health}")

    def get_icon(self):
        return Textures.STAT_ICON_HEALTH



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

    def get_icon(self):
        return Ice(7).get_icon()


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
    
    def get_icon(self):
        return Ricochet(7).get_icon()


class LevelJinguBangRelic:

    key = "jingu_relic"
    shop_locked = True
    cost = 30
    name = "Fragment of Jingu Bang"
    description = "Grow your sword temporarily on successfull attack."
    flavor_text = "Size matters."
    rarity = RARE

    def apply_to(self, robot, health):
        relic = Jingu_Bang(robot)
        robot.relics.add(relic)

    def get_icon(self):
        return Jingu_Bang(7).get_icon()

    


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

    def get_icon(self):
        return Swordmaster_Manual(7).get_icon()


class LevelHermesShoe:

    key = "hermes_relic"
    shop_locked = True
    cost = 40
    name = "Shoe of Hermes"
    description = "Gain a short Movementspeed Buff on succesfull attack"
    flavor_text = "It fits. Am i the Princess now?"
    rarity = RARE

    def apply_to(self, robot, health):
        relic = Hermes_Shoe(robot)
        robot.relics.add(relic)
    
    def get_icon(self):
        return Hermes_Shoe(7).get_icon()


class LevelDevilContractI:

    attack_multiplier = 1.5
    radius_multiplier = 0.7
    maxhealth_multiplier = 0.75

    key = "devil_I_relic"
    shop_locked = True
    cost = 40
    name = "Devil's Contract I"
    description = f"-> {attack_multiplier}x DMG\n-> {radius_multiplier}x Range\n-> {maxhealth_multiplier}x MaxHealth\n-> heal full now"
    flavor_text = "Is it worth it?"
    rarity = RARE

    def apply_to(self, robot, health):
        robot.attack_damage *= self.attack_multiplier
        robot.attack_radius *= self.radius_multiplier
        health.max_health *= self.maxhealth_multiplier
        health.current_health = health.max_health
        relic = Devil_Contract_I(robot)
        robot.relics.add(relic)

    def get_icon(self):
        return Devil_Contract_I(7).get_icon()


class LevelDevilContractII:

    attack_multiplier = 1.6
    maxhealth_multiplier = 0.85

    key = "devil_II_relic"
    shop_locked = True
    cost = 70
    name = "Devil's Contract II"
    description = f"-> {attack_multiplier}x DMG\n-> {maxhealth_multiplier}x MaxHealth\n-> get permanantly poisoned\n-> heal on hit based on missing health\n-> heal full now\n"
    flavor_text = "YOLO."
    rarity = RARE

    def apply_to(self, robot, health):
        robot.attack_damage *= self.attack_multiplier
        health.max_health *= self.maxhealth_multiplier
        health.current_health = health.max_health
        poison = Poison_Debuff(permanent=True)
        robot.status_effects.append(poison)
        relic = Devil_Contract_II(robot)
        robot.relics.add(relic)

    def get_icon(self):
        return Devil_Contract_II(7).get_icon()






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