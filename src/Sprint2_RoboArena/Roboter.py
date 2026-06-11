import pygame
import math
from Collision import AABB
from Animation_Handler import load_spritesheet
from Animation_Handler import animation_scaling


class Robot:
    def __init__(self, arena, health, stamina, level, x, y):
        self.arena  = arena
        self.camera = arena.camera
        self.screen = arena.screen
        self.health = health
        self.stamina = stamina
        self.level = level
        self.status_effects = []
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed_base = 2
        self.speed_current = 2
        self.aabb = AABB(self.x,
                         self.y,
                         self.x + self.width,
                         self.y + self.height)
        self.angle = 0
        self.attack_radius = 200
        self.attack_damage = 10
        self.attack_cooldown = 1000
        self.last_attack_time = pygame.time.get_ticks()
        self.is_attacking = False
        self.attack_visible_until = 0
        self.cone_half_angle = 45
        self.is_moving = False
        self.facing = "down"
        self.current_frame = 0
        self.current_state = "idle"
        self.animation_speed = 0.1

        ## Das Spritesheet komplett einlesen und zerlegen
        # Beispiel: Datei, Breite des Frames, Höhe des Frames, Zeilen, Spalten
        # (Werte an Assets ggf. anpassen)
        grid_idle = load_spritesheet("Sprites/Swordsman_lvl3_Idle_without_shadow.png", 64, 64, 4, 12)
        grid_run = load_spritesheet("Sprites/Swordsman_lvl3_Run_without_shadow.png", 64, 64, 4, 8)
        grid_run_attack = load_spritesheet("Sprites/Swordsman_lvl3_Run_Attack_without_shadow.png", 64, 64, 4, 8)
        grid_idle_attack = load_spritesheet("Sprites/Swordsman_lvl3_attack_without_shadow.png", 64, 64, 4, 8)

        grid_idle = animation_scaling(grid_idle, 2.5)
        grid_run = animation_scaling(grid_run, 2.5)
        grid_idle_attack = animation_scaling(grid_idle_attack, 2.5)
        grid_run_attack = animation_scaling(grid_run_attack, 2.5)

        self.animations = {
            "idle": {
                "down": grid_idle[0],  # Zeile 1: Blick nach vorne (12 Frames)
                "left": grid_idle[1],  # Zeile 2: Blick nach rechts (12 Frames)
                "right": grid_idle[2],  # Zeile 3: Blick nach links (12 Frames)
                "up": grid_idle[3][:4]  # Zeile 4: Blick nach hinten (nur die 4 existierenden Frames!)
            },
            "run": {
                "down": grid_run[0],
                "left": grid_run[1],
                "right": grid_run[2],
                "up": grid_run[3]
            },
            "idle_attack": {
                "down": grid_idle_attack[0],
                "left": grid_idle_attack[1],
                "right": grid_idle_attack[2],
                "up": grid_idle_attack[3]
            },
            "run_attack": {
                "down": grid_run_attack[0],
                "left": grid_run_attack[1],
                "right": grid_run_attack[2],
                "up": grid_run_attack[3]
            }
        }



    # updatet die axis aligned bounding box
    def update_aabb(self):
         self.aabb.update(self.x, 
                          self.y,
                          self.x + self.width,
                          self.y + self.height)

    # überprüft ob Überschneidung mit einer Wand
    def collides_with_wall(self):
        for wall in self.arena.walls:
            if self.aabb.check_collision(wall.aabb):
                return True
        return False   # Falls durchläuft, dann kollidiert nicht mit einer Wand



    def move(self, keys):

        self.is_moving = False

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed_current
            self.is_moving = True
            self.update_aabb()
            if self.collides_with_wall():
                self.y += self.speed_current
                self.update_aabb()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed_current
            self.is_moving = True
            self.update_aabb()
            if self.collides_with_wall():
                self.y -= self.speed_current
                self.update_aabb()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed_current
            self.is_moving = True
            self.update_aabb()
            if self.collides_with_wall():
                self.x += self.speed_current
                self.update_aabb()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed_current
            self.is_moving = True
            self.update_aabb()
            if self.collides_with_wall():
                self.x -= self.speed_current
                self.update_aabb()


    # add a status effect to the robot
    def add_status_effect(self, effect):        
        # if not already effective add to status_effects
        self.status_effects.append(effect)

    # cleanly deletes all the status effects in next frame
    def undo_all_status_effects(self):
        for effect in self.status_effects:
            effect.undo()


    # updates the status effects list
    #   - checks for effect_tiles
    #   - applies effects and removes status_effects with ttl < 0
    def update_status_effects(self):

        # check for effect tiles and apply if colliding
        #   does not apply_to makes sure effect doesnt get applied when tile on cooldown
        for tile in self.arena.tiles:
            if self.aabb.check_collision(tile.aabb):
                tile.apply_to(self)

        # update the status_list and remove timed-out status_effects
        for status_effect in self.status_effects:
            status_effect.apply_to(self)
            if status_effect.ttl_current < 0:
                self.status_effects.remove(status_effect)

    # resets speed and status-effect-list
    def reset(self):
        self.speed_current = self.speed_base
        self.undo_all_status_effects()



    # Zeichne den Roboter
    def draw(self):
        x_screen, y_screen = self.camera.global_to_screen(self)

        # Berechne, in welche der 4 Richtungen der Roboter schaut
        self.update_facing_direction()

        # Animations-Logik
        if self.is_moving and not self.is_attacking:
            new_state = "run"
        elif not self.is_moving and not self.is_attacking:
            new_state = "idle"
        elif not self.is_moving and self.is_attacking:
            new_state = "idle_attack"
        elif self.is_moving and self.is_attacking:
            new_state = "run_attack"

        if new_state != self.current_state:
            self.current_state = new_state
            self.current_frame = 0

        # Animations-Frames holen und hochzählen
        frames = self.animations[self.current_state][self.facing]

        self.current_frame += self.animation_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        current_image = frames[int(self.current_frame)]

        # Bild auf den Screen zeichnen
        rect = current_image.get_rect(
            center=(x_screen + self.width / 2, y_screen + self.height / 2)
        )
        self.screen.blit(current_image, rect.topleft)

        if self.is_attacking:
            cx = x_screen + self.width / 2
            cy = y_screen + self.height / 2
            angle_rad = math.radians(self.angle)
            half_rad = math.radians(self.cone_half_angle)
            num_arc_points = 10
            points = [(cx, cy)]
            for i in range(num_arc_points + 1):
                a = angle_rad - half_rad + (2 * half_rad * i / num_arc_points)
                points.append((
                    cx + math.cos(a) * self.attack_radius,
                    cy - math.sin(a) * self.attack_radius
                ))
            pygame.draw.polygon(self.screen, (255, 0, 0), points)

    # "Zeichnet AAB-Kollisionbox"
    def draw_aabb(self):
        # berechne screen Koordinaten mit Kreis Offset
        x_min_screen, y_min_screen = self.camera.global_to_screen(self)  

        self.aabb.draw_at(self.arena, x_min_screen, y_min_screen)

        

    # Linie zur Maus
    def draw_line_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_screen, y_screen = self.camera.global_to_screen(self)
        pygame.draw.line(
            self.screen, 
            (255, 0, 0),
            (x_screen + (self.width/2), y_screen + (self.height/2)),
            (mouse_x, mouse_y), 2)
        

    # holt den Vektor zur Maus
    def get_direction_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_x, screen_y = self.camera.global_to_screen(self)
        #Berechnet Abstand von Mauszeiger zu sich selbst
        dx = mouse_x -  screen_x
        dy = mouse_y -  screen_y

        distance = math.hypot(dx, dy)
        #Return Abstand
        if distance !=0:
            return dx / distance, dy / distance

        return 0,0
    
    # updatet den Rotationswinkel
    def update_rotation(self):
        direction_x, direction_y = self.get_direction_to_mouse()

        target_angle = math.degrees(math.atan2(-direction_y, direction_x)
        )

        self.angle = target_angle

    def update_facing_direction(self):
        # self.angle geht (durch math.atan2) meist von -180 bis +180 Grad
        if -45 <= self.angle < 45:
            self.facing = "right"
        elif 45 <= self.angle < 135:
            self.facing = "up"
        elif self.angle >= 135 or self.angle < -135:
            self.facing = "left"
        elif -135 <= self.angle < -45:
            self.facing = "down"

    # Erstellt in einem Zeitintervall ein Radius um Spieler, der Damage an Gegnern verursacht
    def update_attack(self, enemies):
        currentTime = pygame.time.get_ticks()
        # Wenn cooldown abgelaufen ist, wird angegriffen
        if currentTime - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = currentTime
            self.is_attacking = True
            self.attack_visible_until = currentTime + 400

            # Frage alle Gegner ab, die im Kegel des Angriffs sind
            for enemy in enemies:
                dx = enemy.x - (self.x + self.width / 2)
                dy = enemy.y - (self.y + self.height / 2)
                distance = math.hypot(dx, dy)

                if distance < self.attack_radius + enemy.radius:
                    enemy_angle = math.degrees(math.atan2(-dy, dx))
                    angle_diff = (enemy_angle - self.angle + 180) % 360 - 180
                    if abs(angle_diff) <= self.cone_half_angle:
                        if hasattr(enemy, 'health_system'):
                            enemy.health_system.take_damage(self.attack_damage)
                            print(f"Gegner getroffen! HP: {enemy.health_system.current_health}")

        # Wenn Angriffscooldown noch nicht abgeklungen ist, kann nicht angegriffen werden
        if currentTime > self.attack_visible_until:
            self.is_attacking = False
