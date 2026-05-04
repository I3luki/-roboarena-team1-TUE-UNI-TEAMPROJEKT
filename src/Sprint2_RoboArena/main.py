import pygame
from sys import exit
from Arena import Arena  # ← importieren

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("RoboArena")
clock = pygame.time.Clock()

# Create arena object
arena = Arena(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Draw arena
    arena.draw()

    pygame.display.update()
    clock.tick(60)