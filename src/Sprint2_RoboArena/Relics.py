import pygame
from Status_Effects import Slow_Debuff, Ricochet_Debuff


ICON_WIDTH = 40
ICON_HEIGHT = 40


class Relics:

    def __init__(self, robot, arena):
        self.robot = robot
        self.screen = arena.screen
        self.list = []   #list of all the current relics

    def on_hit(self, enemy, enemies):
        for relic in self.list:
            if hasattr(relic, "on_hit"):
                relic.on_hit(enemy, enemies)
        
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