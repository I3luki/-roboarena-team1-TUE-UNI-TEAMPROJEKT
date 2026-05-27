import pygame
from sys import exit
from Arena import Arena
from Roboter import Robot
from Orb import Orb
from HealthSystem_Player import HealthSystem_Player
from StaminaSystem_Player import StaminaSystem_Player
from EnemyManager import EnemyManager
from Level import Level
TEST_MODE = False    # TESTMODE: wenn true, dann ist testmodus an

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RoboArena")
clock = pygame.time.Clock()

# Lebens-System:
health = HealthSystem_Player(screen, max_health=100, bar_x=10, bar_y=10, bar_width=400, bar_height=25)
# Stamina-System:
stamina = StaminaSystem_Player(screen, max_stamina=100, bar_x=10, bar_y=40, bar_width=400, bar_height=25)
# Level-system
level = Level(screen)

# Create arena object
arena = Arena(screen)
robot = Robot(arena, health, stamina, level, arena.WIDTH/2, arena.HEIGHT/2)   # spawne in der Mitte der Arena
arena.camera.x = robot.x # lässt kamera auf roboter spawnen
arena.camera.y = robot.y # lässt kamera auf roboter spawnen

orb_list = [Orb(arena,0,0), Orb(arena,0,0)]
enemy_manager = EnemyManager(arena)
for _ in range(2):
    enemy_manager.add_enemy(0, 0)

# randomize orb/enemy positions
for orb in orb_list:
    orb.randomize_position()
for enemy in enemy_manager.enemies:
    enemy.randomize_position()



while True:

    #Events-Bereich
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Input-Berreich
    keys = pygame.key.get_pressed()

    #Updates-Berreich
    robot.move(keys)
    robot.update_rotation()
    arena.update_lightning_tiles(robot, health)
    arena.update_tornado(robot, health)

    # Fügt Orb zur Orbliste hinzu, wenn Gegner stirbt
    dead_positions = enemy_manager.get_dead_positions()
    for x,y in dead_positions:
        new_orb = Orb(arena,x,y)
        orb_list.append(new_orb)
    # Updated Liste an Gegner, die noch am Leben sind
    enemy_manager.update()
    # Draw Gegner die in der "Noch am Leben" Liste sind
    for enemy in enemy_manager.enemies:
        enemy.draw()
        enemy.check_damage_player(robot, health)

    robot.update_attack(enemy_manager.enemies) # Updated Attacke/Damage von Roboter an Gegner

    robot.update_status_effects()


    # Checke für Kollision von Roboter und Orb
    for orb in orb_list[:]:
        if robot.aabb.check_collision(orb.aabb):
            level.collect_orb()
            orb.randomize_position()

    #Draw-Bereich
    # Zeichne Objekte auf den Screen
    arena.draw(robot)
    robot.draw()
    for orb in orb_list:
        orb.draw()
    for enemy in enemy_manager.enemies:
        enemy.draw()

    health.draw()
    stamina.draw()
    level.draw()


    # Testmodus
    # "visualisiert ausgewählte hintergrundberechnungen und andere testbedingte werte"
    if(TEST_MODE):
        for orb in orb_list:
            orb.draw_aabb() 
        robot.draw_aabb()
        robot.draw_line_to_mouse()
        for enemy in enemy_manager.enemies:
            enemy.draw_aabb()
            enemy.draw_line_enemy(robot)
        arena.draw_aabb()
    pygame.display.flip() #update screen
    clock.tick(60)