class Camera: 

    CAMERA_SPEED = 0.05

    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y

    def update(self, robot):
        # update camera position smoothly
        self.x -= (self.x - robot.x) * self.CAMERA_SPEED
        self.y -= (self.y - robot.y) * self.CAMERA_SPEED

    # berechnet den offset/vektor von Kameraposition zu Roboterposition
    #   in:         object must have object.x and object.y
    #   return:     float,float
    def offset_to_object(self, object):
        x = (object.x - self.x)
        y = (object.y - self.y)

        return x,y
    
    # konvertiert globale Koordinaten zu Koordinaten auf dem Screen
    #   in:         object must have object.x and object.y
    #   return:     float,float
    def global_to_screen(self, object):
        # hole screengröße und offset zur Kamera
        screen_width, screen_height = self.screen.get_size()
        offset_x, offset_y = self.offset_to_object(object)

        # Berechne Position auf dem screen
        x = (screen_width / 2)  + offset_x
        y = (screen_height / 2) + offset_y

        return x,y