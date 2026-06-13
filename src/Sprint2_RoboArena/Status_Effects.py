import pygame

SECOND = 60   # because 60FPS at the Moment







# -------------------------------------------------------- Allgemeine Klassen und Methoden ----------------- 
class Effect:

    ICON_WIDTH = 20
    ICON_HEIGHT = 20
    ICON_DURATION_COLOR = (0,0,0)  # (schwarz) Farbe des icon-overlays für duration

    def __init__(self):
        self.ttl_max = 0
        self.ttl_current = 0

    # applies an effect to the given robot
    #       handles TTL and buff reversion
    def apply_to(self, robot):
        pass

    # sets the ttl to 0
    def undo(self):
        self.ttl_current = 0

    # draws a corresponding Icon at the given location
    def draw(self,x,y):
        pass

    def get_icon_overlay(self):
        duration_fraction = 1 - (self.ttl_current / self.ttl_max)
        width = duration_fraction * self.ICON_WIDTH
        return make_icon_overlay(width, self.ICON_HEIGHT, self.ICON_DURATION_COLOR)
        


# Allgemeine Klasse für Effekt die periodisch ausgelöst werden
class Tick_Effect(Effect):
    
    # example init
    def __init__(self):
        self.ttl_max = 1 * SECOND
        self.ttl_current = self.ttl_max
        self.effect_amount = 1                   
        self.tick_rate = int(0.25 * SECOND)
        

    # applies the effect to the robot, has to be implemented
    def apply_to(self, robot):
        pass


# Zeichnet ein Surface mit einem gegebenen Text
def make_icon(width, height, color, text):
    # Create colored surface
    surface = pygame.Surface((width, height))
    surface.fill(color)  
    # Create text surface
    font = pygame.font.Font(None, 10)  
    text = font.render(text, True, (0, 0, 0))  # black tex
    # Center text on button
    text_rect = text.get_rect(center=(width/2, height/2))
    surface.blit(text, text_rect)

    return surface

# Zeichnet eine halbdurchsichtiges Rechteck, Größe abhängig von TTL-fraction
def make_icon_overlay(width, height, color):
    surface = pygame.Surface((width, height))
    surface.set_alpha(128)  # 0 = unsichtbar, 255 = voll sichtbar
    surface.fill(color) 

    return surface


# ------------------------------------------------------------------------------------------------------


# 01 Speed Buff
class Speed_Buff(Effect):

    SPEED_SLOWDOWN = 1 * SECOND

    def __init__(self):
        self.ttl_max = 7 * SECOND
        self.ttl_current = self.ttl_max
        self.in_use = False        
        self.speed_factor = 2.5
        self.speed_buff = 0   # initiation in apply_to()
        self.slow_rate = 0    # initiation in apply_to()


    # applies the speed buff
    def apply_to(self, robot):

        # Initial Application of the Buff
        if(not self.in_use):
            # compute buff
            self.speed_buff = robot.speed_base * self.speed_factor
            self.slow_rate = self.speed_buff / self.SPEED_SLOWDOWN

            # apply buff on Initiation
            if(self.ttl_current > 0):
                robot.speed_current += self.speed_buff
                self.in_use = True 
                return
            else:
                return        
            
        # Revert Buff on TTL=0
        if(self.ttl_current <= 0 and self.in_use):
            robot.speed_current -= self.speed_buff

        # start to gradually slow down
        if(self.ttl_current < self.SPEED_SLOWDOWN and self.in_use):
            self.speed_buff -= self.slow_rate
            robot.speed_current -= self.slow_rate


        # Tick down Time-to-Live
        self.ttl_current -= 1

    def get_icon(self):
        color = (255,255,0)  # gelb
        return make_icon(self.ICON_WIDTH, self.ICON_HEIGHT, color, "speed")
    

    
# Slow_Debuff:  "Slows entity based on base_speed"
class Slow_Debuff(Effect):

    SLOW_TIME = 2*SECOND

    def __init__(self):
        self.ttl_max = self.SLOW_TIME
        self.ttl_current = self.ttl_max
        self.slow_debuff = 0  # initiated in apply_to()
        self.slow_factor = 0.3


    # applies the slow debuff
    def apply_to(self, robot):

        # Initial Application of the Buff
        if(not self.in_use):
            # compute buff
            self.slow_debuff = robot.speed_base * self.slow_factor
            # self.slow_rate = self.speed_buff / self.SPEED_SLOWDOWN

            # apply buff on Initiation
            if(self.ttl_current > 0):
                robot.speed_current -= self.slow_debuff
                self.in_use = True 
                return
            else:
                return        
            
        # Revert Buff on TTL=0
        if(self.ttl_current <= 0 and self.in_use):
            robot.speed_current += self.slow_debuff

        # Tick down Time-to-Live
        self.ttl_current -= 1

    def get_icon(self):
        color = (173, 216, 230)  # hellblau
        return make_icon(self.ICON_WIDTH, self.ICON_HEIGHT, color, "slow")


# Health-Regernaration-Buff
class Healthgen_Buff(Tick_Effect):

    def __init__(self):
        self.ttl_max = 5 * SECOND
        self.ttl_current = self.ttl_max
        self.effect_amount = 0.7                   
        self.tick_rate = int(0.25 * SECOND)
        

    def apply_to(self, robot):
        current_health = robot.health.current_health
        max_health = robot.health.max_health

        # if not full HP and is on tick
        if(current_health < max_health and
           self.ttl_current % self.tick_rate == 0):
            
            # prevent overhealing
            if(current_health+self.effect_amount > max_health):
                robot.health.current_health = robot.health.max_health
            else:
                robot.health.current_health += self.effect_amount

        # update TTL
        self.ttl_current -= 1

    def get_icon(self):
            color = (255, 192, 203)  # pink
            return make_icon(self.ICON_WIDTH, self.ICON_HEIGHT, color, "heal")


# Poison-Debuff
class Poison_Debuff(Tick_Effect):

    def __init__(self):
        self.ttl_max = 5 * SECOND
        self.ttl_current = self.ttl_max
        self.effect_amount = 0.2                   
        self.tick_rate = int(0.1 * SECOND)


    def apply_to(self, robot):
        # on-tick do dmg
        if(self.ttl_current % self.tick_rate == 0):
            robot.health.take_damage(self.effect_amount)
        
        # update TTL
        self.ttl_current -= 1

    def get_icon(self):
        color = (128, 0, 128)  # lila
        return make_icon(self.ICON_WIDTH, self.ICON_HEIGHT, color, "poison")



        
            

        

