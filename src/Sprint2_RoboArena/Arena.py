import pygame
from Arena_Objects import Wall,Speedtile,Healthtile,Surprisetile
from Camera import Camera
from collections import namedtuple

class Arena:


    def __init__(self, screen):

        self.screen = screen
        self.WIDTH = 3000
        self.HEIGHT = 3000
        self.camera = Camera(screen, 0, 0)


        # Hintergrund-Surfaces erstellen
        self.background_surf = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.background_surf.fill((200, 200, 200))

        # list of all walls
        #   a wall is (x, y, WIDTH, HEIGHT)
        self.walls = [
            Wall(self, 1000, 1000, 200, 20),
            Wall(self, 1000, 1000, 20, 200),
            Wall(self, 1000, 1000, 200, 20),
            Wall(self, 1200, 800, 20, 200)
        ]

        # list of all tiles
        #   a tile is (x,y)
        self.tiles = [
            Speedtile(self, 1500, 1500),

            Healthtile(self, 1200,1200), 
            Healthtile(self, 500,500),

            Surprisetile(self, 1200, 1500), 
            Surprisetile(self, 1750,250)
        ]


    # checks if a rectangle is visible on the screen
    def is_rect_onscreen(self, rect):
        min_x = self.camera.x - self.screen.get_width()/2
        max_x = self.camera.y - self.screen.get_width()/2
        min_y = self.camera.x + self.screen.get_height()/2
        max_y = self.camera.y + self.screen.get_height()/2

        return (   min_x > rect.x + rect.width
                or max_x < rect.x 
                or min_y > rect.y + rect.width
                or max_y < rect.y)

    # draws all walls which are in screen
    def draw_walls(self):
        for wall in self.walls:
            if(self.is_rect_onscreen(wall)):
                wall.draw()

    # draws all tiles which are in screen
    def draw_tiles(self):
        for tile in self.tiles:
            if(self.is_rect_onscreen(tile)):
                tile.draw()


    def draw(self, robot):

        # Zeichne Hintergrund
        self.screen.blit(self.background_surf, (0, 0))

        self.camera.update(robot)
        self.draw_walls()
        self.draw_tiles()


    