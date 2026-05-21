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


        # list of all walls
        #   a wall is (x, y, WIDTH, HEIGHT)
        self.walls = [
            Wall(self, 1000, 1000, 200, 20),
            Wall(self, 1000, 1000, 20, 200)
        ]

        # list of all tiles
        #   a tile is (x,y)
        self.tiles = [
            Speedtile(self, 1500, 1500),

            Healthtile(self, 100,100), 
            Healthtile(self, 500,500),

            Surprisetile(self, 300, 250), 
            Surprisetile(self, 1750,250)
        ]

      


        
        # Surfaces erstellen
        self.background_surf = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.background_surf.fill((200, 200, 200))
        """
        

        self.wall_surf = pygame.Surface((50, 50))
        self.wall_surf.fill((44, 44, 44))

        self.red_surf = pygame.Surface((50, 50))
        self.red_surf.fill((255, 0, 0))

        self.blue_surf = pygame.Surface((50, 50))
        self.blue_surf.fill((0, 0, 255))

        self.green_surf = pygame.Surface((50, 50))
        self.green_surf.fill((0, 255, 0))

        self.yellow_surf = pygame.Surface((50, 50))
        self.yellow_surf.fill((255, 255, 0))
        """


    # kann meine tastatur nicht benutzen brauch das um zu kopieren:   >

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

        self.screen.blit(self.background_surf, (0, 0))

        self.camera.update(robot)
        self.draw_walls()
        self.draw_tiles()





        self.screen.blit(self.background_surf, (0, 0))
    
        """
        # Wände
        for x in range(0, 1000, 50):
            self.screen.blit(self.wall_surf, (x, 0))
            self.screen.blit(self.wall_surf, (x, 950))
        for y in range(0, 1000, 50):
            self.screen.blit(self.wall_surf, (0, y))
            self.screen.blit(self.wall_surf, (950, y))

        # Blaue Hindernisse
        for x in range(200, 400, 50):
            self.screen.blit(self.blue_surf, (x, 200))
            self.screen.blit(self.blue_surf, (x, 750))
        for x in range(600, 800, 50):
            self.screen.blit(self.blue_surf, (x, 200))
            self.screen.blit(self.blue_surf, (x, 750))
        for y in range(200, 400, 50):
            self.screen.blit(self.blue_surf, (200, y))
            self.screen.blit(self.blue_surf, (750, y))
        for y in range(600, 800, 50):
            self.screen.blit(self.blue_surf, (200, y))
            self.screen.blit(self.blue_surf, (750, y))

        # Gelb, Rot, Grün
        self.screen.blit(self.yellow_surf, (475, 475))

        self.screen.blit(self.red_surf, (50, 50))
        self.screen.blit(self.red_surf, (50, 900))
        self.screen.blit(self.red_surf, (900, 50))
        self.screen.blit(self.red_surf, (900, 900))

        self.screen.blit(self.green_surf, (350, 350))
        self.screen.blit(self.green_surf, (600, 350))
        self.screen.blit(self.green_surf, (350, 600))
        self.screen.blit(self.green_surf, (600, 600))
        """