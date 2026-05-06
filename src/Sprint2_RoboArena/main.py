import pygame
from sys import exit
from Arena import Arena  # ← importieren
from Roboter import Robot

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("RoboArena")
clock = pygame.time.Clock()

# Create arena object
arena = Arena(screen)
robot = Robot(screen, 475, 475)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    robot.move(keys)

    # Draw arena
    arena.draw()
    robot.draw()

    pygame.display.update()
    clock.tick(60)