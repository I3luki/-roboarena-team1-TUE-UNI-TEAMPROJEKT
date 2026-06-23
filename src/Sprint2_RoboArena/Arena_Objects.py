import pygame
import random
import math
from Collision import AABB
from Status_Effects import Speed_Buff, Healthgen_Buff, Poison_Debuff
from Textures import Textures

SECOND = 60     # Eine Sekunde sind 60 Frames


# -------------------------------------------------- GLOBALE METHODEN, KONSTANTEN UND ALLGEMEINE KLASSEN -------------
# zeichnet die gegebene Instanz
def draw(rect):
    # Schauen, ob das Objekt eigene Offsets hat, sonst 0 nutzen
    offset_x = getattr(rect, 'offset_x', 0)
    offset_y = getattr(rect, 'offset_y', 0)

    # update aabb unter Beachtung des Offsets
    rect.aabb.update(
        rect.x + offset_x,
        rect.y + offset_y,
        rect.x + offset_x + rect.width,
        rect.y + offset_y + rect.height
    )

    x_screen, y_screen = rect.camera.global_to_screen(rect)

    offset_x = (rect.surface.get_width() - rect.width) // 2
    offset_y = (rect.surface.get_height() - rect.height) // 2

    # draw rect
    rect.screen.blit(rect.surface,
                     (x_screen - offset_x,
                      y_screen - offset_y))
        
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
        # Offsets holen (Standard 0)
        offset_x = getattr(rect, 'offset_x', 0)
        offset_y = getattr(rect, 'offset_y', 0)

        # berechne screen Koordinaten
        x_min_screen, y_min_screen = rect.camera.global_to_screen(rect)

        rect.aabb.draw_at(
            rect.arena,
            x_min_screen + offset_x,
            y_min_screen + offset_y
        )



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

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        tex_w = Textures.LABYRINTH_WALL.get_width()
        tex_h = Textures.LABYRINTH_WALL.get_height()

        for tx in range(0, width, tex_w):
            for ty in range(0, height, tex_h):
                self.surface.blit(Textures.LABYRINTH_WALL, (tx, ty))


    def draw(self):
        draw(self) # globale Methode

    def draw_aabb(self):
         draw_aabb(self) # globale Methode



# Gives a SpeedBuff on Collision
class Speedtile(Tile):
    COLOR = (255, 255, 0)     # gelb
     
    # adds the effect to the robot
    def apply_to(self, robot):
        self.apply_effect_to(Speed_Buff(), robot)

    def draw(self):
        # 1. Das normale pinke Tile und den eventuellen Prozent-Cooldown zeichnen
        super().draw()

        # 2. Das schwebende Icon nur zeichnen, wenn das Tile bereit ist (kein Cooldown)
        if self.cooldown_current <= 0:
            current_time = pygame.time.get_ticks()

            # Sinuswelle für das Auf- und Abschweben (Geschwindigkeit * 0.005, Reichweite 5 Pixel)
            bobbing_offset = math.sin(current_time * 0.005) * 5

            x_screen, y_screen = self.camera.global_to_screen(self)

            # Das Icon (30x30) mittig über dem Tile (20x20) platzieren und leicht nach oben versetzen
            icon_x = x_screen + (self.width - Textures.SPEED_ICON.get_width()) // 2
            icon_y = y_screen + (self.height - Textures.SPEED_ICON.get_height()) // 2 - 12 + bobbing_offset

            self.screen.blit(Textures.SPEED_ICON, (icon_x, icon_y))


# Gives a Health-Regeneration-Buff on Collision
class Healthtile(Tile):
    COLOR = (255, 105, 180)  # pink

    # adds the effect to the robot
    def apply_to(self, robot):
        self.apply_effect_to(Healthgen_Buff(), robot)

    def draw(self):
        # 1. Das normale pinke Tile und den eventuellen Prozent-Cooldown zeichnen
        super().draw()

        # 2. Das schwebende Icon nur zeichnen, wenn das Tile bereit ist (kein Cooldown)
        if self.cooldown_current <= 0:
            current_time = pygame.time.get_ticks()

            # Sinuswelle für das Auf- und Abschweben (Geschwindigkeit * 0.005, Reichweite 5 Pixel)
            bobbing_offset = math.sin(current_time * 0.005) * 5

            x_screen, y_screen = self.camera.global_to_screen(self)

            # Das Icon (30x30) mittig über dem Tile (20x20) platzieren und leicht nach oben versetzen
            icon_x = x_screen + (self.width - Textures.HEALING_ICON.get_width()) // 2
            icon_y = y_screen + (self.height - Textures.HEALING_ICON.get_height()) // 2 - 12 + bobbing_offset

            self.screen.blit(Textures.HEALING_ICON, (icon_x, icon_y))

     
# Gives a Random Buff or Debuff on Collision
class Surprisetile(Tile):
    COLOR  = (128, 0, 128) # purple

    
    # Chance for good or bad effect
    GOOD_PERCENT = 70
    BAD_PERCENT = 100 - GOOD_PERCENT


    def apply_to(self, robot):

        # Falls Tile auf Cooldown, keine Berechnung
        if(self.cooldown_current > 0):
            return

        # The Good and Bad Buff from which are picked
        # !!!DONOT put those 2 in __init__ or as class constants
        GOOD_CHOICES = [Speed_Buff(), Healthgen_Buff()]
        BAD_CHOICES = [Poison_Debuff()]

        # pick good or bad choices with weights
        is_good_choices = random.choices((True, False),
                                        weights=(self.GOOD_PERCENT, self.BAD_PERCENT),
                                        k=1)[0]
        # pick from those
        if(is_good_choices):
            choice = random.choice(GOOD_CHOICES)
        else:
            choice = random.choice(BAD_CHOICES)


        # apply the one picked
        self.apply_effect_to(choice, robot)

    def draw(self):
        # 1. Das normale pinke Tile und den eventuellen Prozent-Cooldown zeichnen
        super().draw()

        # 2. Das schwebende Icon nur zeichnen, wenn das Tile bereit ist (kein Cooldown)
        if self.cooldown_current <= 0:
            current_time = pygame.time.get_ticks()

            # Sinuswelle für das Auf- und Abschweben (Geschwindigkeit * 0.005, Reichweite 5 Pixel)
            bobbing_offset = math.sin(current_time * 0.005) * 5

            x_screen, y_screen = self.camera.global_to_screen(self)

            # Das Icon (30x30) mittig über dem Tile (20x20) platzieren und leicht nach oben versetzen
            icon_x = x_screen + (self.width - Textures.RANDOM_ICON.get_width()) // 2
            icon_y = y_screen + (self.height - Textures.RANDOM_ICON.get_height()) // 2 - 12 + bobbing_offset

            self.screen.blit(Textures.RANDOM_ICON, (icon_x, icon_y))
        

# Makes a small amount of Damage on Impact 
class Cactus:
    width = 15
    height = 15
    DAMAGE = 0.5

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        self.last_damage_time = 0
        self.cooldown = 500

        # Bild laden und auf die gewünschte Grafik-Größe skalieren
        self.surface = pygame.transform.scale(Textures.CACTUS1, (80, 80))
        self.sort_offset = 60

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def handle_damage(self, robot):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.cooldown:
            self.last_damage_time = current_time
            robot.health.take_damage(self.DAMAGE)
    
    
    def apply_to(self, robot):
        if (self.cooldown_current <= 0):
            robot.health.take_damage(self.DAMAGE) # that stings
            self.cooldown_current = self.cooldown_max

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class CursedStone:
    width = 70
    height = 50

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        # Bild laden und auf die gewünschte Grafik-Größe
        # Entweder 1 oder 2 der Assets aus Textures.CURSED_ROCK1 oder Textures.CURSED_ROCK2
        r = random.randint(0, 1)
        if r == 0:
            self.surface = pygame.transform.scale(Textures.CURSED_STONE1, (100, 140))
            self.sort_offset = 70
        else:
            self.surface = pygame.transform.scale(Textures.CURSED_STONE2, (100, 140))
            self.sort_offset = 70

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class CursedHole:

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        # Bild laden und auf die gewünschte Grafik-Größe
        r = random.randint(1, 3)
        if r == 1:
            self.surface = pygame.transform.scale(Textures.CURSED_HOLE1, (100, 140))
            self.width = 42
            self.height = 36
        elif r == 2:
            self.surface = pygame.transform.scale(Textures.CURSED_HOLE2, (100, 140))
            self.width = 38
            self.height = 32
        else:
            self.surface = pygame.transform.scale(Textures.CURSED_HOLE3, (100, 140))
            self.width = 34
            self.height = 42

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)


class Bone:

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        self.x = x
        self.y = y

        r = random.randint(1,6)
        if r == 1:
            self.surface = pygame.transform.scale(Textures.BONE1, (120, 120))
            self.width = 60
            self.height = 40
            self.sort_offset = 60

            self.offset_x = 10
            self.offset_y = -20

        elif r == 2:
            self.surface = pygame.transform.scale(Textures.BONE2, (200, 200))
            self.width = 100
            self.height = 60
            self.sort_offset = 100

            self.offset_x = -10
            self.offset_y = 0

        elif r == 3:
            self.surface = pygame.transform.scale(Textures.BONE3, (100, 100))
            self.width = 60
            self.height = 20
            self.sort_offset = 60

            self.offset_x = 0
            self.offset_y = 0

        elif r == 4:
            self.surface = pygame.transform.scale(Textures.BONE4, (100, 100))
            self.width = 40
            self.height = 30
            self.sort_offset = 60

            self.offset_x = 0
            self.offset_y = 0

        elif r == 5:
            self.surface = pygame.transform.scale(Textures.BONE5, (100, 100))
            self.width = 50
            self.height = 25
            self.sort_offset = 60

            self.offset_x = 0
            self.offset_y = -10

        elif r == 6:
            self.surface = pygame.transform.scale(Textures.BONE6, (90, 90))
            self.width = 30
            self.height = 40
            self.sort_offset = 60

            self.offset_x = 10
            self.offset_y = -20

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Bone_Rib:

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        self.x = x
        self.y = y

        r = random.randint(1,2)
        if r == 1:
            self.surface = pygame.transform.scale(Textures.BONE_RIB1, (200, 200))
            self.width = 40
            self.height = 70
            self.sort_offset = 100

            self.offset_x = 20
            self.offset_y = 30

        elif r == 2:
            self.surface = pygame.transform.scale(Textures.BONE_RIB2, (200, 200))
            self.width = 40
            self.height = 70
            self.sort_offset = 100

            self.offset_x = -10
            self.offset_y = 30

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)


class Stone:

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        # Bild laden und auf die gewünschte Grafik-Größe (100x100) skalieren
        r = random.randint(1, 7)
        if r == 1:
            self.surface = pygame.transform.scale(Textures.STONE1, (150, 150))
            self.width = 70
            self.height = 45
            self.sort_offset = 100
        elif r == 2:
            self.surface = pygame.transform.scale(Textures.STONE2, (80, 80))
            self.width = 43
            self.height = 25
            self.sort_offset = 40
        elif r == 3:
            self.surface = pygame.transform.scale(Textures.STONE3, (150, 150))
            self.width = 72
            self.height = 48
            self.sort_offset = 80
        elif r == 4:
            self.surface = pygame.transform.scale(Textures.STONE4, (110, 110))
            self.width = 43
            self.height = 33
            self.sort_offset = 75
        elif r == 5:
            self.surface = pygame.transform.scale(Textures.STONE5, (130, 130))
            self.width = 60
            self.height = 40
            self.sort_offset = 75
        elif r == 6:
            self.surface = pygame.transform.scale(Textures.STONE6, (130, 130))
            self.width = 75
            self.height = 40
            self.sort_offset = 75
        else:
            self.surface = pygame.transform.scale(Textures.STONE7, (130, 130))
            self.width = 80
            self.height = 45
            self.sort_offset = 75

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Ruins:

    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        self.surface = pygame.transform.scale(Textures.RUINS1, (250, 250))
        self.width = 160
        self.height = 110
        self.sort_offset = 150

        self.offset_x = 0
        self.offset_y = 30

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Tree_Normal:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        self.surface = Textures.TREE_NORMAL
        self.width = 20
        self.height = 20
        self.sort_offset = 85

        self.offset_x = 0
        self.offset_y = 15

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Tree_Dead:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        self.surface = Textures.TREE_DEAD
        self.width = 20
        self.height = 20
        self.sort_offset = 85

        self.offset_x = 0
        self.offset_y = 15

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Tree_Palm:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        self.surface = Textures.TREE_PALM
        self.width = 20
        self.height = 20
        self.sort_offset = 85

        self.offset_x = 0
        self.offset_y = 15

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Tree_Fir:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        self.surface = Textures.TREE_FIR
        self.width = 20
        self.height = 20
        self.sort_offset = 85

        self.offset_x = 0
        self.offset_y = 15

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Center_Normal:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        r = random.randint(1, 3)
        if r == 1:
            self.surface = Textures.CENTER_NORMAL1
            self.width = 30
            self.height = 15
            self.sort_offset = 60

        elif r == 2:
            self.surface = Textures.CENTER_NORMAL2
            self.width = 30
            self.height = 15
            self.sort_offset = 60

        elif r == 3:
            self.surface = Textures.CENTER_NORMAL3
            self.width = 30
            self.height = 15
            self.sort_offset = 50

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Center_Dead:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        r = random.randint(1, 3)
        if r == 1:
            self.surface = Textures.CENTER_DEAD1
            self.width = 60
            self.height = 20
            self.sort_offset = 80

            self.offset_x = 0
            self.offset_y = -10

        elif r == 2:
            self.surface = Textures.CENTER_DEAD2
            self.width = 30
            self.height = 15
            self.sort_offset = 60

        elif r == 3:
            self.surface = Textures.CENTER_DEAD3
            self.width = 30
            self.height = 15
            self.sort_offset = 60

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Center_Palm:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        r = random.randint(1, 3)
        if r == 1:
            self.surface = Textures.CENTER_PALM1
            self.width = 30
            self.height = 15
            self.sort_offset = 60

        elif r == 2:
            self.surface = Textures.CENTER_PALM2
            self.width = 30
            self.height = 15
            self.sort_offset = 60

            self.offset_x = 5
            self.offset_y = 0

        elif r == 3:
            self.surface = Textures.CENTER_PALM3
            self.width = 30
            self.height = 15
            self.sort_offset = 60

        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)

class Center_Fir:
    def __init__(self, arena, x, y):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera

        # Die Hitbox sitzt genau auf den übergebenen Koordinaten
        self.x = x
        self.y = y

        r = random.randint(1, 2)
        if r == 1:
            self.surface = Textures.CENTER_FIR1
            self.width = 30
            self.height = 15
            self.sort_offset = 60

        elif r == 2:
            self.surface = Textures.CENTER_FIR2
            self.width = 30
            self.height = 15
            self.sort_offset = 60


        self.aabb = AABB(self.x, self.y, self.x + self.width, self.y + self.height)

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)


class GrassTile:
    def __init__(self, arena, x, y, surface):
        self.arena = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.surface = surface  # Hier übergeben wir die bereits ausgeschnittene Kachel

    def draw(self):
        # Wir nutzen dein Kamerasystem. Da 'global_to_screen' das Objekt selbst erwartet,
        # übergeben wir 'self' (da es .x und .y besitzt).
        x_screen, y_screen = self.camera.global_to_screen(self)

        # Direkt auf den Bildschirm blitten (ohne AABB-Berechnungen)
        self.screen.blit(self.surface, (x_screen, y_screen))

class LightningTile:
    WARNING_COLOR = (255, 255, 0)   # gelbes Warn-Dreieck
    COLOR = (250, 250, 250)   # hellblau
    width = 80
    height = 20

    WARNING_TIME = 500      # 1 Sekunde Warnung
    LIFETIME = 500         # bleibt 2 Sekunden
    DAMAGE = 5              # Schaden pro Treffer
    DAMAGE_COOLDOWN = 500   # Schaden nur alle 0.5 Sekunden

    FRAME_DURATION = 60 # Wie viele ms ein Animationsframe sichtbar ist

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
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_time
        x_screen, y_screen = self.camera.global_to_screen(self)

        if self.is_warning:
            # Schatten zeichnen
            shadow_x = x_screen + (self.width // 2) - (Textures.LIGHTNING_SHADOW.get_width() // 2)
            shadow_y = y_screen + (self.height // 2) - (Textures.LIGHTNING_SHADOW.get_height() // 2)
            self.screen.blit(Textures.LIGHTNING_SHADOW, (shadow_x, shadow_y))

        else:
            # Blitz Animation abspielen
            active_frames = Textures.LIGHTNING_ANIMATION[0]
            frame_index = (elapsed_time // self.FRAME_DURATION) % len(active_frames)
            current_surface = active_frames[frame_index]

            # Zentrieren damit Hitbox mittig vom Blitz ist
            x_offset = (current_surface.get_width() - self.width) // 2
            y_offset = current_surface.get_height() - self.height

            self.screen.blit(current_surface, (x_screen - x_offset, y_screen - y_offset))

    def draw_aabb(self):
        draw_aabb(self)

class Tornado:
    width = 105
    height = 105

    SPEED_X = 4
    SPEED_Y = 3

    DAMAGE = 8
    DAMAGE_COOLDOWN = 600

    PULL_RADIUS = 250
    PULL_STRENGTH = 2

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

        self.frames = [frame for row in Textures.TORNADO_ANIMATION for frame in row]

        self.current_frame = 0
        self.animation_speed = 0.35 # höher = schneller, niedriger = langsamer

        self.surface = self.frames[0]

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

        # Animation
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        self.surface = self.frames[int(self.current_frame)]

        # Spieler anziehen

        dx_player = self.x + self.width / 2 - robot.x
        dy_player = self.y + self.height / 2 - robot.y

        distance = math.sqrt(dx_player**2 + dy_player**2)

        if 0 < distance < self.PULL_RADIUS:
            strength = (self.PULL_RADIUS - distance) / self.PULL_RADIUS * 5

            robot.x += (dx_player / distance) * strength
            robot.y += (dy_player / distance) * strength

            robot.update_aabb()

                # Schaden
        if self.aabb.check_collision(robot.aabb):
            if current_time - self.last_damage_time >= self.DAMAGE_COOLDOWN:
                health.take_damage(self.DAMAGE)
                self.last_damage_time = current_time

    def apply_to(self, robot):
         pass #TODO: implement an effect

    def draw(self):
        draw(self)

    def draw_aabb(self):
        draw_aabb(self)