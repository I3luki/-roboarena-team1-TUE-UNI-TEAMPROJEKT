import pygame
import math
import random
from Textures import Textures

SECOND = 60   # because 60FPS at the Moment

# -------------------------------------------------------- Allgemeine Klassen und Methoden ----------------- 
class Effect:

    ICON_WIDTH = 30
    ICON_HEIGHT = 30
    ICON_DURATION_COLOR = (80,80,80)  # (schwarz) Farbe des icon-overlays für duration

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



# Zeichnet eine halbdurchsichtiges Rechteck, Größe abhängig von TTL-fraction
def make_icon_overlay(width, height, color):
    surface = pygame.Surface((width, height))
    surface.set_alpha(128)  # 0 = unsichtbar, 255 = voll sichtbar
    surface.fill(color) 

    return surface







# ------------------------------------------------------------------------------------------------------








# Speed_Buff: "gives speed buff based on speed_base, slows down after a certain time"
class Speed_Buff(Effect):


    def __init__(self, ttl=4*SECOND, factor=0.4, source="tile"):
        self.source = source     #needed to not be able to hardstack speedbuff from hermes relic
        self.ttl_max = ttl
        self.ttl_current = self.ttl_max
        self.in_use = False        
        self.speed_factor = factor
        self.speed_buff = 0   # initiation in apply_to()
        self.slow_rate = 0    # initiation in apply_to()
        self.SPEED_SLOWDOWN = int(1.5 * SECOND)


    # applies the speed buff
    def apply_to(self, robot):
        print("current speed: "+str(robot.speed_current) )
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
            
        # Tick down Time-to-Live
        self.ttl_current -= 1
            
        # Revert Buff on TTL=0
        if(self.ttl_current <= 0 and self.in_use):
            robot.speed_current -= self.speed_buff
            self.speed_buff = 0

        # start to gradually slow down
        if(self.ttl_current <= self.SPEED_SLOWDOWN and self.in_use):
            if self.speed_buff<=0:
                return
            self.speed_buff -= self.slow_rate
            robot.speed_current -= self.slow_rate


    def renew(self):
        self.ttl_current = self.ttl_max

    def get_icon(self):
        return Textures.SPEED_ICON_STATUS
    


# Slow_Debuff:  "Slows entity based on base_speed"
class Slow_Debuff(Effect):

    SLOW_TIME = 1.5 * SECOND

    def __init__(self, robot):
        self.camera = robot.arena.camera
        self.screen = robot.arena.screen
        self.ttl_max = self.SLOW_TIME
        self.ttl_current = self.ttl_max
        self.slow_debuff = 0  # initiated in apply_to()
        self.slow_factor = 0.5
        self.in_use = False
        self.me = None   # current holder of the debuff


    # applies the slow debuff
    def apply_to(self, me):
        
        self.me = me

        # Initial Application of the Buff
        if(not self.in_use):
            # compute debuff
            self.slow_debuff = me.speed_base * self.slow_factor

            # apply buff on Initiation
            if(self.ttl_current > 0):
                me.speed_current -= self.slow_debuff
                self.in_use = True 
                return
            else:
                return        
            
        # Revert Buff on TTL=0
        if(self.ttl_current <= 0 and self.in_use):
            me.speed_current += self.slow_debuff

        # Tick down Time-to-Live
        self.ttl_current -= 1

    def get_icon(self):
        return Textures.SLOW_ICON_STATUS
    

    def draw(self):
        offset = 50

        x_screen, y_screen = self.camera.global_to_screen(self.me)
        x_screen -= offset
        y_screen -= offset

        # if self.me was already assigned
        if self.me:
            self.screen.blit(self.get_icon(), (x_screen, y_screen))




# Healthgen_Buff: "gives flat healthgeneration over fixed time"
class Healthgen_Buff(Tick_Effect):

    def __init__(self):
        self.ttl_max = 5 * SECOND
        self.ttl_current = self.ttl_max
        self.effect_amount = 2.0
        self.tick_rate = int(0.5 * SECOND)
        

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
            return Textures.HEALING_ICON_STATUS



# Poison-Debuff: "does flat tick-damage over time"
class Poison_Debuff(Tick_Effect):

    def __init__(self, duration=3*SECOND, dmg=1.5, permanent=False):
        self.ttl_max = duration
        self.ttl_current = duration
        self.effect_amount = dmg
        self.tick_rate = int(0.5 * SECOND)  # alle 0.5 Sekunden Schaden
        self.permanent = permanent

    def apply_to(self, robot):

        # nur auf Tick Schaden machen
        if self.ttl_current % self.tick_rate == 0:
            robot.health.take_damage(self.effect_amount)

        if not self.permanent:
            self.ttl_current -= 1

    def get_icon(self):
        return Textures.POISON_ICON_STATUS


# Ricochet_Debuff: "Sends a Ricochet to a random near enough enemy with damage based on robot damage"
class Ricochet_Debuff(Effect):

    def __init__(self, robot, enemies):
        self.robot = robot
        self.camera = robot.arena.camera
        self.screen = robot.arena.screen
        self.damage = robot.attack_damage * 0.5

        self.start = robot   # the start of the riccochet
        self.me = robot      # the current holder of the debuff
        self.x = robot.x     # position of the ricochet
        self.y = robot.y
        self.jumps = 3
        self.range = 250
        self.tick = int(SECOND/4)  # makes smth every tick
        self.enemies = enemies
        random.shuffle(self.enemies)
        self.enemies_copy = enemies.copy()
        
        self.ttl_max = self.jumps * self.tick + 1   # ttl is 0 when no jumps left
        self.ttl_current = self.ttl_max
        

    def apply_to(self, me):
        # update
        # (has to be done first to prevent instant proccing on the next enemy, maybe)
        self.ttl_current -= 1
        self.me = me   

        # when it is time to tick
        if(self.ttl_current % self.tick == 0):

            print("Riccochet tick") #TODO: delete after testing
            # delete self out of the enemies list, update start
            self.start = me
            self.enemies_copy.remove(me)

            # make damage
            me.health_system.current_health -= self.damage

            # jump to first close enough enemy
            x1 = me.aabb.x
            y1 = me.aabb.y
            for enemy in self.enemies_copy:
                x2 = enemy.aabb.x
                y2 = enemy.aabb.y
                # check distance
                distance = math.hypot(x2 - x1, y2 - y1)
                if(distance < self.range):
                    print("Ricochet: near enemy found!") #TODO: delete after testing
                    # add this debuff to the enemy, than remove this effect from me
                    enemy.status_effects.append(self)
                    me.status_effects.remove(self) 
                    return
                
            # if no target found, destroy this status effect
            self.ttl_current = -1
            print("Ricochet: no more near targets found") #TODO: delete after testing


    # draws a ricochet
    def draw(self):

        img_ricochet = pygame.Surface((20,20))
        img_ricochet.fill((0,0,0)) #black

        fraction = 1 - ((self.ttl_current % self.tick) / self.tick)
        direction = (self.me.x - self.start.x, self.me.y - self.start.y)

        self.x = self.start.aabb.x + (direction[0]*fraction)
        self.y = self.start.aabb.y + (direction[1]*fraction)

        x_screen, y_screen = self.camera.global_to_screen(self)

        self.screen.blit(img_ricochet, (x_screen, y_screen))




class Slow_DebuffPlayer(Effect):

    def __init__(self, duration=0.3*SECOND, factor=0.25):
        self.ttl_max = duration
        self.ttl_current = duration
        self.factor = factor
        self.in_use = False
        self.slow_amount = 0


    def apply_to(self, robot):

        if not self.in_use and self.ttl_current > 0:
            self.slow_amount = robot.speed_current * (1 - self.factor)
            robot.speed_current -= self.slow_amount
            self.in_use = True

        # wenn abgelaufen → zurücksetzen
        if self.ttl_current <= 0 and self.in_use:
            robot.speed_current += self.slow_amount
            self.in_use = False

        # TTL runterzählen
        self.ttl_current -= 1

    def refresh(self):
        self.ttl_current = self.ttl_max

    def get_icon(self):
        return Textures.SLOW_ICON_STATUS
    


class Relic_RangeBuff(Effect):

    def __init__(self):
        self.ttl_max = 2 * SECOND
        self.ttl_current = self.ttl_max
        self.in_use = False        
        self.range_flat = 25
        self.range_buff = 0


    # applies the range
    def apply_to(self, robot):

        # Initial Application of the Buff
        if(not self.in_use):

            # apply buff on Initiation
            if(self.ttl_current > 0):
                print("buff initially applied")
                robot.attack_radius += self.range_flat
                self.range_buff += self.range_flat
                self.in_use = True 
                return
            else:
                return        
            
        # Revert Buff on TTL=0
        if(self.ttl_current <= 0 and self.in_use):
            robot.attack_radius -= self.range_buff

        # Tick down Time-to-Live
        self.ttl_current -= 1


    # repeats the range buff, resets ttl
    def repeat(self, robot, max_range = 200):
        print("range buff repeated")
        self.ttl_current = self.ttl_max
        if self.range_buff >= max_range:
            return
        robot.attack_radius += self.range_flat
        self.range_buff += self.range_flat


    def get_icon(self):
        return Textures.RANGE_ICON_STATUS
        

# Swordmaster_AttackspeedBuff: "gain x relative attackspeed every xth attack for y attacks"
class Swordmaster_AttackspeedBuff(Effect):

    def __init__(self,b):
        self.ttl_max = b             #attackspeed-buff for b attacks; !!! this is not a classic ttl, name because compatibility
        self.ttl_current = self.ttl_max           
        self.in_use = False        
        self.attackspeed_factor = 2.5
        self.attackspeed_buff = 0   #initiated in apply_to()



    # applies the range
    def apply_to(self, robot):

        # Initial Application of the Buff
        if(not self.in_use):

            # apply buff on Initiation
            if(self.ttl_current > 0):
                self.attackspeed_buff = robot.attack_cooldown / self.attackspeed_factor
                self.attackspeed_buff *= self.attackspeed_factor-1
                robot.attack_cooldown -= self.attackspeed_buff
                self.in_use = True
                return
            else:
                return        
            
        # Revert Buff on TTL=0
        if(self.ttl_current == 0 and self.in_use):
            robot.attack_cooldown += self.attackspeed_buff
            self.ttl_current -= 1
            print("as-buff reverted, new att-cd: "+str(robot.attack_cooldown))

    def decrease(self):
        self.ttl_current -= 1

    def get_icon(self):
        return Textures.AS_ICON_STATUS
    
        
