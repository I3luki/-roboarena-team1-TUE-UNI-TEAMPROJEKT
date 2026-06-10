import pygame
import random
from Collision import AABB
from Status_Effects import Speed_Buff, Healthgen_Buff, Poison_Debuff


SECOND = 60     # Eine Sekunde sind 60 Frames


# -------------------------------------------------- GLOBALE METHODEN, KONSTANTEN UND ALLGEMEINE KLASSEN -------------
# zeichnet die gegebene Instanz
def draw(rect):
    # update AABB
    rect.aabb.update(rect.x, rect.y,
                     rect.x + rect.width, rect.y + rect.height)
    
    # draw tile
    x_screen, y_screen = rect.camera.global_to_screen(rect)
    rect.screen.blit(rect.surface,
                     (x_screen, y_screen))
        
# Zeichnet einen Cooldown über das Tile
def draw_cooldown(tile):

    if(tile.cooldown_current > 0):
        # get width and height of tile
        width = tile.width
        height = tile.height
        x_screen, y_screen = tile.camera.global_to_screen(tile)

        # Transparente Fläche erstellen
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((80, 80, 80, 128)) # grau, 50% durchsichtig

        # Prozent bis wieder up berechnen
        ratio = (tile.cooldown_max - tile.cooldown_current) / tile.cooldown_max
        percent = int(ratio*100)

        # Zahl rendern
        font = pygame.font.Font(None, 15)
        text = font.render(str(percent)+"%", True, (255, 255, 255))

        # Text zentrieren
        text_rect = text.get_rect(center=(width//2, height//2))
        overlay.blit(text, text_rect)

        # Fläche auf den Bildschirm zeichnen
        tile.screen.blit(overlay, (x_screen, y_screen))
        
# Zeichnet die AABB der gegeben Instanz:        
def draw_aabb(rect):
        # berechne screen Koordinaten
        x_min_screen, y_min_screen = rect.camera.global_to_screen(rect)  

        rect.aabb.draw_at(rect.arena, x_min_screen, y_min_screen)



# allgemeine Klasse für Tiles
class Tile:
    COLOR = (255, 255,255)     # schwarz
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
        
        self.cooldown_max = 10 * SECOND
        self.cooldown_current = 0
        
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.COLOR)

    # Apply the given buff if cooldown is 0
    def apply_effect_to(self, effect ,robot):
        if (self.cooldown_current <= 0):
            robot.add_status_effect(effect)
            self.cooldown_current = self.cooldown_max

    # Updates the cooldown of the tile
    def update(self):
        if (self.cooldown_current > 0):
            self.cooldown_current -= 1
        
    def apply_to(self, robot):
        pass
         
    def draw(self):
        draw(self) # globale Methode
        draw_cooldown(self) # globale Methode

    def draw_aabb(self):
        draw_aabb(self) # globale Methode

# --------------------------------------------------------------------------------------------------------        




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



# Gives a SpeedBuff on Collision
class Speedtile(Tile):
    COLOR = (255, 255, 0)     # gelb
     
    # applies the unique effect to the given robot
    def apply_to(self, robot):
         self.apply_effect_to(Speed_Buff(), robot)

   
# Gives a Health-Regeneration-Buff on Collision
class Healthtile(Tile):
    COLOR = (255, 105, 180)  # pink

    # adds the effect to the robot
    def apply_to(self, robot):
         self.apply_effect_to(Healthgen_Buff(), robot)

     
# Gives a Random Buff or Debuff on Collision
class Surprisetile(Tile):
    COLOR  = (128, 0, 128) # purple

    
    # Chance for good or bad effect
    GOOD_PERCENT = 70
    BAD_PERCENT = 100 - GOOD_PERCENT


    def apply_to(self, robot):
        # The Good and Bad Buff from which are picked
        # !!!DONOT put those 2 in __init__ or as class constants
        GOOD_CHOICES = [Speed_Buff(), Healthgen_Buff()]
        BAD_CHOICES = [Poison_Debuff()]

        # pick good or bad choices with weights
        is_good_choices = random.choices((True, False),
                                        weights=(self.GOOD_PERCENT, self.BAD_PERCENT),
                                        k=1)
        # pick from those
        if(is_good_choices):
            choice = random.choice(GOOD_CHOICES)
        else:
            choice = random.choice(BAD_CHOICES)


        # apply the one picked
        self.apply_effect_to(choice, robot)
        

# Makes a small amount of Damage on Impact 
class CactusTile(Tile):
    COLOR = (0, 150, 0)
    width = 40
    height = 40
    
    DAMAGE = 0.5

    def __init__(self,arena,x,y):
        super().__init__(arena, x, y)
        self.cooldown_max = int(0.5*SECOND)
    
    
    def apply_to(self, robot):
        if (self.cooldown_current <= 0):
            robot.health.take_damage(self.DAMAGE) # that stings
            self.cooldown_current = self.cooldown_max


            
class SkullTile(Tile):
    COLOR = (70, 70, 70)
    width = 30
    height = 30

    def apply_to(self, robot):
         pass #TODO: implement an effect


class BoneTile(Tile):
    COLOR = (245, 245, 220)
    width = 35
    height = 15

    def apply_to(self, robot):
         pass #TODO: implement an effect



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