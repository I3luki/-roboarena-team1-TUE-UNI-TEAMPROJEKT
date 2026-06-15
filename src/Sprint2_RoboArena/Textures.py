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
    LIGHTNING_ANIMATION = None
    GROUND_ROCKS = None
    GROUND_LABYRINTH = None
    CURSED_STONE1 = None
    CURSED_STONE2 = None
    CURSED_HOLE1 = None
    CURSED_HOLE2 = None
    CURSED_HOLE3 = None

    @classmethod
    def load_all(cls):
        """Lädt alle Texturen einmalig in den Speicher.
        MUSS nach pygame.display.set_mode() aufgerufen werden!"""

        print("Lade Texturen...")

        cls.CACTUS1 = pygame.image.load("Sprites/Cactus1.png").convert_alpha()
        cls.CACTUS1 = pygame.transform.scale(cls.CACTUS1, (80, 80))

        cls.STONE1 = pygame.image.load("Sprites/Stone1.png").convert_alpha()
        cls.STONE2 = pygame.image.load("Sprites/Stone2.png").convert_alpha()
        cls.STONE3 = pygame.image.load("Sprites/Stone3.png").convert_alpha()
        cls.STONE4 = pygame.image.load("Sprites/Stone4.png").convert_alpha()
        cls.STONE5 = pygame.image.load("Sprites/Stone5.png").convert_alpha()
        cls.STONE6 = pygame.image.load("Sprites/Stone6.png").convert_alpha()
        cls.STONE7 = pygame.image.load("Sprites/Stone7.png").convert_alpha()

        raw_lightning_animation = load_spritesheet("Sprites/Lightning1.png", 64, 160, 1, 10, skip_cols=[2])
        cls.LIGHTNING_ANIMATION = animation_scaling(raw_lightning_animation, 2.0, 2.5)

        cls.GROUND_ROCKS = pygame.image.load("Sprites/ground_rocks1.png").convert_alpha()
        cls.GROUND_ROCKS = pygame.transform.scale(cls.GROUND_ROCKS, (50, 50))

        rocks_full_sheet = pygame.image.load("Sprites/ground_rocks_all.png").convert_alpha()

        cls.GROUND_LABYRINTH = pygame.image.load("Sprites/ground_labyrinth.png").convert_alpha()
        cls.GROUND_LABYRINTH = pygame.transform.scale(cls.GROUND_LABYRINTH, (80, 80))

        cls.CURSED_STONE1 = pygame.image.load("Sprites/ground_cursed_stone1.png").convert_alpha()
        cls.CURSED_STONE2 = pygame.image.load("Sprites/ground_cursed_stone2.png").convert_alpha()
        cls.CURSED_HOLE1 = pygame.image.load("Sprites/ground_cursed_hole1.png").convert_alpha()
        cls.CURSED_HOLE2 = pygame.image.load("Sprites/ground_cursed_hole2.png").convert_alpha()
        cls.CURSED_HOLE3 = pygame.image.load("Sprites/ground_cursed_hole3.png").convert_alpha()




def load_spritesheet(filename, frame_width, frame_height, rows, cols, skip_cols=None, colorkey = (0,0,0)):
    """
    Lädt ein Spritesheet und schneidet es in eine Liste von Listen (Zeilen & Spalten)
    """
    if skip_cols is None:
        skip_cols = []

    raw_sheet = pygame.image.load(filename)
    if colorkey is not None:
        raw_sheet.set_colorkey(colorkey)

    sprite_sheet = raw_sheet.convert_alpha()
    sheet_width = sprite_sheet.get_width()
    sheet_height = sprite_sheet.get_height()

    animation_grid = []

    for row in range(rows):
        row_frames = []
        for col in range(cols):
            # Von 0,1,2.. auf 1,2,3..
            current_col_intuitive = col + 1
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