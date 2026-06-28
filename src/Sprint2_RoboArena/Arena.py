import pygame
import random
from Arena_Objects import Wall, Speedtile, Healthtile, Surprisetile, Cactus, LightningTile, \
    Tornado, Stone, CursedStone, CursedHole, Bone, Bone_Rib, Ruins, Tree_Dead, Tree_Normal, Tree_Palm, Tree_Fir, \
    Center_Normal, Center_Dead, Center_Palm, Center_Fir
from Camera import Camera
from Arena_Matrix import Arena_Matrix
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder
from Textures import Textures

class Arena:


    def __init__(self, screen, TEST_MODE = False):

        self.screen = screen
        self.TEST_MODE = TEST_MODE
        self.WIDTH = 3000
        self.HEIGHT = 3000
        self.camera = Camera(screen, 0, 0)
        WALL_THICKNESS = 20
        self.player_spawn = (1500, 1600)
        self.lightning_mode = "zone"


        # Hintergrund-Surfaces erstellen
        self.background_surf = pygame.Surface((self.WIDTH,self.HEIGHT), pygame.SRCALPHA)

        tile_rocks_w = Textures.GROUND_STONE.get_width()
        tile_rocks_h = Textures.GROUND_STONE.get_height()

        rockland_area = [
            (1950, 1500, 1050, 450),
            (1500, 1950, 1500, 1050)
        ]

        # Rockland-Surfaces erstellen
        for rx, ry, width, height in rockland_area:
            for x in range(rx, rx + width, tile_rocks_w):
                for y in range(ry, ry + height, tile_rocks_h):
                    self.background_surf.blit(Textures.GROUND_STONE, (x, y))

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

        # Wüste unten links
        desert_area = [
            (0, 1500, 1050, 450),
            (0, 1950, 1500, 1050)
        ]

        tile_desert_w = Textures.GROUND_DESERT.get_width()
        tile_desert_h = Textures.GROUND_DESERT.get_height()

        # Desert-Surfaces erstellen
        for lx, ly, width, height in desert_area:
            for x in range(lx, lx + width, tile_desert_w):
                for y in range(ly, ly + height, tile_desert_h):
                    self.background_surf.blit(Textures.GROUND_DESERT, (x, y))

        # Farbige Map-Zonen
        self.zones = [
            # Blitzland oben rechts
            (1500, 0, 1500, 1050, (157, 98, 89)),
            (1950, 1050, 1050, 450, (157, 98, 89)),

            # Healing Spawn Mitte
            (1050, 1050, 900, 900, "GRASS")
        ]
        self.zone_surfaces = []

        for x, y, width, height, zone_type in self.zones:
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            if zone_type == "GRASS":
                surface.fill((166, 176, 79))
                # --- INTEGRATION: Fülle die Healing-Zone mit zufälligen Gras-Tiles ---
                tile_size = 50  # Gewünschte Anzeigegröße der Kacheln auf der Map
                if Textures.GRASS_TILES:
                    for tx in range(0, width, tile_size):
                        for ty in range(0, height, tile_size):
                            # Zufällige Kachel wählen & auf Map-Größe skalieren
                            rand_tile = random.choice(Textures.GRASS_TILES)
                            scaled_tile = pygame.transform.scale(rand_tile, (tile_size, tile_size))
                            surface.blit(scaled_tile, (tx, ty))
                else:
                    # Fallback, falls die Texturen nicht geladen wurden
                    surface.fill((166, 176, 79))
            else:
                # Normale Farbzone (z.B. Blitzland)
                surface.fill(zone_type)

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
            Cactus(self, 800, 2100),
            Cactus(self, 1000, 2600)
        ]

        self.bones = [
            Bone(self, 350, 2500),
            Bone(self, 1200, 2100),
            Bone(self, 900, 2800),
            Bone(self, 250, 2300)
        ]

        self.bone_ribs = [
            Bone_Rib(self, 600, 1700),
            Bone_Rib(self, 1000, 2400)
        ]

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

        self.ruins = [
            Ruins(self, 1450, 1400),
        ]

        self.trees_normal = [
            Tree_Normal(self, 1150, 1150),
        ]

        self.trees_dead = [
            Tree_Dead(self, 1800, 1150),
        ]

        self.trees_palm = [
            Tree_Palm(self, 1150, 1800),
        ]

        self.trees_fir = [
            Tree_Fir(self, 1800, 1800),
        ]

        self.center_normal = [
            Center_Normal(self, 1100, 1300),
            Center_Normal(self, 1300, 1100),
        ]

        self.center_dead = [
            Center_Dead(self, 1800, 1300),
            Center_Dead(self, 1630, 1100),
        ]

        self.center_palm = [
            Center_Palm(self, 1150, 1650),
            Center_Palm(self, 1350, 1800),
        ]

        self.center_fir = [
            Center_Fir(self, 1650, 1770),
            Center_Fir(self, 1850, 1670),
        ]

        # Definiere grid matrix für Enemy Movement
        # Erstelle dafür all_obstacles mit allen Objekten, die als nicht begehbar gelten sollen
        all_obstacles = self.walls + self.stones + self.cactus + self.cursed_stones + self.cursed_holes \
                + self.bones + self.bone_ribs + self.ruins + self.trees_normal + self.trees_dead + self.trees_palm \
                + self.trees_fir + self.center_normal + self.center_dead + self.center_palm + self.center_fir
        self.grid_matrix = Arena_Matrix().build_grid(self.WIDTH, self.HEIGHT, all_obstacles)

        # Grid und Finder nur einmal erstellen
        self.pf_grid = Grid(matrix=self.grid_matrix)
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

        #Tornado Tiles
        self.tornado = Tornado(self)

        self.enemy_manager = None



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

    def draw_bones(self):
        for bone in self.bones:
            bone.draw()

    def draw_ruins(self):
        for ruins in self.ruins:
            ruins.draw()

    def draw_tree_normal(self):
        for tree_normal in self.trees_normal:
            tree_normal.draw()

    def draw_tree_dead(self):
        for tree_dead in self.trees_dead:
            tree_dead.draw()

    def draw_tree_palm(self):
        for tree_palm in self.trees_palm:
            tree_palm.draw()

    def draw_tree_fir(self):
        for tree_fir in self.trees_fir:
            tree_fir.draw()

    def draw_center_normal(self):
        for center_normal in self.center_normal:
            center_normal.draw()

    def draw_center_dead(self):
        for center_dead in self.center_dead:
            center_dead.draw()

    def draw_center_palm(self):
        for center_palm in self.center_palm:
            center_palm.draw()

    def draw_center_fir(self):
        for center_fir in self.center_fir:
            center_fir.draw()

    # Zeichen die Zonen
    def draw_zones(self):
        for surface, x, y in self.zone_surfaces:
            screen_x = x - self.camera.x + self.screen.get_width() / 2
            screen_y = y - self.camera.y + self.screen.get_height() / 2

            self.screen.blit(surface, (screen_x, screen_y))

    def draw_center(self):
        tile_w = Textures.GROUND_DIRT1.get_width()
        tile_h = Textures.GROUND_DIRT1.get_height()

        # Der absolute Mittelpunkt der 3000x3000-Map
        center_x = 1500
        center_y = 1500

        # Startkoordinate des exakten zentralen Tiles
        mid_tile_x = center_x - tile_w // 2
        mid_tile_y = center_y - tile_h // 2

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        # Dictionary, das alle Kacheln temporär speichert (Key: (col, row), Value: Texture)
        tiles = {}

        # 1. Das zentrale 7x7 Dirt-Quadrat (-3 bis 3)
        for row in range(-3, 4):
            for col in range(-3, 4):
                tiles[(col, row)] = Textures.GROUND_DIRT1

        # 2. Der standardmäßige 9x9 Gras-Außenrahmen
        for col in range(-4, 5):
            # Oben
            if col == -4:
                tiles[(-4, -4)] = Textures.GROUND_GRASS_UP_LEFT
            elif col == 4:
                tiles[(4, -4)] = Textures.GROUND_GRASS_UP_RIGHT
            else:
                tiles[(col, -4)] = Textures.GROUND_GRASS_UP

            # Unten
            if col == -4:
                tiles[(-4, 4)] = Textures.GROUND_GRASS_DOWN_LEFT
            elif col == 4:
                tiles[(4, 4)] = Textures.GROUND_GRASS_DOWN_RIGHT
            else:
                tiles[(col, 4)] = Textures.GROUND_GRASS_DOWN

        for row in range(-3, 4):
            tiles[(-4, row)] = Textures.GROUND_GRASS_LEFT
            tiles[(4, row)] = Textures.GROUND_GRASS_RIGHT

        # Die 4 Wege generieren
        max_reach = 8

        # --- Linker Weg (col von -max_reach bis -4) ---
        for col in range(-max_reach, -3):
            tiles[(col, 0)] = Textures.GROUND_DIRT1
            if col == -4:  # Die Verbindung zum Quadrat
                tiles[(col, -1)] = Textures.GROUND_GRASS_UP_LEFT
                tiles[(col, 1)] = Textures.GROUND_GRASS_DOWN_LEFT
            else:
                tiles[(col, -1)] = Textures.GROUND_GRASS_UP
                tiles[(col, 1)] = Textures.GROUND_GRASS_DOWN

        # --- Rechter Weg (col von 4 to max_reach) ---
        for col in range(4, max_reach + 1):
            tiles[(col, 0)] = Textures.GROUND_DIRT1
            if col == 4:  # Die Verbindung zum Quadrat
                tiles[(col, -1)] = Textures.GROUND_GRASS_UP_RIGHT
                tiles[(col, 1)] = Textures.GROUND_GRASS_DOWN_RIGHT
            else:
                tiles[(col, -1)] = Textures.GROUND_GRASS_UP
                tiles[(col, 1)] = Textures.GROUND_GRASS_DOWN

        # --- Oberer Weg (row von -max_reach bis -4) ---
        for row in range(-max_reach, -3):
            tiles[(0, row)] = Textures.GROUND_DIRT1
            if row == -4:  # Die Verbindung zum Quadrat
                tiles[(-1, row)] = Textures.GROUND_GRASS_UP_LEFT
                tiles[(1, row)] = Textures.GROUND_GRASS_UP_RIGHT
            else:
                tiles[(-1, row)] = Textures.GROUND_GRASS_LEFT
                tiles[(1, row)] = Textures.GROUND_GRASS_RIGHT

        # --- Unterer Weg (row von 4 bis max_reach) ---
        for row in range(4, max_reach + 1):
            tiles[(0, row)] = Textures.GROUND_DIRT1
            if row == 4:  # Die Verbindung zum Quadrat
                tiles[(-1, row)] = Textures.GROUND_GRASS_DOWN_LEFT
                tiles[(1, row)] = Textures.GROUND_GRASS_DOWN_RIGHT
            else:
                tiles[(-1, row)] = Textures.GROUND_GRASS_LEFT
                tiles[(1, row)] = Textures.GROUND_GRASS_RIGHT

        # Bestimmte Kacheln explizit mit Dirt-Tiles überschreiben
        specific_dirt_tiles = [(-4, -1), (-4, 1), (-2, 4), (1, 4), (-1, -4), (1, -4), (4, -1), (4, 1), (-1, 4)]
        for c, r in specific_dirt_tiles:
            tiles[(c, r)] = Textures.GROUND_DIRT1

        # Alle berechneten Tiles auf den Screen blitten
        for (col, row), texture in tiles.items():
            world_x = mid_tile_x + (col * tile_w)
            world_y = mid_tile_y + (row * tile_h)

            screen_x = world_x - self.camera.x + screen_w / 2
            screen_y = world_y - self.camera.y + screen_h / 2

            # Frustum Culling: Rendere nur, was im sichtbaren Bildschirmbereich liegt
            if -tile_w <= screen_x <= screen_w and -tile_h <= screen_y <= screen_h:
                self.screen.blit(texture, (screen_x, screen_y))

    # Zeichne alle Arena-Objekte und Hintergründe
    def draw(self, robot):

        # Zeichne Hintergrund
        self.camera.update(robot)

        bg_x = 0 - self.camera.x + self.screen.get_width() / 2
        bg_y = 0 - self.camera.y + self.screen.get_height() / 2
        self.screen.blit(self.background_surf, (bg_x, bg_y))

        self.draw_zones()
        self.draw_center()
        self.draw_walls()

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

        render_queue.extend(self.bone_ribs)

        render_queue.extend(self.bones)

        render_queue.extend(self.cursed_stones)

        render_queue.extend(self.ruins)

        render_queue.extend(self.trees_normal)
        render_queue.extend(self.trees_dead)
        render_queue.extend(self.trees_palm)
        render_queue.extend(self.trees_fir)

        render_queue.extend(self.center_normal)
        render_queue.extend(self.center_dead)
        render_queue.extend(self.center_palm)
        render_queue.extend(self.center_fir)

        # Roboter (Spieler) hinzufügen
        render_queue.append(robot)

        # Gegner hinzufügen
        render_queue.extend(self.enemy_manager.enemies)

        # Tornado hinzufügen
        render_queue.append(self.tornado)

        # (Wenn Gegner hinzugefügt werden, kommen die auch hier rein: render_queue.extend(self.enemies))

        # Sortieren nach der Unterkante des Objekts (y + height)
        # Lambda nimmt jedes Objekt und schaut, wo seine "Füße" auf der Y-Achse stehen
        render_queue.sort(key=lambda obj: obj.y + getattr(obj, 'sort_offset', getattr(obj, 'height', 0)))

        # Objekte von hinten nach vorne durchgehen und zeichnen
        for obj in render_queue:
            obj.draw()

        for lightning in self.lightning_tiles:
            lightning.draw()

        if self.TEST_MODE:
            self.draw_aabb()




    # Zeichne AABBs
    def draw_aabb(self):

        for tile in self.tiles:
            if self.is_rect_onscreen(tile):
                tile.draw_aabb()

        for wall in self.walls:
            if self.is_rect_onscreen(wall):
                wall.draw_aabb()

        for stone in self.stones:
            if self.is_rect_onscreen(stone):
                stone.draw_aabb()

        for bone in self.bones:
            if self.is_rect_onscreen(bone):
                bone.draw_aabb()

        for cactus in self.cactus:
            if self.is_rect_onscreen(cactus):
                cactus.draw_aabb()

        for bone_rib in self.bone_ribs:
            if self.is_rect_onscreen(bone_rib):
                bone_rib.draw_aabb()

        for ruins in self.ruins:
            if self.is_rect_onscreen(ruins):
                ruins.draw_aabb()