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