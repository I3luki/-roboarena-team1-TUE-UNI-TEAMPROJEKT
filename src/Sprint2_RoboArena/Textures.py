import pygame

class Textures:
    CACTUS1 = None
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

    LIGHTNING_ANIMATION = None
    TORNADO_ANIMATION = None

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



def load_spritesheet(filename, frame_width, frame_height, rows, cols, skip_cols=None, skip_rows=None, colorkey = (0,0,0)):
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