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

        self.WIDTH = 2000
        self.HEIGHT = 2000

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
        self.player_spawn = (1000, 1000)

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
            Wall(self, 0, 0, 2000, WALL_THICKNESS),
            Wall(self, 0, 0, WALL_THICKNESS, 2000),
            Wall(self, 0, 1980, 2000, WALL_THICKNESS),
            Wall(self, 1980, 0, WALL_THICKNESS, 2000),

            # HIER DEINE LABYRINTH-WÄNDE EINFÜGEN
        ]

        self.tiles = [
            Healthtile(self, 200, 100),
            Healthtile(self, 1200, 430),

            Speedtile(self, 200, 1000),
            Speedtile(self, 1000, 100),

            Surprisetile(self, 500, 500),
            Surprisetile(self, 800, 900),
        ]

        self.lightning_tiles = [
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
            LightningTile(self),
        ]

        all_obstacles = self.walls

        self.grid_matrix = Arena_Matrix().build_grid(
            self.WIDTH,
            self.HEIGHT,
            all_obstacles
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