


# FORDERUNGEN:
#
#       Variablen:  ttl_current
#
#       Methoden:   renew(self)
#                   apply_to(self, robot)



SECOND = 60   # because 60FPS at the Moment

# 01 Speed Buff
class Speed_Buff:

    def __init__(self):
        self.ttl_max = 3 * SECOND
        self.ttl_current = self.ttl_max
        self.in_use = False        
        self.speed_factor = 1.5
        self.speed_buff = 0   # initiation in apply_to()

    # renews the TTL
    def renew(self):
        self.ttl_current = self.ttl_max

    # applies the speed buff
    def apply_to(self, robot):

        # Initial Application of the Buff
        if(not self.in_use):
            # compute buff
            self.speed_buff = robot.speed_base * self.speed_factor

            # apply buff on Initiation
            if(self.ttl_current > 0):
                robot.speed_current += self.speed_buff
                self.in_use = True 
                return
            else:
                return
            
        # Revert Buff on TTL=0
        if(self.ttl_current <= 0):
            robot.speed_current -= self.speed_buff

        # Tick down Time-to-Live
        self.ttl_current -= 1
            


class Healthgen_Buff:

    def __init__(self):
        self.ttl_max = 1 * SECOND
        self.ttl_current = self.ttl_max
        self.heal_amount = 0.7                   
        self.tick_rate = int(0.25 * SECOND)
        

    def renew(self):
        time_to_next_tick = self.ttl_current % self.tick_rate  # prevent overclocking (so heal doesnt get triggered permanantly on tile)
        self.ttl_current = self.ttl_max + time_to_next_tick

    def apply_to(self, robot):
        current_health = robot.health.current_health
        max_health = robot.health.max_health

        # if not full HP and is on tick
        if(current_health < max_health and self.ttl_current % self.tick_rate == 0):
            # prevent overhealing
            if(current_health+self.heal_amount > max_health):
                robot.health.current_health = robot.health.max_health
            else:
                robot.health.current_health += self.heal_amount

        # update TTL
        self.ttl_current -= 1

        
            

        

