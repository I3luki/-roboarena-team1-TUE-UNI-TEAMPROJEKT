import pygame
from sys import exit
from Arena import Arena
from Roboter import Robot
from Orb import Orb
from HealthSystem_Player import HealthSystem_Player
from StaminaSystem_Player import StaminaSystem_Player
from EnemyManager import EnemyManager
from Level import Level
from GameManager import GameManager
from BuffManager import BuffManager
from WaveManager import WaveManager
from Screens.MainMenu import MainMenu
from Screens.PauseMenu import PauseMenu
from Screens.StatsScreen import StatsScreen
from Textures import Textures


TEST_MODE = True    # TESTMODE: wenn true, dann ist testmodus an

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1200

# Update alles
def update():
    #Input-Bereich
    keys = pygame.key.get_pressed()
    if game.state ==  "GAME_OVER":
        return
    
    # Robo-Updates
    robot.move(keys)
    robot.update_rotation()
    robot.update_attack(enemy_manager.enemies) # Updated Attacke/Damage von Roboter an Gegner
    robot.update_status_effects()

    # Aren-Updates
    arena.update(robot, health)

    # Updated Liste an Gegner (Gegner die am Leben sind, Path von Gegner zu Spieler)
    enemy_manager.update(robot, orb_list, arena)
    wave_manager.update()
    for enemy in enemy_manager.enemies:
        enemy.check_damage_player(robot, health)

    
    # Checke für Kollision von Roboter und Orb
    for orb in orb_list[:]:
        if robot.aabb.check_collision(orb.aabb):
            level.collect_orb(buff_manager, game)
            orb_list.remove(orb)


# Zeichne alles
def draw():
    screen.fill((0, 0, 0))
    arena.draw(robot)
    robot.draw_status_effects()
    robot.relics.draw_icons()
    for orb in orb_list:
        orb.draw()
    enemy_manager.draw()

    health.draw()
    stamina.draw()
    level.draw()

    if game.state == "GAME_OVER":
        game.draw_game_over(screen)

    buff_manager.draw(screen)

# Testmodus
# "visualisiert ausgewählte hintergrundberechnungen und andere testbedingte werte"
def test_mode():
    if(TEST_MODE):
        # Zeichnungen
        for orb in orb_list:
            orb.draw_aabb() 
        robot.draw_aabb()
        robot.draw_line_to_mouse()
        for enemy in enemy_manager.enemies:
            enemy.draw_aabb()
            enemy.draw_line_enemy(robot)
        arena.draw_aabb()

        # Konsolenausgaben
        print(robot.status_effects)




# -------------------------------------------------------------------- INITIATION ------------
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RoboArena")
clock = pygame.time.Clock()

Textures.load_all()

# Lebens-System:
health = HealthSystem_Player(screen, max_health=100, bar_x=10, bar_y=10, bar_width=400, bar_height=25)
# Stamina-System:
stamina = StaminaSystem_Player(screen, max_stamina=100, bar_x=10, bar_y=40, bar_width=400, bar_height=25)
# Level-system
level = Level(screen)
buff_manager = BuffManager()

# Create arena object
arena = Arena(screen, TEST_MODE = TEST_MODE)
robot = Robot(arena, health, stamina, level, arena.WIDTH/2, 1600)   # spawne in der Mitte der Arena
arena.camera.x = robot.x # lässt kamera auf roboter spwanen
arena.camera.y = robot.y # lässt kamera auf roboter spwanen

# Gegner und Orbs
orb_list = [Orb(arena,0,0), Orb(arena,0,0)]
enemy_manager = EnemyManager(arena)
wave_manager = WaveManager(enemy_manager)

# Definiere Event, welches alle x Sekunden Gegner spawnen soll
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 1000)
def spawn_enemy():
    for _ in range(2):
        enemy_manager.add_enemy(0, 0)
        enemy_manager.enemies[-1].randomize_position()

# randomize orb/enemy positions
for orb in orb_list:
    orb.randomize_position()
for enemy in enemy_manager.enemies:
    enemy.randomize_position()


game = GameManager()

#Hauptmeunü
main_menu = MainMenu(screen)

game.state = "MENU"
#Pausemenü
pause_menu = PauseMenu(screen)
#stats
stats_screen = StatsScreen(screen)


# -------------------------------------------------------------------- GAME LOOP ------------
while True:

    # -------------------- EVENTS --------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game.state == "MENU":
            main_menu.handle_event(event, game)

        elif game.state == "STATS":
            stats_screen.handle_event(event, game)

        elif game.state == "PAUSE":
            pause_menu.handle_event(
                event,
                game,
                health,
                stamina,
                robot,
                arena,
                enemy_manager,
                orb_list,
                level,
                wave_manager
            )

        else:
            game.handle_event(
                event,
                health,
                stamina,
                robot,
                arena,
                enemy_manager,
                orb_list,
                level,
                wave_manager
            )

        # Pause
        if game.state == "PLAYING" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.state = "PAUSE"

        # Buff-Auswahl
        if buff_manager.active and event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                buff_manager.apply_buff(0, robot, health)

            elif event.key == pygame.K_2:
                buff_manager.apply_buff(1, robot, health)

            elif event.key == pygame.K_3:
                buff_manager.apply_buff(2, robot, health)

    #draws der Menüs
    if game.state == "MENU":

        main_menu.draw()
    elif game.state == "PLAYING":


        if not buff_manager.active:
            update()

        game.check_game_over(health)
        draw()
    elif game.state == "GAME_OVER":

        draw()

    elif game.state == "PAUSE":
        draw()
        pause_menu.draw()

    elif game.state == "STATS":
        stats_screen.draw()

    pygame.display.flip()
    clock.tick(60)