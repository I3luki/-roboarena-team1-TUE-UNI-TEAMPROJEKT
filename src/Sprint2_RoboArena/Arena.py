import pygame
from Arena_Objects import Wall,Speedtile,Healthtile,Surprisetile,CactusTile,SkullTile,BoneTile, LightningTile, Tornado
from Camera import Camera

class Arena:


    def __init__(self, screen):

        self.screen = screen
        self.WIDTH = 3000
        self.HEIGHT = 3000
        self.camera = Camera(screen, 0, 0)


        # Hintergrund-Surfaces erstellen
        self.background_surf = pygame.Surface((self.WIDTH,self.HEIGHT))
        self.background_surf.fill((200, 200, 200))

        # Farbige Map-Zonen
        self.zones = [
            # Labyrinth oben links
            (0, 0, 1500, 1050, (180, 120, 220)),
            (0, 1050, 1050, 450, (180, 120, 220)),

            # Blitzland oben rechts
            (1500, 0, 1500, 1050, (255, 120, 120)),
            (1950, 1050, 1050, 450, (255, 120, 120)),

            # Wüste unten links
            (0, 1500, 1050, 450, (240, 190, 120)),
            (0, 1950, 1500, 1050, (240, 190, 120)),

            # Rochland unten rechts
            (1950, 1500, 1050, 450, (170, 170, 170)),
            (1500, 1950, 1500, 1050, (170, 170, 170)),

            # Healing Spawn Mitte
            (1050, 1050, 900, 900, (100, 230, 230)),
        ]

        # list of all walls
        #   a wall is (x, y, WIDTH, HEIGHT)
        self.walls = [
            # Außenrand
            Wall(self, 0, 0, 3000, 20),
            Wall(self, 0, 0, 20, 3000),
            Wall(self, 0, 2980, 3000, 20),
            Wall(self, 2980, 0, 20, 3000),

            # Labyrinth-Wände
            Wall(self, 80, 80, 160, 20),
            Wall(self, 80, 80, 20, 20),
            Wall(self, 320, 180, 180, 20),
            Wall(self, 440, 60, 20, 140),
            Wall(self, 440, 60, 180, 20),
            Wall(self, 780, 60, 420, 20),
            Wall(self, 780, 60, 20, 180),

            Wall(self, 920, 190, 20, 360),

            Wall(self, 920, 390, 360, 20),
            Wall(self, 1340, 60, 120, 20),
            Wall(self, 1400, 60, 20, 360),

            Wall(self, 120, 430, 240, 20),
            Wall(self, 120, 430, 20, 180),

            Wall(self, 210, 530, 20, 110),
            Wall(self, 440, 320, 240, 20),
            Wall(self, 440, 320, 20, 240),
            Wall(self, 620, 500, 20, 120),
            Wall(self, 620, 620, 120, 20),

            # Rechte Mitte
            Wall(self, 1120, 500, 240, 20),
            Wall(self, 1120, 500, 20, 250),

            Wall(self, 1260, 500, 20, 250),

            Wall(self, 1020, 500, 20, 180),
            Wall(self, 1320, 500, 120, 20),
            Wall(self, 1380, 690, 80, 20),
            Wall(self, 1440, 590, 20, 100),
            Wall(self, 1340, 590, 40, 40),
            Wall(self, 1000, 300, 170, 20),

            Wall(self, 1150, 180, 20, 120),

            Wall(self, 800, 300, 60, 100),
            Wall(self, 760, 450, 20, 100),
            Wall(self, 210, 260, 100, 100),

            Wall(self, 380, 200, 20, 80),

            Wall(self, 650, 120, 20, 130),
            Wall(self, 620, 700, 360, 20),
            Wall(self, 620, 700, 20, 120),

            Wall(self, 60, 750, 240, 20),
            Wall(self, 60, 750, 20, 180),
            Wall(self, 140, 870, 240, 20),

            Wall(self, 380, 690, 120, 20),
            Wall(self, 380, 690, 20, 120),

            Wall(self, 500, 690, 20, 120),

            Wall(self, 920, 810, 320, 20),
            Wall(self, 920, 810, 20, 180),
            Wall(self, 1120, 810, 20, 180),

            Wall(self, 1280, 890, 120, 20),
            Wall(self, 1400, 770, 20, 180),

            Wall(self, 1280, 890, 20, 60),
            Wall(self, 155, 945, 240, 20),
            Wall(self, 155, 945, 20, 300),

            Wall(self, 380, 1050, 360, 20),
            Wall(self, 380, 1050, 20, 240),
            Wall(self, 660, 930, 20, 260),

            Wall(self, 1000, 1050, 20, 180),
            Wall(self, 80, 1400, 180, 20),
            Wall(self, 80, 1280, 20, 120),

            Wall(self, 260, 1400, 20, 60),
            Wall(self, 580, 1180, 20, 120),
            Wall(self, 580, 1250, 280, 20),

            Wall(self, 860, 1250, 20, 120),

            Wall(self, 380, 1360, 300, 20),
            Wall(self, 750, 800, 80, 80),
            Wall(self, 800, 940, 20, 60),
            Wall(self, 500 , 900 , 20 , 150),
            Wall(self, 800, 1100, 250, 20),
            Wall(self, 250, 1100, 20, 300),


            # Wüste Wände

            Wall(self, 300, 2000, 100,100),

            Wall(self, 200, 2500,50,90),
            Wall(self, 900, 1700, 90,90),
            Wall(self, 700, 2500,50,100),
            Wall(self, 750, 2450,50,150),






        ]
        #Schabrettmusster für das Quadrat
        ROCK_SIZE = 100
        SPACING = 200

        # Quadrat unten rechts
        for row in range(5):
            for col in range(5):
                if (row + col) % 2 == 0:
                    x = 2050 + col * SPACING
                    y = 2050 + row * SPACING

                    self.walls.append(
                        Wall(self, x, y, ROCK_SIZE, ROCK_SIZE)
                    )


        # Rechteck oben rechts
        for row in range(2):
            for col in range(5):
                if (row + col) % 2 == 0:
                    x = 2050 + col * SPACING
                    y = 1550 + row * SPACING

                    self.walls.append(
                        Wall(self, x, y, ROCK_SIZE, ROCK_SIZE)
                    )


        # Rechteck links unten
        for row in range(5):
            for col in range(2):
                if (row + col) % 2 == 0:
                    x = 1550 + col * SPACING
                    y = 2050 + row * SPACING

                    self.walls.append(
                        Wall(self, x, y, ROCK_SIZE, ROCK_SIZE)
                    )

        # list of all tiles
        #   a tile is (x,y)
        self.tiles = [

            #Tile Labyrinth
            Healthtile(self, 500,500),
            Healthtile(self, 200, 100),
            Healthtile(self, 1200, 430),

            Speedtile(self, 200, 1000),
            Speedtile(self,1000,100),
            Speedtile(self, 900, 1200),

            Surprisetile(self, 500,500),
            Surprisetile(self, 800,900),

            # Wüsten-Tiles(Nur optik)
            CactusTile(self, 250, 1800),
            CactusTile(self, 500, 2200),
            CactusTile(self, 800, 2600),

            SkullTile(self, 700, 1900),
            SkullTile(self, 1000, 2400),

            BoneTile(self, 350, 2500),
            BoneTile(self, 1200, 2100),
            BoneTile(self, 900, 2800),

            #Tiles wüste
            Speedtile(self, 250, 1700),
            Speedtile(self, 700, 2100),
            Speedtile(self, 1200, 2600),

            Healthtile(self, 500, 1900),
            Healthtile(self, 950, 2300),
            Healthtile(self, 300, 2750),

            Surprisetile(self, 800, 1800),
            Surprisetile(self, 1100, 2000),
            Surprisetile(self, 600, 2500),




        ]

        #Lighting Tiles Anzahl
        self.lightning_tiles = [
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
            LightningTile(self)

       ]
        #Tornado Tiles
        self.tornado = Tornado(self)
    #Update Methode für Tornado 
    def update_tornado(self, robot, health):
        self.tornado.update(robot, health)

    #Update Mehtode für Lightning
    def update_lightning_tiles(self, robot, health):
        for lightning in self.lightning_tiles:
            lightning.update(robot, health)


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
            wall.draw()

    # draws all tiles which are in screen
    def draw_tiles(self):
        for tile in self.tiles:
            tile.draw()

    # Zeichen die Zonen
    def draw_zones(self):
        for x, y, width, height, color in self.zones:
            screen_x = x - self.camera.x + self.screen.get_width() / 2
            screen_y = y - self.camera.y + self.screen.get_height() / 2

            pygame.draw.rect(
                self.screen,
                color,
                (screen_x, screen_y, width, height)
            )

    # Zeichne alle Arena-Objekte und Hintergründe
    def draw(self, robot):

        # Zeichne Hintergrund
        self.camera.update(robot)

        self.screen.fill((0, 0, 0))

        self.draw_zones()
        self.draw_walls()
        self.draw_tiles()
        self.tornado.draw()

        #Blitze zeichen
        for lightning in self.lightning_tiles:
            lightning.draw()

    # Zeichne AABBs
    def draw_aabb(self):

        for tile in self.tiles:
            if(self.is_rect_onscreen(tile)):
                tile.draw_aabb()

        for wall in self.walls:
            if(self.is_rect_onscreen(wall)):
                wall.draw_aabb()

    