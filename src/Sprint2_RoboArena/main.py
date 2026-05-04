import pygame
from sys import exit

pygame.init()
window_width = 1000
window_height = 1000
block_size = 50

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("RoboArena")
clock = pygame.time.Clock()

# Create background
background_surf = pygame.Surface(screen.get_size())
background_surf.fill((200, 200, 200))

# Create walls
wall_surf = pygame.Surface((50, 50))
wall_surf.fill((44, 44, 44))

# Create obstacles
red_obstacle_surf = pygame.Surface((50, 50))
red_obstacle_surf.fill((255, 0, 0))

blue_obstacle_surf = pygame.Surface((50, 50))
blue_obstacle_surf.fill((0, 0, 255))

green_obstacle_surf = pygame.Surface((50, 50))
green_obstacle_surf.fill((0, 255, 0))

yellow_obstacle_surf = pygame.Surface((50, 50))
yellow_obstacle_surf.fill((255, 255, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Paint background
    screen.blit(background_surf, (0, 0))

    # Paint walls
    for x in range(0, 1000, 50):
        screen.blit(wall_surf, (x, 0))  # oben
        screen.blit(wall_surf, (x, 950))  # unten

    for y in range(0, 1000, 50):
        screen.blit(wall_surf, (0, y))  # links
        screen.blit(wall_surf, (950, y))  # rechts

    # Paint obstacles
    for x in range(200, 400, 50):
        screen.blit(blue_obstacle_surf, (x, 200))  # oben
        screen.blit(blue_obstacle_surf, (x, 750))  # unten
    for x in range(600, 800, 50):
        screen.blit(blue_obstacle_surf, (x, 200))  # oben
        screen.blit(blue_obstacle_surf, (x, 750))  # unten

    for y in range(200, 400, 50):
        screen.blit(blue_obstacle_surf, (200, y))  # links
        screen.blit(blue_obstacle_surf, (750, y))  # rechts
    for y in range(600, 800, 50):
        screen.blit(blue_obstacle_surf, (200, y))  # links
        screen.blit(blue_obstacle_surf, (750, y))  # rechts

    screen.blit(yellow_obstacle_surf, (475, 475))

    screen.blit(red_obstacle_surf, (50, 50))
    screen.blit(red_obstacle_surf, (50, 900))
    screen.blit(red_obstacle_surf, (900, 50))
    screen.blit(red_obstacle_surf, (900, 900))

    screen.blit(green_obstacle_surf, (350, 350))
    screen.blit(green_obstacle_surf, (600, 350))
    screen.blit(green_obstacle_surf, (350, 600))
    screen.blit(green_obstacle_surf, (600, 600))

    pygame.display.update()
    clock.tick(60)

