import pygame
from sys import exit
from Arena import Arena  # ← importieren
from Roboter import Robot
from Orb import Orb

TEST_MODE = True     # TESTMODE: wenn true, dann ist testmodus an

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RoboArena")
clock = pygame.time.Clock()

# Create arena object
arena = Arena(screen)
robot = Robot(screen, 475, 475)
orb_list = [Orb(screen,200,200), Orb(screen,600,400)]


# "Checkt ob zwei Boxen sich überschneiden"
#   Nimmt zwei aabb in der Form [(x,y),(x,y)]
#   Gibt true aus wenn sich aabbs schneiden
def check_collision(box1, box2):
    min1_x, min1_y   = box1[0] 
    max1_x, max1_y = box1[1]
    min2_x, min2_y   = box2[0] 
    max2_x, max2_y = box2[1] 

    return (
        min1_x < max2_x and
        max1_x > min2_x and
        min1_y < max2_y and
        max1_y > min2_y
    )


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    robot.move(keys)

    # Checke für Kollision
    for orb in orb_list[:]:
        if check_collision(robot.aabb, orb.aabb):
            orb_list.remove(orb)

    # Zeichne arena, roboter und orbs
    arena.draw()
    robot.draw()
    for orb in orb_list:
        orb.draw()


    # Testmodus
    # "visualisiert ausgewählte hintergrundberechnungen und andere testbedingte werte"
    if(TEST_MODE):
        for orb in orb_list:
            orb.draw_aabb()
        robot.draw_aabb()

    pygame.display.update()
    clock.tick(60)