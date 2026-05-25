import pygame
from sys import exit
from Arena import Arena  # ← importieren
from Roboter import Robot
from Orb import Orb
from HealthSystem_Player import HealthSystem_Player
from StaminaSystem_Player import StaminaSystem_Player
from Enemy import Enemy
from Level import Level
TEST_MODE = False    # TESTMODE: wenn true, dann ist testmodus an

SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 2000


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RoboArena")
clock = pygame.time.Clock()

# Create arena object
arena = Arena(screen)
robot = Robot(arena, arena.WIDTH/2, arena.HEIGHT/2)   # spawne in der Mitte der Arena
orb_list = [Orb(arena,0,0), Orb(arena,0,0)]
enemy_list = [Enemy(arena,0,0), Enemy(arena,0,0)]

# randomize orb positions
for orb in orb_list:
    orb.randomize_position()
for enemy in enemy_list:
    enemy.randomize_position()





# Lebens-System:
health = HealthSystem_Player(screen, max_health=100, bar_x=10, bar_y=10, bar_width=400, bar_height=25)

# Stamina-System:
stamina = StaminaSystem_Player(screen, max_stamina=100, bar_x=10, bar_y=40, bar_width=400, bar_height=25)

# Level-system
level = Level(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    robot.move(keys)
    robot.update_rotation()
    arena.update_lightning_tiles(robot, health)
    arena.update_tornado(robot, health)

    # Checke für Kollision von Roboter und Orb
    for orb in orb_list[:]:
        if robot.aabb.check_collision(orb.aabb):
            level.collect_orb()
            orb.randomize_position()

    # Zeichne Objekte auf den Screen
    screen.fill((0, 0, 0))  # clear previous frame
    arena.draw(robot)
    robot.draw()
    for orb in orb_list:
        orb.draw()
    for enemy in enemy_list:
        enemy.draw()
        enemy.check_damage_player(robot,health)
    health.draw()
    stamina.draw()
    level.draw()
    pygame.display.flip() #update screen


    # Testmodus
    # "visualisiert ausgewählte hintergrundberechnungen und andere testbedingte werte"
    if(TEST_MODE):
        for orb in orb_list:
            orb.draw_aabb() 
        robot.draw_aabb()
        robot.draw_line_to_mouse()
        for enemy in enemy_list:
            enemy.draw_aabb()
            enemy.draw_line_enemy(robot)
        arena.draw_aabb()

    pygame.display.update()
    clock.tick(60)