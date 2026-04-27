import pygame

# Gegensätzliche Richtungen definieren
def is_opposite_direction(current_direction, new_direction):
    opposite_directions = {
        "up": "down",
        "down": "up",
        "left": "right",
        "right": "left",
    }
    return opposite_directions.get(current_direction) == new_direction

# Tastenerkenung
def handle_keydown(event, current_direction):
    new_direction = current_direction

    if event.key in (pygame.K_w, pygame.K_UP):
        new_direction = "up"
    elif event.key in (pygame.K_s, pygame.K_DOWN):
        new_direction = "down"
    elif event.key in (pygame.K_a, pygame.K_LEFT):
        new_direction = "left"
    elif event.key in (pygame.K_d, pygame.K_RIGHT):
        new_direction = "right"
    # Gegensätzliche bewgungen verbieten
    if is_opposite_direction(current_direction, new_direction):
        return current_direction

    return new_direction