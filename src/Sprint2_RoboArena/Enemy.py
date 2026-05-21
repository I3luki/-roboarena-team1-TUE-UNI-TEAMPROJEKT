import pygame
import random
import math
from Collision import AABB
from Camera import Camera



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
        
    # setzt Koordinaten auf zufällige Nummer innerhalb des screens
    # und updatet aabb
    def randomize_position(self):
        # frage Screengröße ab, dann erzeuge zufälliges x und y
        screen_width, screen_height = self.screen.get_size()
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)

        # update Enemy-Koordinaten
        self.x = x
        self.y = y



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


    def draw_aabb(self):
        # berechne screen Koordinaten mit Kreis Offset
        x_min_screen, y_min_screen = self.camera.global_to_screen(self)  
        x_min_screen -= self.radius
        y_min_screen -= self.radius

        # Zeichne
        self.aabb.draw_at(self.arena, x_min_screen, y_min_screen)



