

SECOND = 60   # because 60FPS at the Moment


# Allgemeine Klasse für Effekte 
class Effect:
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


# -----------------------------------------------------------------------------------


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

        if(self.ttl_current < self.SPEED_SLOWDOWN and self.in_use):
            self.speed_buff -= self.slow_rate
            robot.speed_current -= self.slow_rate


        # Tick down Time-to-Live
        self.ttl_current -= 1


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



        
            

        

