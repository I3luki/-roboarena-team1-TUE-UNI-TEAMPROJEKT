
from Orb import Orb
from Goblin import Goblin
from Slime import Slime
from Bee import Bee
from Wolf import Wolf


# Updated Liste von Gegnern, die am Leben sind
class EnemyManager:
    def __init__(self, arena):
        self.arena = arena
        self.enemies = []

    # Fügt Gegner zu Gegnerliste hinzu


    def add_enemy(self, enemy_type, x, y, wave):

        if enemy_type == "goblin":
            enemy = Goblin(self.arena, x, y, wave)
            print("Goblin gespawned")
        elif enemy_type == "slime":
            enemy = Slime(self.arena, x, y, wave)
            print("slime gespawned")
        elif enemy_type == "bee":
            enemy = Bee(self.arena, x, y, wave)
            print("bee gespawned")
        elif enemy_type == "wolf":
            enemy = Wolf(self.arena, x, y, wave)
            print("Wolf gespawned")


        else:
            return

        self.enemies.append(enemy)

    # Updated Liste an lebenden Gegnern
    def update(self, robot, orb_list, arena):
        for enemy in self.enemies[:]:
            if hasattr(enemy, 'health_system') and enemy.health_system.is_dead(): # Wenn Gegner tot ist
                new_orb = Orb(arena, enemy.x, enemy.y)
                orb_list.append(new_orb) # Erstelle neuen Orb und füge ihn der Liste hinzu
                self.enemies.remove(enemy) # Entferne Gegner aus der Liste

        MAX_CALCS_PER_FRAME =  2 # Maximale Anzahl an A* Berechnungen pro Frame
        calcs_done_this_frame = 0

        for enemy in self.enemies:
            # Prüfen ob für diesen Frame noch Budget frei ist
            budget_available = MAX_CALCS_PER_FRAME > calcs_done_this_frame

            # Ergebnis abrufen: Hat Gegner wirklich gerechnet?
            did_calculate = enemy.update(robot, budget_available)

            if did_calculate:
                calcs_done_this_frame += 1