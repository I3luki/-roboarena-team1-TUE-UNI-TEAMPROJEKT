import pygame
import random
import math




class Enemy:
    def __init__(self, arena, x ,y):
        self.screen = arena.screen
        self.camera = arena.camera
        self.x = x
        self.y = y
        self.radius = 20
        self.aabb = [(self.x - self.radius, self.y - self.radius),
                     (self.x + self.radius, self.y + self.radius)]
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
        pygame.draw.line(self.screen,
                  (25, 33, 33),
                  (self.x , self.y),
                  (robot.x,robot.y), 1)
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
        color = (0,128,0)

        x_screen, y_screen = self.camera.global_to_screen(self)

        pygame.draw.circle(
            self.screen,
            color,
            (x_screen,y_screen),
            self.radius
        )
        pygame.draw.circle(self.screen,(0,0,0),(self.x,self.y),100,2)



