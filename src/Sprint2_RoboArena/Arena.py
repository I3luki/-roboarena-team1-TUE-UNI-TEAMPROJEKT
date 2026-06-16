import pygame
from Arena_Objects import Wall, Speedtile, Healthtile, Surprisetile, Cactus, SkullTile, BoneTile, LightningTile, \
    Tornado, Stone, CursedStone, CursedHole
from Camera import Camera
from Arena_Matrix import Arena_Matrix
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
from Textures import Textures

class Arena:


    def __init__(self, screen):

        self.screen = screen
        self.WIDTH = 3000
        self.HEIGHT = 3000
        self.camera = Camera(screen, 0, 0)
        WALL_THICKNESS = 20

        # Hintergrund-Surfaces erstellen
        self.background_surf = pygame.Surface((self.WIDTH,self.HEIGHT), pygame.SRCALPHA)

        tile_rocks_w = Textures.GROUND_ROCKS.get_width()
        tile_rocks_h = Textures.GROUND_ROCKS.get_height()

        rockland_area = [
            (1950, 1500, 1050, 450),
            (1500, 1950, 1500, 1050)
        ]

        # Rockland-Surfaces erstellen
        for rx, ry, width, height in rockland_area:
            for x in range(rx, rx + width, tile_rocks_w):
                for y in range(ry, ry + height, tile_rocks_h):
                    self.background_surf.blit(Textures.GROUND_ROCKS, (x, y))

        labyrinth_area = [
            (0, 0, 1500, 1050),
            (0, 1050, 1050, 450)
        ]

        tile_labyrinth_w = Textures.GROUND_LABYRINTH.get_width()
        tile_labyrinth_h = Textures.GROUND_LABYRINTH.get_height()

        # Labyrinth-Surfaces erstellen
        for lx, ly, width, height in labyrinth_area:
            for x in range(lx, lx + width, tile_labyrinth_w):
                for y in range(ly, ly + height, tile_labyrinth_h):
                    self.background_surf.blit(Textures.GROUND_LABYRINTH, (x, y))

        # Farbige Map-Zonen
        self.zones = [
            # Blitzland oben rechts
            (1500, 0, 1500, 1050, (157, 98, 89)),
            (1950, 1050, 1050, 450, (157, 98, 89)),

            # Wüste unten links
            (0, 1500, 1050, 450, (240, 190, 120)),
            (0, 1950, 1500, 1050, (240, 190, 120)),

            # Healing Spawn Mitte
            (1050, 1050, 900, 900, (100, 230, 230)),
        ]
        self.zone_surfaces = []

        for x, y, width, height, color in self.zones:
            surface = pygame.Surface((width, height))
            surface.fill(color)

            self.zone_surfaces.append((surface, x, y))


        # list of all walls
        #   a wall is (x, y, WIDTH, HEIGHT)
        self.walls = [
            # Außenrand
            Wall(self, 0, 0, 3000, WALL_THICKNESS),
            Wall(self, 0, 0, WALL_THICKNESS, 3000),
            Wall(self, 0, 2980, 3000, WALL_THICKNESS),
            Wall(self, 2980, 0, WALL_THICKNESS, 3000),

            # Horizontale Wände (nach x sortiert)
            Wall(self, 80, 750, 240, WALL_THICKNESS),
            Wall(self, 80, 80, 160, WALL_THICKNESS),
            Wall(self, 80, 1400, 180, WALL_THICKNESS),
            Wall(self, 120, 430, 240, WALL_THICKNESS),
            Wall(self, 155, 945, 240, WALL_THICKNESS),
            Wall(self, 320, 180, 180, WALL_THICKNESS),
            Wall(self, 380, 690, 120, WALL_THICKNESS),
            Wall(self, 380, 1050, 360, WALL_THICKNESS),
            Wall(self, 380, 1360, 300, WALL_THICKNESS),
            Wall(self, 440, 80, 180, WALL_THICKNESS),
            Wall(self, 440, 320, 240, WALL_THICKNESS),
            Wall(self, 580, 1250, 280, 20),
            Wall(self, 620, 620, 120, WALL_THICKNESS),
            Wall(self, 620, 700, 360, WALL_THICKNESS),
            Wall(self, 780, 80, 420, WALL_THICKNESS),
            Wall(self, 800, 1100, 250, WALL_THICKNESS),
            Wall(self, 920, 390, 360, WALL_THICKNESS),
            Wall(self, 920, 810, 320, WALL_THICKNESS),
            Wall(self, 1000, 300, 170, WALL_THICKNESS),
            Wall(self, 1120, 500, 240, WALL_THICKNESS),
            Wall(self, 1280, 890, 120, WALL_THICKNESS),
            Wall(self, 1320, 500, 120, WALL_THICKNESS),
            Wall(self, 1340, 80, 120, WALL_THICKNESS),
            Wall(self, 1380, 690, 80, WALL_THICKNESS),

            # Vertikale Wände (nach x sortiert)
            Wall(self, 80, 750, WALL_THICKNESS, 180),
            Wall(self, 80, 1280, WALL_THICKNESS, 120),
            Wall(self, 120, 430, WALL_THICKNESS, 180),
            Wall(self, 155, 945, WALL_THICKNESS, 300),
            Wall(self, 210, 530, WALL_THICKNESS, 110),
            Wall(self, 260, 1400, WALL_THICKNESS, 60),
            Wall(self, 380, 690, WALL_THICKNESS, 120),
            Wall(self, 380, 1050, WALL_THICKNESS, 240),
            Wall(self, 440, 80, WALL_THICKNESS, 120),
            Wall(self, 440, 320, WALL_THICKNESS, 240),
            Wall(self, 500, 690, WALL_THICKNESS, 120),
            Wall(self, 580, 1180, WALL_THICKNESS, 120),
            Wall(self, 620, 500, WALL_THICKNESS, 120),
            Wall(self, 620, 700, WALL_THICKNESS, 120),

            Wall(self, 760, 450, WALL_THICKNESS, 100),
            Wall(self, 780, 80, WALL_THICKNESS, 180),
            Wall(self, 800, 940, WALL_THICKNESS, 60),
            Wall(self, 860, 1250, WALL_THICKNESS, 120),
            Wall(self, 920, 190, WALL_THICKNESS, 360),
            Wall(self, 920, 810, WALL_THICKNESS, 180),
            Wall(self, 1000, 1050, WALL_THICKNESS, 180),

            Wall(self, 1120, 500, WALL_THICKNESS, 250),
            Wall(self, 1120, 810, WALL_THICKNESS, 180),
            Wall(self, 1150, 180, WALL_THICKNESS, 120),
            Wall(self, 1260, 500, WALL_THICKNESS, 250),
            Wall(self, 1280, 890, WALL_THICKNESS, 60),
            Wall(self, 1400, 80, WALL_THICKNESS, 360),
            Wall(self, 1400, 770, WALL_THICKNESS, 180),
            Wall(self, 1440, 590, WALL_THICKNESS, 100),

            # Blöcke (nach x sortiert)
            Wall(self, 210, 260, 100, 100),
            Wall(self, 750, 800, 80, 80),

            Wall(self, 1340, 590, 40, 40),

            # Wüste Wände

            Wall(self, 300, 2000, 100,100),

            Wall(self, 200, 2500,50,90),
            Wall(self, 900, 1700, 90,90),
            Wall(self, 700, 2500,50,100),
            Wall(self, 750, 2450,50,150),
        ]

        # --- Steine ---
        self.stones = []
        #Schabrettmuster für das Quadrat
        SPACING = 200

        # Quadrat unten rechts
        for row in range(5):
            for col in range(5):
                if (row + col) % 2 == 0:
                    x = 2050 + col * SPACING
                    y = 2050 + row * SPACING
                    self.stones.append(Stone(self, x, y))


        # Rechteck oben rechts
        for row in range(2):
            for col in range(5):
                if (row + col) % 2 == 0:
                    x = 2050 + col * SPACING
                    y = 1550 + row * SPACING
                    self.stones.append(Stone(self, x, y))


        # Rechteck links unten
        for row in range(5):
            for col in range(2):
                if (row + col) % 2 == 0:
                    x = 1550 + col * SPACING
                    y = 2050 + row * SPACING
                    self.stones.append(Stone(self, x, y))

        # Cactus Objekte
        self.cactus = [
            Cactus(self, 250, 1800),
            Cactus(self, 500, 2200),
            Cactus(self, 800, 2600)]

        # list of all tiles
        #   a tile is (x,y)
        self.tiles = [

            #Tile Labyrinth
            Healthtile(self, 200, 100),
            Healthtile(self, 1200, 430),

            Speedtile(self, 200, 1000),
            Speedtile(self,1000,100),
            Speedtile(self, 900, 1200),

            Surprisetile(self, 500,500),
            Surprisetile(self, 800,900),

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

        self.cursed_stones = [
            CursedStone(self, 1720, 280),
            CursedStone(self, 2510, 410),
            CursedStone(self, 1980, 790),
            CursedStone(self, 2440, 1220),
        ]

        self.cursed_holes = [
            CursedHole(self, 1910, 360),
            CursedHole(self, 2380, 180),
            CursedHole(self, 2200, 620),
            CursedHole(self, 2150, 1130),
        ]

        # Definiere grid matrix für Enemy Movement
        # Erstelle dafür all_obstacles mit allen Objekten, die als nicht begehbar gelten sollen
        all_obstacles = self.walls + self.stones + self.cactus+ self.cursed_stones + self.cursed_holes
        self.grid_matrix = Arena_Matrix().build_grid(self.WIDTH, self.HEIGHT, all_obstacles)

        # Grid und Finder nur einmal erstellen
        self.pf_grid = Grid(matrix=self.grid_matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

        #Tornado Tiles
        self.tornado = Tornado(self)



    #Update Methode für Tornado 
    def update_tornado(self, robot, health):
        self.tornado.update(robot, health)

    #Update Mehtode für Lightning
    def update_lightning_tiles(self, robot, health):
        for lightning in self.lightning_tiles:
            lightning.update(robot, health)

    # Updates all other Tiles
    def update_tiles(self):
        for tile in self.tiles:
            tile.update()

    # Updates everything
    def update(self, robot, health):
        self.update_tornado(robot, health)
        self.update_lightning_tiles(robot, health)
        self.update_tiles()


    # checks if a rectangle is visible on the screen
    def is_rect_onscreen(self, rect):
        min_x = self.camera.x - self.screen.get_width() / 2
        max_x = self.camera.x + self.screen.get_width() / 2

        min_y = self.camera.y - self.screen.get_height() / 2
        max_y = self.camera.y + self.screen.get_height() / 2

        return (
                rect.x + rect.width  >= min_x and
                rect.x               <= max_x and
                rect.y + rect.height >= min_y and
                rect.y               <= max_y
        )

    # draws all walls which are in screen
    def draw_walls(self):
        for wall in self.walls:
            wall.draw()
    # draws all stones which are in screen
    def draw_stones(self):
        for stone in self.stones:
            stone.draw()

    def draw_cursed_stones(self):
        for cursed_stone in self.cursed_stones:
            cursed_stone.draw()

    def draw_cursed_holes(self):
        for cursed_hole in self.cursed_holes:
            cursed_hole.draw()

    # draws all tiles which are in screen
    def draw_tiles(self):
        for tile in self.tiles:
            tile.draw()

    def draw_cactus(self):
        for cactus in self.cactus:
            cactus.draw()

    # Zeichen die Zonen
    def draw_zones(self):
        for surface, x, y in self.zone_surfaces:
            screen_x = x - self.camera.x + self.screen.get_width() / 2
            screen_y = y - self.camera.y + self.screen.get_height() / 2

            self.screen.blit(surface, (screen_x, screen_y))



    # Zeichne alle Arena-Objekte und Hintergründe
    def draw(self, robot):

        # Zeichne Hintergrund
        self.camera.update(robot)

        bg_x = 0 - self.camera.x + self.screen.get_width() / 2
        bg_y = 0 - self.camera.y + self.screen.get_height() / 2
        self.screen.blit(self.background_surf, (bg_x, bg_y))

        self.draw_zones()
        self.draw_walls()
        self.draw_stones()
        self.draw_cursed_stones()

        # --- Schwarze Vierecke unter den cursed holes zeichnen ---
        for hole in self.cursed_holes:
            # ERHÖHE diese Werte, um das Quadrat weiter nach unten/rechts zu schieben:
            move_horizontal = 15  # Erhöhe, wenn es noch weiter nach rechts soll
            move_vertical = 30  # Erhöhe, wenn es noch weiter nach unten soll

            # Berechnung inklusive Kamera und Feintuning
            screen_x = (hole.x - 32 + move_horizontal) - self.camera.x + self.screen.get_width() / 2
            screen_y = (hole.y - 32 + move_vertical) - self.camera.y + self.screen.get_height() / 2

            # Zeichne das 64x64 Quadrat
            pygame.draw.rect(self.screen, (0, 0, 0), (screen_x, screen_y, 64, 64))

        self.draw_cursed_holes()
        self.draw_tiles()
        self.tornado.draw()

        # Y-SORTIERUNG: Alle Objekte mit "Tiefe" in einer Liste sammeln
        render_queue = []

        # Steine hinzufügen
        render_queue.extend(self.stones)

        # Cactus hinzufügen
        render_queue.extend(self.cactus)

        render_queue.extend(self.cursed_stones)

        # Roboter (Spieler) hinzufügen
        render_queue.append(robot)

        # Tornado hinzufügen
        render_queue.append(self.tornado)

        # (Wenn Gegner hinzugefügt werden, kommen die auch hier rein: render_queue.extend(self.enemies))

        # Sortieren nach der Unterkante des Objekts (y + height)
        # Lambda nimmt jedes Objekt und schaut, wo seine "Füße" auf der Y-Achse stehen
        render_queue.sort(key=lambda obj: obj.y + obj.height)

        # Objekte von hinten nach vorne durchgehen und zeichnen
        for obj in render_queue:
            obj.draw()

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

        for stone in self.stones:
            if(self.is_rect_onscreen(stone)):
                stone.draw_aabb()