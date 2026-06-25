import pygame
from Status_Effects import Slow_Debuff, Ricochet_Debuff, Relic_RangeBuff, Swordmaster_AttackspeedBuff, Speed_Buff


ICON_WIDTH = 40
ICON_HEIGHT = 40

SECOND = 60


class Relics:

    def __init__(self, robot, arena):
        self.robot = robot
        self.screen = arena.screen
        self.list = []   #list of all the current relics

    def add(self, relic):
        self.list.append(relic)

    def on_hit(self, enemy, enemies):
        for relic in self.list:
            if hasattr(relic, "on_hit"):
                relic.on_hit(enemy, enemies)

    def on_attack(self, enemies):
        print("relic on attack called")  #TODO: DELETE
        for relic in self.list:
            if hasattr(relic, "on_attack"):
                relic.on_attack(enemies)
        
    def draw_icons(self):
        # Definiere Position der Icons
        icon_bar = pygame.Surface((ICON_WIDTH*7, ICON_HEIGHT), pygame.SRCALPHA)
        icon_bar.fill((0,0,0,0))
        icon_bar_pos = (30, 120)
        index = 0
        space = int(ICON_WIDTH / 4)  # abstand zwischen icons

        # Zeichne die relic Icons auf die Icon-Bar
        for relic in self.list:
            icon_bar.blit(relic.get_icon(), (index*(ICON_WIDTH+space), 0))
            index += 1

        # Zeichne die Icon-Bar auf den Screen
        self.screen.blit(icon_bar, icon_bar_pos)


    # updates every on-hit-cooldown relic
    def update_on_hit(self):
        for relic in self.list:
            if hasattr(relic, "update_on_hit"):
                relic.update_on_hit()
            
    # updates every on-attack-cooldown
    def update_on_attack(self):
        for relic in self.list:
            if hasattr(relic, "update_on_attack"):
                relic.update_on_attack()






# Ricochet: "extra damage jumps to multiple enemies"
#       Type: on-hit
class Ricochet:

    def __init__(self, robot):
        self.robot = robot
        self.cooldown = 1    # every 7th enemy hit    #TODO: change to 7, maybe 
        self.count = self.cooldown


    def on_hit(self, enemy, enemies):
        # Tesla-Effekt aktivieren
        if(self.count <= 0):
            enemy.status_effects.append(Ricochet_Debuff(self.robot, enemies))
            self.count = self.cooldown

    def update_on_hit(self):
        self.count -= 1
        

    def get_icon(self):
        surf = pygame.Surface((ICON_WIDTH,ICON_HEIGHT))
        surf.fill((0,0,255))     # blau
        return surf
    
    


# Ice: "slows enemies on every 4th hit"
class Ice:

    def __init__(self, robot):
        self.robot = robot
        self.cooldown = 1   # every attack
        self.count = self.cooldown
        self.damage = 0.5
        self.slow = 0.5     # takes speed to 0.6 of current

    def on_hit(self, enemy, enemies):
        # gebe getroffenem Gegner Ice-Debuff
        if(self.count <= 0):
            print('on-hit ice applied') # TODO: delete after testing
            enemy.status_effects.append(Slow_Debuff(self.robot))
            


    def update_on_attack(self):
        print("Ice count updated on attack")#TODO: delete after testing
        if(self.count <= 0):
            self.count = self.cooldown

        self.count -= 1


    def get_icon(self):
        surf = pygame.Surface((ICON_WIDTH,ICON_HEIGHT))
        surf.fill(((173, 216, 230)))   # hellblau
        return surf   
    


# Jingu_Bang: "adds temporary attack-range on successfull attack"
class Jingu_Bang:

    def __init__(self, robot):
        self.robot = robot
        self.cooldown = 1   # every attack
        self.count = self.cooldown

    def on_hit(self, enemy, enemies):
        # gebe Spieler range Buff
        print("jingu hit detected")
        if(self.count <= 0):
            self.count = self.cooldown   # prox max 1 time per attack
            print('jingu on-hit triggered') # TODO: delete after testing
            # wenn der status effekt schon teil von spieler, erneuere durch repeat
            for effect in self.robot.status_effects:
                if isinstance(effect, Relic_RangeBuff):
                    effect.repeat(self.robot)
                    return
            # wenn status effekt noch nicht teil von spieler ist
            self.robot.status_effects.append(Relic_RangeBuff())
            

    def update_on_attack(self):
        if(self.count <= 0):
            self.count = self.cooldown
        self.count -= 1
        print("attack-range: " + str(self.robot.attack_radius))


    def get_icon(self):
        surf = pygame.Surface((ICON_WIDTH,ICON_HEIGHT))
        surf.fill(((255, 165, 0)))   # orange
        return surf  
     
    
# Swordmaster_Manual: "every a-th attack gain x attackspeed for b attacks"
class Swordmaster_Manual:

    def __init__(self, robot):
        self.robot = robot
        self.a = 4      #every a-th attack get buff
        self.b = 2      #for b-th attacks
        self.cooldown = self.a + self.b   # every (a+b)th attack apply
        self.count = self.a


    def on_attack(self, enemies):
        # gebe Spieler attack-speed Buff
        if(self.count <= 0):
            print('swordmaster xth on-attack triggered') # TODO: delete after testing
            # wenn der status effekt schon teil von spieler, erneuere durch repeat
            self.robot.status_effects.append(Swordmaster_AttackspeedBuff(self.b))
        # decrease the buff on each attack
        if (self.count <= self.a):
            for effect in self.robot.status_effects:
                if isinstance(effect, Swordmaster_AttackspeedBuff):
                    effect.decrease()

    def update_on_attack(self):
        if(self.count <= 0):
            self.count = self.cooldown
        self.count -= 1

    def get_icon(self):
        surf = pygame.Surface((ICON_WIDTH,ICON_HEIGHT))
        surf.fill((245, 222, 179))   # pergament
        return surf   
    

# Hermes_Shoe: "adds temporary movementspeed on successfull attack"
class Hermes_Shoe():

    def __init__(self, robot):
        self.robot = robot
        self.cooldown = 1   # every attack
        self.count = self.cooldown

    def on_hit(self, enemy, enemies):
        # gebe Spieler movementspeed Buff
        if(self.count <= 0):
            self.count = self.cooldown   # prox max 1 time per attack
            print('hermes on-hit trigger') # TODO: delete after testing
            # wenn der status effekt schon teil vom spieler mit der gleichen quelle, erneuere durch renew
            for effect in self.robot.status_effects:
                if isinstance(effect, Speed_Buff):
                    if effect.source == "hermes":
                        effect.renew(self.robot)
                        return
            # wenn status effekt noch nicht teil von spieler ist
            self.robot.status_effects.append(Speed_Buff(ttl=int(0.2*SECOND), factor=1.3, source="hermes"))
            

    def update_on_attack(self):
        if(self.count <= 0):
            self.count = self.cooldown
        self.count -= 1


    def get_icon(self):
        surf = pygame.Surface((ICON_WIDTH,ICON_HEIGHT))
        surf.fill((192, 192, 192))   # silber
        return surf 
    

# Devil_Contract_I: "1.7xDMG, 0.5xRange, 0.7xMaxHealth"
class Devil_Contract_I:

    def __init__(self, robot):
        self.robot = robot

    def get_icon(self):
        surf = pygame.Surface((ICON_WIDTH,ICON_HEIGHT))
        surf.fill((180, 0, 0))   # red
        return surf 
    

# Devil_Contract_II: "1.7xDMG, 0.8xMaxHealth, get permanantly poisoned, heal on hit based on missing health, heal full now"
class Devil_Contract_II:

    def __init__(self, robot):
        self.robot = robot
        self.heal_factor = 0.1   #based on missing health
        self.cooldown = 1   # every attack heal
        self.count = self.cooldown

    def on_hit(self, enemy, enemies):
        # gebe Spieler Health on hit
        max_health = self.robot.health.max_health
        current_health = self.robot.health.current_health
        if(self.count <= 0):
            heal_amount = 0.1 * (max_health - current_health)   
            self.robot.health.current_health += heal_amount
            print("DC_II: healed for " + str(heal_amount))       #TODO: DELETE AFTER TESTING
            
    def update_on_attack(self):
        if(self.count <= 0):
            self.count = self.cooldown
        self.count -= 1

    def get_icon(self):
        surf = pygame.Surface((ICON_WIDTH,ICON_HEIGHT))
        surf.fill((100, 0, 0))   # dunkelrot
        return surf 
    
