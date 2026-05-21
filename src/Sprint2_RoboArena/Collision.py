import pygame

class AABB:

    def __init__(self,x,y,x_max,y_max):
        # definiert durch Ecken oben links und unten rechts
        # extra nicht min_x und min_y für Kompatibilität
        self.x     = x
        self.y     = y
        self.x_max = x_max
        self.y_max = y_max

    # updates Position and Bigness
    def update(self,x,y,x_max,y_max):
        self.x     = x
        self.y     = y
        self.x_max = x_max
        self.y_max = y_max

    # "Checkt ob zwei Boxen sich überschneiden"
    #   Nimmt zwei aabb in der Form [(x,y),(x,y)]
    #   Gibt true aus wenn sich aabbs schneiden
    def check_collision(self, box):
         
        return (
            self.x     < box.x_max and
            self.x_max > box.x     and
            self.y     < box.y_max and
            self.y_max > box.y
        )
    
    def draw_at(self, arena, x,y):
        color = (155,0,0)
        screen = arena.screen

        #Berechne Breite und Höhe
        x_min = self.x
        y_min = self.y
        x_max = self.x_max
        y_max = self.y_max
        width  = x_max - x_min
        height = y_max - y_min

        # Zeichne
        pygame.draw.rect(
            screen,
            color,
            (x, y, width, height),
            width=1   # Zeichne nur die Kontur
        )
