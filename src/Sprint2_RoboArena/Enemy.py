import pygame
import random
import math



class Enemy:
    def __init__(self, screen, x ,y):
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 20
        self.aabb = [(self.x - self.radius, self.y - self.radius),
                     (self.x + self.radius, self.y + self.radius)]
        self.damage_radius = 100
        self.damage = 0.1
    #Spieler bekommt schaden wenn er im gewissen radius zum Turret ist.

    def check_damage_player(self, Robot, health):
        dx = Robot.x - self.x
        dy = Robot.y - self.y

        distance = math.hypot(dx, dy)

        if distance <self.damage_radius:
          health.take_damage(self.damage)


    # setzt Koordinaten auf zufällige Nummer innerhalb des screens
    # und updatet aabb
    def randomize_position(self):
        # frage Screengröße ab, dann erzeuge zufälliges x und y
        screen_width, screen_height = self.screen.get_size()
        x = random.randint(0, screen_width/2)
        y = random.randint(0, screen_height/2)

        # update Orb-Koordinaten
        self.x = x
        self.y = y



    # zeichnet den Gegener
    def draw(self):
        color = (0,128,0)

        pygame.draw.circle(
            self.screen,
            color,
            (self.x,self.y),
            self.radius
        )
        pygame.draw.circle(self.screen,(0,0,0),(self.x,self.y),100-self.radius,2)



