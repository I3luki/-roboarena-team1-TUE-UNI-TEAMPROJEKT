import pygame
import random
import math
from Collision import AABB
from HealthSystem_Enemy import HealthSystem_Enemy
from Enemy_Movement import Enemy_Movement


class Enemy:
    def __init__(self, arena, x ,y):
        self.arena  = arena
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.radius = 20
        self.aabb = AABB(self.x - self.radius,
                         self.y - self.radius,
                         self.x + self.radius, 
                         self.y + self.radius)
        self.damage_radius = 100
        self.damage = 0.1
        self.health_system = HealthSystem_Enemy()
        self.speed = 1.5
        self.movement = Enemy_Movement()

    #Spieler bekommt schaden wenn er im gewissen radius zum Turret ist.
    def check_damage_player(self, robot, health):
        dx = robot.x - self.x
        dy = robot.y - self.y

        distance = math.hypot(dx, dy)

        if distance <self.damage_radius:
          health.take_damage(self.damage)

    def draw_line_enemy(self,robot):
        # konvertiere zu screen-Koordinaten
        x_screen_enemy, y_screen_enemy = self.camera.global_to_screen(self)
        x_screen_robot, y_screen_robot = self.camera.global_to_screen(robot)

        # Setze Roboter-Screen-Koordinaten zu Mitte von Roboter
        x_screen_robot += robot.width/2
        y_screen_robot += robot.height/2

        # Zeichne
        pygame.draw.line(self.screen,
                        (25, 33, 33),
                        (x_screen_enemy, y_screen_enemy),
                        (x_screen_robot, y_screen_robot), 
                        1)
        
    # Generiert zufällige Koordinaten
    # Koordinaten sind valide, wenn gilt: Außerhalb des Screens UND keine Kollision mit Wänden
    def randomize_position(self):
        # frage Screengröße ab, dann erzeuge zufälliges x und y
        while True:
            x = random.randint(self.radius, self.arena.WIDTH - self.radius)
            y = random.randint(self.radius, self.arena.HEIGHT - self.radius)

            temp = type('', (), {})()
            temp.x = x
            temp.y = y

            x_screen, y_screen = self.camera.global_to_screen(temp)

            # Suche nach Position außerhalb des Screens
            if (0 <= x_screen <= self.screen.get_width() and
                    0 <= y_screen <= self.screen.get_height()):
                continue

            # Erstelle temporäres aabb
            # Suche damit Position, die nicht mit einer Wand kollidiert
            temp_aabb = AABB(x - self.radius, y - self.radius,
                             x + self.radius, y + self.radius)
            if any(temp_aabb.check_collision(wall.aabb) for wall in self.arena.walls):
                continue

            break

        # update Enemy-Koordinaten
        self.x = x
        self.y = y

        self.aabb = AABB(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )

    # zeichnet den Gegener
    def draw(self):
        color_inner = (0,128,0)
        color_outer = (0,0,0)

        x_screen, y_screen = self.camera.global_to_screen(self)

        # Zeichne inneren Kreis
        pygame.draw.circle(
            self.screen,
            color_inner,
            (x_screen,y_screen),
            self.radius
        )

        # Zeichne äußeren Kreis
        pygame.draw.circle(self.screen,
                           color_outer,
                           (x_screen,y_screen),
                           100,
                           2)

        self.health_system.draw(self.screen, x_screen, y_screen)


    def draw_aabb(self):
        # berechne screen Koordinaten mit Kreis Offset
        x_min_screen, y_min_screen = self.camera.global_to_screen(self)  
        x_min_screen -= self.radius
        y_min_screen -= self.radius

        # Zeichne
        self.aabb.draw_at(self.arena, x_min_screen, y_min_screen)

    # Update Enemy Movement zum Spieler
    def update(self, robot):
        self.movement.update(self, robot, self.arena.grid_matrix)