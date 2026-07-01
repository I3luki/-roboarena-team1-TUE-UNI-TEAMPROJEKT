import pygame

from Arena_Objects import Wall, Speedtile, Healthtile, Surprisetile, LightningTile
from Camera import Camera
from Arena_Matrix import Arena_Matrix
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
from Textures import Textures


class ArenaLabyrinth:

    def __init__(self, screen, TEST_MODE=False):

        self.screen = screen
        self.TEST_MODE = TEST_MODE

        self.WIDTH = 1500
        self.HEIGHT = 1500

        self.camera = Camera(screen, 0, 0)

        self.stones = []
        self.cactus = []

        self.cursed_stones = []
        self.cursed_holes = []

        self.bones = []
        self.bone_ribs = []

        self.ruins = []

        self.trees_normal = []
        self.trees_dead = []
        self.trees_palm = []
        self.trees_fir = []

        self.center_normal = []
        self.center_dead = []
        self.center_palm = []
        self.center_fir = []
        self.player_spawn = (750, 750)

        self.tornado = None

        self.lightning_mode = "full_map"

        WALL_THICKNESS = 20

        # Hintergrund
        self.background_surf = pygame.Surface(
            (self.WIDTH, self.HEIGHT),
            pygame.SRCALPHA
        )

        tile_w = Textures.GROUND_LABYRINTH.get_width()
        tile_h = Textures.GROUND_LABYRINTH.get_height()

        for x in range(0, self.WIDTH, tile_w):
            for y in range(0, self.HEIGHT, tile_h):
                self.background_surf.blit(
                    Textures.GROUND_LABYRINTH,
                    (x, y)
                )

        # Außenwände
        self.walls = [
            Wall(self, 0, 0, 1500, WALL_THICKNESS),
            Wall(self, 0, 0, WALL_THICKNESS, 1500),
            Wall(self, 0, 1480, 1500, WALL_THICKNESS),
            Wall(self, 1480, 0, WALL_THICKNESS, 1500),

            # LABYRINTH-WÄNDE
            #Horinzontal
            Wall(self, 100, 120, 300, WALL_THICKNESS),
            Wall(self, 190, 200, 400, WALL_THICKNESS),
            Wall(self, 250 , 280, 200, WALL_THICKNESS),
            Wall(self, 250 , 350, 500, WALL_THICKNESS),
            Wall(self, 350 , 420, 500, WALL_THICKNESS),
            Wall(self, 250 , 600, 550, WALL_THICKNESS),
            Wall(self, 100 , 700, 530, WALL_THICKNESS),
            Wall(self, 120 , 780, 300, WALL_THICKNESS),
            Wall(self, 250 , 890, 200, WALL_THICKNESS),
            Wall(self, 140 , 970, 450, WALL_THICKNESS),
            Wall(self, 90 , 1070, 150, WALL_THICKNESS),
            Wall(self, 210 , 1150, 350, WALL_THICKNESS),
            Wall(self, 250 , 1280, 350, WALL_THICKNESS),
            Wall(self, 100 , 1380, 200, WALL_THICKNESS),

            Wall(self, 680 , 840, 350, WALL_THICKNESS),
            Wall(self, 700 , 150, 100, WALL_THICKNESS),
            Wall(self, 1000 , 370, 200, WALL_THICKNESS),
            Wall(self, 630 , 520, 250, WALL_THICKNESS),
            Wall(self, 700 , 720, 180, WALL_THICKNESS),
            Wall(self, 950 , 1000, 400, WALL_THICKNESS),
            Wall(self, 800 , 1150, 400, WALL_THICKNESS),
            Wall(self, 700 , 1300, 350, WALL_THICKNESS),
            Wall(self, 620 , 1400, 200, WALL_THICKNESS),
            Wall(self, 1200 , 100, 200, WALL_THICKNESS),
            Wall(self, 1100 , 200, 300, WALL_THICKNESS),
            Wall(self, 1000 , 700, 500, WALL_THICKNESS),
            Wall(self, 1200 , 1350, 200, WALL_THICKNESS),
            Wall(self, 700 , 240, 200, WALL_THICKNESS),
            Wall(self, 1030 , 900, 200, WALL_THICKNESS),

            Wall(self, 600 , 1050, 280, WALL_THICKNESS),
            Wall(self, 860 , 600, 300, WALL_THICKNESS),
            Wall(self, 1000 , 500, 270, WALL_THICKNESS),



            #Horinzontale
            Wall(self, 100 , 120,  WALL_THICKNESS, 300),
            Wall(self, 100 , 600,  WALL_THICKNESS, 300),
            Wall(self, 250 , 280,  WALL_THICKNESS, 70),
            Wall(self, 100 , 400,  WALL_THICKNESS, 300),
            Wall(self, 400 , 420,  WALL_THICKNESS, 180),
            Wall(self, 90 , 1070, WALL_THICKNESS, 150),
            Wall(self, 860 , 520, WALL_THICKNESS, 200),
            Wall(self, 280 , 1400, WALL_THICKNESS, 100),
            Wall(self, 850 , 250, WALL_THICKNESS, 190),
            Wall(self, 600 , 1280, WALL_THICKNESS, 140),
            Wall(self, 1200 , 1150, WALL_THICKNESS, 200),
            Wall(self, 1400 , 1120, WALL_THICKNESS, 250),
            Wall(self, 1300 , 820, WALL_THICKNESS, 200),
            Wall(self, 1010 , 850, WALL_THICKNESS, 70),
            Wall(self, 700 , 0, WALL_THICKNESS, 150),
            Wall(self, 800 , 1230, WALL_THICKNESS, 80),
            Wall(self, 590 , 970, WALL_THICKNESS, 100),
            Wall(self, 1000 , 150, WALL_THICKNESS, 220),
            Wall(self, 1000 , 500, WALL_THICKNESS, 100),
            Wall(self, 1050 , 1300, WALL_THICKNESS, 200),
            Wall(self, 1350 , 200, WALL_THICKNESS, 200),
            Wall(self, 1350 , 500, WALL_THICKNESS, 200),
            Wall(self, 1200 , 1000, WALL_THICKNESS, 200),




        ]


        self.tiles = [
            Healthtile(self, 200, 100),
            Healthtile(self, 1200, 430),
            Healthtile(self, 600, 900),
            Healthtile(self, 400, 1330),


            Speedtile(self, 200, 1000),
            Speedtile(self, 1000, 100),
            Speedtile(self, 1300, 1300),

            Surprisetile(self, 500, 500),
            Surprisetile(self, 1040, 730),
            Surprisetile(self, 1100, 1400),
        ]

        self.lightning_tiles = [
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
        ]

        self.all_obstacles = self.walls

        self.grid_matrix = Arena_Matrix().build_grid(
            self.WIDTH,
            self.HEIGHT,
            self.all_obstacles
        )

        self.pf_grid = Grid(matrix=self.grid_matrix)

        self.finder = AStarFinder(
            diagonal_movement=DiagonalMovement.only_when_no_obstacle
        )

    def update_lightning_tiles(self, robot, health):
        for lightning in self.lightning_tiles:
            lightning.update(robot, health)

    def update_tiles(self):
        for tile in self.tiles:
            tile.update()

    def update(self, robot, health):
        self.update_lightning_tiles(robot, health)
        self.update_tiles()

    def draw_walls(self):
        for wall in self.walls:
            wall.draw()

    def draw_tiles(self):
        for tile in self.tiles:
            tile.draw()

    def draw(self, robot):

        self.camera.update(robot)

        bg_x = -self.camera.x + self.screen.get_width() / 2
        bg_y = -self.camera.y + self.screen.get_height() / 2

        self.screen.blit(self.background_surf, (bg_x, bg_y))

        self.draw_walls()
        self.draw_tiles()

        for lightning in self.lightning_tiles:
            lightning.draw()

        robot.draw()

    def is_rect_onscreen(self, rect):

        min_x = self.camera.x - self.screen.get_width() / 2
        max_x = self.camera.x + self.screen.get_width() / 2

        min_y = self.camera.y - self.screen.get_height() / 2
        max_y = self.camera.y + self.screen.get_height() / 2

        return (
                rect.x + rect.width >= min_x and
                rect.x <= max_x and
                rect.y + rect.height >= min_y and
                rect.y <= max_y
        )

    def draw_aabb(self):

        for tile in self.tiles:
            if self.is_rect_onscreen(tile):
                tile.draw_aabb()

        for wall in self.walls:
            if self.is_rect_onscreen(wall):
                wall.draw_aabb()