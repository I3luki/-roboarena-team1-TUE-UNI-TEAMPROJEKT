import pygame

class Textures:

    STONE1 = None
    STONE2= None
    STONE3 = None
    STONE4 = None
    STONE5 = None
    STONE6 = None
    STONE7 = None

    CURSED_STONE1 = None
    CURSED_STONE2 = None
    CURSED_HOLE1 = None
    CURSED_HOLE2 = None
    CURSED_HOLE3 = None

    CACTUS1 = None
    BONE1 = None
    BONE2 = None
    BONE3 = None
    BONE4 = None
    BONE5 = None
    BONE6 = None
    BONE_RIB1 = None
    BONE_RIB2 = None

    LABYRINTH_WALL_VERTICAL = None
    LABYRINTH_WALL_HORIZONTAL = None
    LABYRINTH_WALL = None

    RUINS1 = None
    TREE_NORMAL = None
    TREE_DEAD = None
    TREE_FIR = None
    TREE_PALM = None
    CENTER_NORMAL1 = None
    CENTER_NORMAL2 = None
    CENTER_NORMAL3 = None
    CENTER_DEAD1 = None
    CENTER_DEAD2 = None
    CENTER_DEAD3 = None
    CENTER_PALM1 = None
    CENTER_PALM2 = None
    CENTER_PALM3 = None
    CENTER_FIR1 = None
    CENTER_FIR2 = None

    GROUND_STONE = None
    GROUND_LABYRINTH = None
    GROUND_DESERT = None
    GROUND_DIRT1 = None
    GROUND_GRASS_DOWN = None
    GROUND_GRASS_UP = None
    GROUND_GRASS_LEFT = None
    GROUND_GRASS_RIGHT = None
    GROUND_GRASS_UP_LEFT = None
    GROUND_GRASS_UP_RIGHT = None
    GROUND_GRASS_DOWN_LEFT = None
    GROUND_GRASS_DOWN_RIGHT = None

    GRASS_TILES = []

    LIGHTNING_ANIMATION = None
    TORNADO_ANIMATION = None

    LIGHTNING_SHADOW = None

    HEALING_ICON = None
    SPEED_ICON = None
    RANDOM_ICON = None
    ORB_ICON = None

    GOBLIN_WALK_ANIMATION = None
    GOBLIN_DEATH_ANIMATION = None
    BEE_WALK_ANIMATION = None
    BEE_DEATH_ANIMATION = None
    WOLF_WALK_ANIMATION = None
    WOLF_DEATH_ANIMATION = None
    SLIME_WALK_ANIMATION = None
    SLIME_DEATH_ANIMATION = None

    @classmethod
    def load_all(cls):
        """Lädt alle Texturen einmalig in den Speicher.
        MUSS nach pygame.display.set_mode() aufgerufen werden!"""

        print("Lade Texturen...")

        # --- Stone ---
        cls.GROUND_STONE = pygame.image.load("Sprites/ground_stone2.png").convert_alpha()
        cls.GROUND_STONE = pygame.transform.scale(cls.GROUND_STONE, (50, 50))

        cls.STONE1 = pygame.image.load("Sprites/Stone1.png").convert_alpha()
        cls.STONE2 = pygame.image.load("Sprites/Stone2.png").convert_alpha()
        cls.STONE3 = pygame.image.load("Sprites/Stone3.png").convert_alpha()
        cls.STONE4 = pygame.image.load("Sprites/Stone4.png").convert_alpha()
        cls.STONE5 = pygame.image.load("Sprites/Stone5.png").convert_alpha()
        cls.STONE6 = pygame.image.load("Sprites/Stone6.png").convert_alpha()
        cls.STONE7 = pygame.image.load("Sprites/Stone7.png").convert_alpha()

        # --- Desert ---
        cls.GROUND_DESERT = pygame.image.load("Sprites/ground_sand1.png").convert_alpha()
        cls.GROUND_DESERT = pygame.transform.scale(cls.GROUND_DESERT, (50, 50))

        cls.CACTUS1 = pygame.image.load("Sprites/Cactus1.png").convert_alpha()

        cls.BONE1 = pygame.image.load("Sprites/bone1.png").convert_alpha()
        cls.BONE2 = pygame.image.load("Sprites/bone2.png").convert_alpha()
        cls.BONE3 = pygame.image.load("Sprites/bone3.png").convert_alpha()
        cls.BONE4 = pygame.image.load("Sprites/bone4.png").convert_alpha()
        cls.BONE5 = pygame.image.load("Sprites/bone5.png").convert_alpha()
        cls.BONE6 = pygame.image.load("Sprites/bone6.png").convert_alpha()

        cls.BONE_RIB1 = pygame.image.load("Sprites/bonerib1.png").convert_alpha()
        cls.BONE_RIB2 = pygame.image.load("Sprites/bonerib2.png").convert_alpha()

        # --- Labyrinth ---
        cls.GROUND_LABYRINTH = pygame.image.load("Sprites/ground_labyrinth.png").convert_alpha()
        cls.GROUND_LABYRINTH = pygame.transform.scale(cls.GROUND_LABYRINTH, (87, 87))

        cls.LABYRINTH_WALL_VERTICAL = pygame.image.load("Sprites/labyrinth_wall_vertical.png").convert_alpha()
        cls.LABYRINTH_WALL_HORIZONTAL = pygame.image.load("Sprites/labyrinth_wall_horizontal.png").convert_alpha()
        cls.LABYRINTH_WALL = pygame.image.load("Sprites/labyrinth_wall3.png").convert_alpha()
        cls.LABYRINTH_WALL = pygame.transform.scale(cls.LABYRINTH_WALL, (20, 20))

        # --- Cursed ---

        cls.CURSED_STONE1 = pygame.image.load("Sprites/ground_cursed_stone1.png").convert_alpha()
        cls.CURSED_STONE2 = pygame.image.load("Sprites/ground_cursed_stone2.png").convert_alpha()
        cls.CURSED_HOLE1 = pygame.image.load("Sprites/ground_cursed_hole1.png").convert_alpha()
        cls.CURSED_HOLE2 = pygame.image.load("Sprites/ground_cursed_hole2.png").convert_alpha()
        cls.CURSED_HOLE3 = pygame.image.load("Sprites/ground_cursed_hole3.png").convert_alpha()

        raw_lightning_animation = load_spritesheet("Sprites/Lightning1.png", 64, 160, 1, 10, skip_cols=[2])
        cls.LIGHTNING_ANIMATION = animation_scaling(raw_lightning_animation, 2.0, 2.5)

        cls.LIGHTNING_SHADOW = pygame.image.load(
            "Sprites/lightning_shadow.png"
        ).convert_alpha()
        cls.LIGHTNING_SHADOW = pygame.transform.scale(cls.LIGHTNING_SHADOW, (60, 60))

        raw_tornado_animation = load_spritesheet("Sprites/tornado.png", 1048, 1048, 12, 5, skip_rows=[0,1,2])
        cls.TORNADO_ANIMATION = animation_scaling(raw_tornado_animation, 0.15, 0.15)

        # --- Middle Ground ---
        cls.GROUND_DIRT1 = pygame.image.load("Sprites/ground_dirt1.png").convert_alpha()
        cls.GROUND_DIRT1 = pygame.transform.scale(cls.GROUND_DIRT1, (53, 53))

        cls.GROUND_GRASS_DOWN = pygame.image.load("Sprites/ground_grass_down.png").convert_alpha()
        cls.GROUND_GRASS_DOWN = pygame.transform.scale(cls.GROUND_GRASS_DOWN, (53, 53))

        cls.GROUND_GRASS_UP = pygame.image.load("Sprites/ground_grass_up.png").convert_alpha()
        cls.GROUND_GRASS_UP = pygame.transform.scale(cls.GROUND_GRASS_UP, (53, 53))

        cls.GROUND_GRASS_LEFT = pygame.image.load("Sprites/ground_grass_left.png").convert_alpha()
        cls.GROUND_GRASS_LEFT = pygame.transform.scale(cls.GROUND_GRASS_LEFT, (53, 53))

        cls.GROUND_GRASS_RIGHT = pygame.image.load("Sprites/ground_grass_right.png").convert_alpha()
        cls.GROUND_GRASS_RIGHT = pygame.transform.scale(cls.GROUND_GRASS_RIGHT, (53, 53))

        cls.GROUND_GRASS_UP_LEFT = pygame.image.load("Sprites/ground_grass_up_left.png").convert_alpha()
        cls.GROUND_GRASS_UP_LEFT = pygame.transform.scale(cls.GROUND_GRASS_UP_LEFT, (53, 53))

        cls.GROUND_GRASS_UP_RIGHT = pygame.image.load("Sprites/ground_grass_up_right.png").convert_alpha()
        cls.GROUND_GRASS_UP_RIGHT = pygame.transform.scale(cls.GROUND_GRASS_UP_RIGHT, (53, 53))

        cls.GROUND_GRASS_DOWN_LEFT = pygame.image.load("Sprites/ground_grass_down_left.png").convert_alpha()
        cls.GROUND_GRASS_DOWN_LEFT = pygame.transform.scale(cls.GROUND_GRASS_DOWN_LEFT, (53, 53))

        cls.GROUND_GRASS_DOWN_RIGHT = pygame.image.load("Sprites/ground_grass_down_right.png").convert_alpha()
        cls.GROUND_GRASS_DOWN_RIGHT = pygame.transform.scale(cls.GROUND_GRASS_DOWN_RIGHT, (53, 53))

        cls.RUINS1 = pygame.image.load("Sprites/ruins1.png").convert_alpha()

        cls.TREE_NORMAL = pygame.image.load("Sprites/tree_normal.png").convert_alpha()
        cls.TREE_NORMAL = pygame.transform.scale(cls.TREE_NORMAL, (150, 150))

        cls.TREE_DEAD = pygame.image.load("Sprites/tree_dead.png").convert_alpha()
        cls.TREE_DEAD = pygame.transform.scale(cls.TREE_DEAD, (150, 150))

        cls.TREE_FIR = pygame.image.load("Sprites/tree_fir.png").convert_alpha()
        cls.TREE_FIR = pygame.transform.scale(cls.TREE_FIR, (150, 150))

        cls.TREE_PALM = pygame.image.load("Sprites/tree_palm.png").convert_alpha()
        cls.TREE_PALM = pygame.transform.scale(cls.TREE_PALM, (150, 150))

        cls.CENTER_NORMAL1 = pygame.image.load("Sprites/center_normal1.png").convert_alpha()
        cls.CENTER_NORMAL1 = pygame.transform.scale(cls.CENTER_NORMAL1, (130, 130))
        cls.CENTER_NORMAL2 = pygame.image.load("Sprites/center_normal2.png").convert_alpha()
        cls.CENTER_NORMAL2 = pygame.transform.scale(cls.CENTER_NORMAL2, (150, 150))
        cls.CENTER_NORMAL3 = pygame.image.load("Sprites/center_normal3.png").convert_alpha()
        cls.CENTER_NORMAL3 = pygame.transform.scale(cls.CENTER_NORMAL3, (80, 80))

        cls.CENTER_DEAD1 = pygame.image.load("Sprites/center_dead1.png").convert_alpha()
        cls.CENTER_DEAD1 = pygame.transform.scale(cls.CENTER_DEAD1, (200, 200))
        cls.CENTER_DEAD2 = pygame.image.load("Sprites/center_dead2.png").convert_alpha()
        cls.CENTER_DEAD2 = pygame.transform.scale(cls.CENTER_DEAD2, (150, 150))
        cls.CENTER_DEAD3 = pygame.image.load("Sprites/center_dead3.png").convert_alpha()
        cls.CENTER_DEAD3 = pygame.transform.scale(cls.CENTER_DEAD3, (150, 150))

        cls.CENTER_PALM1 = pygame.image.load("Sprites/center_palm1.png").convert_alpha()
        cls.CENTER_PALM1 = pygame.transform.scale(cls.CENTER_PALM1, (130, 130))
        cls.CENTER_PALM2 = pygame.image.load("Sprites/center_palm2.png").convert_alpha()
        cls.CENTER_PALM2 = pygame.transform.scale(cls.CENTER_PALM2, (150, 150))
        cls.CENTER_PALM3 = pygame.image.load("Sprites/center_palm3.png").convert_alpha()
        cls.CENTER_PALM3 = pygame.transform.scale(cls.CENTER_PALM3, (150, 150))

        cls.CENTER_FIR1 = pygame.image.load("Sprites/center_fir1.png").convert_alpha()
        cls.CENTER_FIR1 = pygame.transform.scale(cls.CENTER_FIR1, (80, 80))
        cls.CENTER_FIR2 = pygame.image.load("Sprites/center_fir2.png").convert_alpha()
        cls.CENTER_FIR2 = pygame.transform.scale(cls.CENTER_FIR2, (150, 150))

        cls.GRASS_TILES = pygame.image.load("Sprites/grass_tiles.png").convert_alpha()

        # --- Icons ---

        cls.HEALING_ICON = pygame.image.load("Sprites/healing_icon.png").convert_alpha()
        cls.HEALING_ICON = pygame.transform.scale(cls.HEALING_ICON, (30, 30))

        cls.SPEED_ICON = pygame.image.load("Sprites/speed_icon.png").convert_alpha()
        cls.SPEED_ICON = pygame.transform.scale(cls.SPEED_ICON, (23, 30))

        cls.RANDOM_ICON = pygame.image.load("Sprites/random_icon.png").convert_alpha()
        cls.RANDOM_ICON = pygame.transform.scale(cls.RANDOM_ICON, (20, 30))

        cls.ORB_ICON = pygame.image.load("Sprites/orb_yellow.png").convert_alpha()
        cls.ORB_ICON = pygame.transform.scale(cls.ORB_ICON, (30, 30))

        raw_grass_sheet = pygame.image.load("Sprites/grass_tiles.png").convert_alpha()
        tile_w = raw_grass_sheet.get_width() // 4
        tile_h = raw_grass_sheet.get_height() // 4

        cls.GRASS_TILES = []
        for row in range(4):
            for col in range(4):
                x = col * tile_w
                y = row * tile_h
                tile = raw_grass_sheet.subsurface(pygame.Rect(x, y, tile_w, tile_h))
                cls.GRASS_TILES.append(tile)

        # --- Enemy Animation ---
        raw_goblin_walk_animation = load_spritesheet("Sprites/goblin_walk_animation.png", 48, 48, 1, 6)
        cls.GOBLIN_WALK_ANIMATION = animation_scaling(raw_goblin_walk_animation, 2, 2)
        raw_goblin_death_animation = load_spritesheet("Sprites/goblin_death_animation.png", 48, 48, 1, 6)
        cls.GOBLIN_DEATH_ANIMATION = animation_scaling(raw_goblin_death_animation, 2, 2)

        raw_bee_walk_animation = load_spritesheet("Sprites/bee_walk_animation.png", 48, 48, 1, 6)
        cls.BEE_WALK_ANIMATION = animation_scaling(raw_bee_walk_animation, 2, 2)
        raw_bee_death_animation = load_spritesheet("Sprites/bee_death_animation.png", 48, 48, 1, 6)
        cls.BEE_DEATH_ANIMATION = animation_scaling(raw_bee_death_animation, 2, 2)

        raw_wolf_walk_animation = load_spritesheet("Sprites/wolf_walk_animation.png", 48, 48, 1, 6)
        cls.WOLF_WALK_ANIMATION = animation_scaling(raw_wolf_walk_animation, 2, 2)
        raw_wolf_death_animation = load_spritesheet("Sprites/wolf_death_animation.png", 48, 48, 1, 6)
        cls.WOLF_DEATH_ANIMATION = animation_scaling(raw_wolf_death_animation, 2, 2)

        raw_slime_walk_animation = load_spritesheet("Sprites/slime_walk_animation.png", 48, 48, 1, 6)
        cls.SLIME_WALK_ANIMATION = animation_scaling(raw_slime_walk_animation, 2, 2)
        raw_slime_death_animation = load_spritesheet("Sprites/slime_death_animation.png", 48, 48, 1, 6)
        cls.SLIME_DEATH_ANIMATION = animation_scaling(raw_slime_death_animation, 2, 2)

def load_spritesheet(filename, frame_width, frame_height, rows, cols, skip_cols=None, skip_rows=None, colorkey = None):
    """
    Lädt ein Spritesheet und schneidet es in eine Liste von Listen (Zeilen & Spalten)
    """
    if skip_cols is None:
        skip_cols = []

    if skip_rows is None:
        skip_rows = []

    raw_sheet = pygame.image.load(filename)
    if colorkey is not None:
        raw_sheet.set_colorkey(colorkey)

    sprite_sheet = raw_sheet.convert_alpha()

    animation_grid = []

    for row in range(rows):
        row_frames = []
        if row in skip_rows:
            continue

        for col in range(cols):
            # Von 0,1,2.. auf 1,2,3..
            # current_col_intuitive = col + 1

            # Wenn Spalte in Skipliste, überspringen
            if col in skip_cols:
                continue

            # Berechne die exakte Pixel-Position des aktuellen Frames
            x = col * frame_width
            y = row * frame_height

            # subsurface() schneidet ein "Fenster" aus dem Hauptbild heraus
            # Es kopiert das Bild nicht, sondern verweist darauf -> Extrem schnell!
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            row_frames.append(frame)

        animation_grid.append(row_frames)

    return animation_grid

def animation_scaling(grid, x_scale, y_scale):
    if y_scale is None:
        y_scale = x_scale

    return [
        [
            pygame.transform.scale(
                frame,
                (int(frame.get_width() * x_scale), int(frame.get_height() * y_scale))
            )
            for frame in row
        ]
        for row in grid
    ]