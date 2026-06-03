import pygame
import math
from Collision import AABB


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
        self.attack_radius = 80
        self.attack_damage = 10
        self.attack_cooldown = 1000
        self.last_attack_time = pygame.time.get_ticks()
        self.is_attacking = False
        self.attack_visible_until = 0



    # updatet die axis aligned bounding box
    def update_aabb(self):
         self.aabb.update(self.x, 
                          self.y,
                          self.x + self.width,
                          self.y + self.height)

    # überprüft ob Überschneidung mit einer Wand
    def collides_with_wall(self):
        for wall in self.arena.walls:
            if(self.aabb.check_collision(wall.aabb)):
                return True
        False   # Falls durchläuft, dann kollidiert nicht mit einer Wand



    def move(self, keys):

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed_current
            self.update_aabb()
            if(self.collides_with_wall()):
                self.y += self.speed_current
                self.update_aabb()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed_current
            self.update_aabb()
            if(self.collides_with_wall()):
                self.y -= self.speed_current
                self.update_aabb()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed_current
            self.update_aabb()
            if(self.collides_with_wall()):
                self.x += self.speed_current
                self.update_aabb()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed_current
            self.update_aabb()
            if(self.collides_with_wall()):
                self.x -= self.speed_current
                self.update_aabb()


    # add a status effect to the robot
    def add_status_effect(self, effect):

        # check if effect already effective
        for status_effect in self.status_effects:
            if(isinstance(status_effect, type(effect))):
                status_effect.renew()
                return                           # return if effect already active
        
        # if not already effective add to status_effects
        self.status_effects.append(effect)
    def reset_status_effects(self):
        for effect in self.status_effects:
            effect.reset()

        self.status_effects.clear()


    # updates the status effects list
    # checks for effect_tiles
    # applies effects and removes status_effects with ttl==0
    def update_status_effects(self):

        # check for effect tiles and apply if colliding
        for tile in self.arena.tiles:
            if(self.aabb.check_collision(tile.aabb)):
                tile.apply_to(self)

        # update the status_list
        for status_effect in self.status_effects:
            status_effect.apply_to(self)
            if (status_effect.ttl_current < 0):
                self.status_effects.remove(status_effect)

    def reset(self):
        self.speed_current = self.speed_base
        self.reset_status_effects()



    # Zeichner den Roboter
    def draw(self):

        # lokale Koordinaten
        x_screen, y_screen = self.camera.global_to_screen(self)

        # Eigene Fläche
        robot_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Körper
        pygame.draw.rect(
            robot_surface,
            (120, 120, 120),
            (0, 0, self.width, self.height)
        )

        # Kopf
        pygame.draw.circle(
            robot_surface,
            (0, 255, 0),
            (35, 25),
            8
        )

        # Rotieren
        rotated_surface = pygame.transform.rotate(robot_surface, self.angle)

        # Mittelpunkt setzen
        rect = rotated_surface.get_rect(
            center=(x_screen + self.width/2, y_screen + self.height/2)
        )

        # zeichen in screen
        self.screen.blit(rotated_surface, rect.topleft)

        # Wenn Attacke aktiv ist, zeichne Kreis
        if self.is_attacking:
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (x_screen + (self.width/2), y_screen + (self.height/2)),
                self.attack_radius
            )

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

        # Smooth Rotation
        angle_difference = (target_angle - self.angle + 180) % 360 - 180

        self.angle += angle_difference * 0.1

    # Erstellt in einem Zeitintervall ein Radius um Spieler, der Damage an Gegnern verursacht
    def update_attack(self, enemies):
        currentTime = pygame.time.get_ticks()
        # Wenn cooldown abgelaufen ist, wird angegriffen
        if currentTime - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = currentTime
            self.is_attacking = True
            self.attack_visible_until = currentTime + 150

            # Frage alle Gegner ab, die in dem Radius des Angriffs sind
            for enemy in enemies:
                dx = enemy.x - (self.x + self.width / 2)
                dy = enemy.y - (self.y + self.height / 2)
                distance = math.hypot(dx, dy)

                # Wenn der Gegner im Attackeradius ist, verliert er Leben
                if distance < self.attack_radius + enemy.radius:
                    if hasattr(enemy, 'health_system'):
                        enemy.health_system.take_damage(self.attack_damage)
                        print(f"Gegner getroffen! HP: {enemy.health_system.current_health}")

        # Wenn Angriffscooldown noch nicht abgeklungen ist, kann nicht angegriffen werden
        if currentTime > self.attack_visible_until:
            self.is_attacking = False
