import pygame
from Collision import AABB
from Status_Effects import Speed_Buff, Healthgen_Buff


# RICHTLINIEN für Klassen:
#
#                           Variablen:  arena
#                                       screen
#                                       camera
#                                       x
#                                       y
#                                       aabb
#                           Methoden:   draw()
#                                       draw_aabb()
#                                       apply_to(robot)            <- GILT NUR FÜR EFFEKT_TILES




# zeichnet die gegebene Instanz
def draw(rect):
        rect.aabb.update(rect.x, rect.y,
                         rect.x + rect.width, rect.y + rect.height)
        x_screen, y_screen = rect.camera.global_to_screen(rect)
        rect.screen.blit(rect.surface,
                         (x_screen, y_screen))
        
# Zeichnet die AABB der gegeben Instanz:        
def draw_aabb(rect):
        # berechne screen Koordinaten
        x_min_screen, y_min_screen = rect.camera.global_to_screen(rect)  

        rect.aabb.draw_at(rect.arena, x_min_screen, y_min_screen)
        



class Wall: 
    COLOR = (0,0,255)
     
    def __init__(self, arena, x, y, width, height):
          self.arena = arena
          self.screen = arena.screen
          self.camera = arena.camera
          self.x = x
          self.y = y
          self.width = width
          self.height = height
          self.aabb = AABB(x,y,
                           x + self.width, y + self.height)

          self.surface = pygame.Surface((width, height))
          self.surface.fill(self.COLOR)
             

    def draw(self):
        draw(self) # globale Methode

    def draw_aabb(self):
         draw_aabb(self) # globale Methode

  
class Speedtile:
    COLOR = (255, 255, 0)     # gelb
    width = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.aabb = AABB(x,y,
                         x + self.width, y + self.height)
        
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    # applies the unique effect to the given robot
    def apply_to(self, robot):
         status_effect = Speed_Buff()
         robot.add_status_effect(status_effect)
         

    def draw(self):
        draw(self) # globale Methode
    
    def draw_aabb(self):
         draw_aabb(self) # globale Methode
   
  
  
class Healthtile:
    COLOR = (255, 105, 180)  # pink
    width = 20
    height = 20

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.aabb = AABB(x,y,
                         x + self.width, y + self.height)        

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    # adds the effect to the robot
    def apply_to(self, robot):
         status_effect = Healthgen_Buff()
         robot.add_status_effect(status_effect)

    def draw(self):
        draw(self) # globale methode

    def draw_aabb(self):
         draw_aabb(self) # globale Methode
     

class Surprisetile:
    COLOR  = (128, 0, 128) # purple
    width  = 20
    height = 20
     
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.aabb = AABB(x,y,
                         x + self.width, y + self.height)
        
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)


    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        draw(self) # globale Methode

    def draw_aabb(self):
         draw_aabb(self) # globale Methode
        
        



class CactusTile:
    COLOR = (0, 150, 0)
    width = 40
    height = 40
    
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        self.x = x
        self.y = y

        self.aabb = AABB(
            x, y,
            x + self.width,
            y + self.height
        )

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)
        
        


class SkullTile():
    COLOR = (70, 70, 70)
    width = 30
    height = 30
    
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        self.x = x
        self.y = y

        self.aabb = AABB(
            x, y,
            x + self.width,
            y + self.height
        )

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)


class BoneTile():
    COLOR = (245, 245, 220)
    width = 35
    height = 15

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        self.x = x
        self.y = y

        self.aabb = AABB(
            x, y,
            x + self.width,
            y + self.height
        )

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)



class LightningTile:
    WARNING_COLOR = (255, 255, 0)   # gelbes Warn-Dreieck
    COLOR = (250, 250, 250)   # hellblau
    width = 80
    height = 80

    WARNING_TIME = 1000      # 1 Sekunde Warnung
    LIFETIME = 2000         # bleibt 2 Sekunden
    DAMAGE = 5              # Schaden pro Treffer
    DAMAGE_COOLDOWN = 500   # Schaden nur alle 0.5 Sekunden

    def __init__(self, arena):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        self.last_damage_time = 0
        self.spawn_random()

    def spawn_random(self):
        import random

        # Blitz-Arena besteht aus 2 Rechtecken:
        # 1. oben rechts
        # 2. rechts neben der Healzone

        spawn_areas = [
            (1500, 0, 1500, 1050),      # oben rechts
            (1950, 1050, 1050, 450),    # rechts neben Healzone
        ]

        area = random.choice(spawn_areas)

        area_x, area_y, area_width, area_height = area

        self.x = random.randint(area_x, area_x + area_width - self.width)
        self.y = random.randint(area_y, area_y + area_height - self.height)

        self.spawn_time = pygame.time.get_ticks()

        self.is_warning = True

        self.aabb = AABB(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height
        )

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def update(self, robot, health):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time

        self.aabb.update(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height
        )

        # Warnphase: noch kein Schaden

        if self.is_warning:
            if elapsed_time >= self.WARNING_TIME:
                self.is_warning = False
                self.spawn_time = current_time
            return

        #Aktivepahse
        if self.aabb.check_collision(robot.aabb):
            if current_time - self.last_damage_time >= self.DAMAGE_COOLDOWN:
                health.take_damage(self.DAMAGE)
                self.last_damage_time = current_time

        # Nach Aktivzeit neu spawnen
        if elapsed_time >= self.LIFETIME:
            self.spawn_random()

    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)

        if self.is_warning:
            points = [
                (x_screen + self.width / 2, y_screen),
                (x_screen, y_screen + self.height),
                (x_screen + self.width, y_screen + self.height)
            ]

            pygame.draw.polygon(
                self.screen,
                self.WARNING_COLOR,
                points
            )
        else:
          self.screen.blit(self.surface, (x_screen, y_screen))

    def draw_aabb(self):
        draw_aabb(self)

class Tornado:
    COLOR = (80, 80, 80)

    width = 70
    height = 70

    SPEED_X = 4
    SPEED_Y = 3

    DAMAGE = 8
    DAMAGE_COOLDOWN = 600

    def __init__(self, arena):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Startposition in der Blitz-Zone
        self.x = 2000
        self.y = 400

        self.dx = self.SPEED_X
        self.dy = self.SPEED_Y

        self.last_damage_time = 0

        self.aabb = AABB(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height
        )

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    def update(self, robot, health):
        current_time = pygame.time.get_ticks()

        old_x = self.x
        old_y = self.y

        self.x += self.dx
        self.y += self.dy

        # Blitz-Arena-Grenzen
        min_x = 1500
        max_x = 3000 - self.width
        min_y = 0
        max_y = 1500 - self.height

        # Healzone
        heal_x = 1050
        heal_y = 1050
        heal_w = 900
        heal_h = 900

        # Rand-Abprall
        if self.x <= min_x or self.x >= max_x:
            self.dx *= -1
            self.x = old_x

        if self.y <= min_y or self.y >= max_y:
            self.dy *= -1
            self.y = old_y

        # Aktuelle AABB updaten
        self.aabb.update(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height
        )

        # Healzone-AABB temporär bauen
        heal_aabb = AABB(
            heal_x,
            heal_y,
            heal_x + heal_w,
            heal_y + heal_h
        )

        # Wenn Tornado Healzone berührt: zurücksetzen und Richtung ändern
        if self.aabb.check_collision(heal_aabb):
            self.x = old_x
            self.y = old_y

            self.dx *= -1
            self.dy *= -1

            self.aabb.update(
                self.x,
                self.y,
                self.x + self.width,
                self.y + self.height
            )

        # Schaden
        if self.aabb.check_collision(robot.aabb):
            if current_time - self.last_damage_time >= self.DAMAGE_COOLDOWN:
                health.take_damage(self.DAMAGE)
                self.last_damage_time = current_time

    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)
        self.screen.blit(self.surface, (x_screen, y_screen))

    def draw_aabb(self):
        draw_aabb(self)