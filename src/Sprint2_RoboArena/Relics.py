import pygame


ICON_WIDTH = 40
ICON_HEIGHT = 40


class Relics:

    def __init__(self, robot, arena ):
        self.robot = robot
        self.screen = arena.screen
        self.list = []   #list of all the current relics

    def on_hit(self, enemy):
        for relic in self.list:
            if hasattr(relic, "on_hit"):
                relic.on_hit(enemy)
        
    def draw_icons(self):
        # Definiere Position der Icons
        icon_bar = pygame.surface(ICON_WIDTH*7, ICON_HEIGHT, pygame.SRCALPHA)
        icon_bar.fill((0,0,0,0))
        icon_bar_pos = (50, 200)
        index = 0
        space = int(ICON_WIDTH / 4)  # abstand zwischen icons

        # Zeichne die relic Icons auf die Icon-Bar
        for relic in self.list:
            relic.get_icon().blit(icon_bar, index*(ICON_WIDTH+space))

        # Zeichne die Icon-Bar auf den Screen
        icon_bar.blit(self.screen, icon_bar_pos)

    # updates every on-hit-cooldown relic
    def update_on_hit(self):
        for relic in self.list:
            if hasattr(relic, "update_on_hit"):
                relic.update_on_hit()
            
    # updates every on-attack-cooldown
    def update_on_attack(self):
        for relic in self.list:
            if hasattr(relic, "update_on_hit"):
                relic.update_on_attack()






# Tesla: "extra damage jumps to multiple enemies"
#       Type: on-hit
class Tesla:

    def __init__(self, robot):
        self.robot = robot
        self.cooldown = 4    # every 4th hit  
        self.count = self.cooldown
        self.damage = 3
        self.jumps = 5
        self.range = 100

    def on_hit(self, enemy):
        # Tesla-Effekt aktivieren
        if(self.count <= 0):
            # TODO: do smth
            self.count = self.cooldown

    def update_on_hit(self):
        self.count -= 1
        

    def get_icon(self):
        surf = pygame.surface(ICON_WIDTH,ICON_HEIGHT)
        surf.fill((0,0,255))     # blau
        return surf
    
    


# Ice: "slows enemies on every 4th hit"
class Ice:

    def __init__(self):
        self.cooldown = 3   # every 3rd attack
        self.count = self.cooldown
        self.damage = 0.5
        self.slow = 0.7

    def on_hit(self, robot, enemy):
        # Ice Effekt aktivieren
        if(self.count <= 0):
            # TODO: do smth
            self.count = self.cooldown


    def update_on_attack():
        count -= 1

    def get_icon(self):
        surf = pygame.surface(ICON_WIDTH,ICON_HEIGHT)
        surf.fill(((173, 216, 230)))   # hellblau
        return surf   