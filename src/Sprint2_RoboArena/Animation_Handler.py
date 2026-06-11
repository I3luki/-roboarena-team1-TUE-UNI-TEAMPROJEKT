import pygame

def load_spritesheet(filename, frame_width, frame_height, rows, cols):
    """
    Lädt ein Spritesheet und schneidet es in eine Liste von Listen (Zeilen & Spalten)
    """
    # .convert_alpha() ist wichtig, damit die Transparenz performant geladen wird
    sprite_sheet = pygame.image.load(filename).convert_alpha()

    animation_grid = []

    for row in range(rows):
        row_frames = []
        for col in range(cols):
            # Berechne die exakte Pixel-Position des aktuellen Frames
            x = col * frame_width
            y = row * frame_height

            # subsurface() schneidet ein "Fenster" aus dem Hauptbild heraus
            # Es kopiert das Bild nicht, sondern verweist darauf -> Extrem schnell!
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            row_frames.append(frame)

        animation_grid.append(row_frames)

    return animation_grid

def animation_scaling(grid, scale):
    new_width = int(64 * scale)
    new_height = int(64 * scale)
    return [
            [
                pygame.transform.scale(frame, (new_width, new_height))
                for frame in row
            ]
            for row in grid
        ]