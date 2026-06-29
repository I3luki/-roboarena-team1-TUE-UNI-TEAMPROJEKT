
from Orb import Orb
from Goblin import Goblin
from Slime import Slime
from Bee import Bee
from Wolf import Wolf
from Textures import Textures


# Updated Liste von Gegnern, die am Leben sind
class EnemyManager:
    def __init__(self, arena):
        self.arena = arena
        self.enemies = []

        self.orb_drops = {
            Goblin: Textures.ORB_ICON,
            Slime: Textures.ORB_BLUE,
            Wolf: Textures.ORB_PURPLE,
            Bee: Textures.ORB_YELLOW
        }

    def drop_orbs(self, enemy, orb_list, arena):
        orb_texture = self.orb_drops[type(enemy)]

        orb_count = 1

        if hasattr(enemy, "is_boss") and enemy.is_boss:
            orb_count = 5 #erstmal 5x so viele Orbs gerne auch anpassen

        for i in range(orb_count):
            new_orb = Orb(arena, enemy.x, enemy.y, orb_texture)
            orb_list.append(new_orb)
    # Fügt Gegner zu Gegnerliste hinzu


    def add_enemy(self, enemy_type, x, y, wave, is_boss=False):

        if enemy_type == "goblin":
            enemy = Goblin(self.arena, x, y, wave, is_boss)
            print("Goblin gespawned")
        elif enemy_type == "slime":
            enemy = Slime(self.arena, x, y, wave)
            print("slime gespawned")
        elif enemy_type == "bee":
            enemy = Bee(self.arena, x, y, wave, is_boss)
            print("bee gespawned")
        elif enemy_type == "wolf":
            enemy = Wolf(self.arena, x, y, wave,is_boss)
            print("Wolf gespawned")


        else:
            return

        self.enemies.append(enemy)

    # Updated Liste an lebenden Gegnern
    def update(self, robot, orb_list, arena):
        for enemy in self.enemies[:]:
            enemy.update_status_effects()
            if hasattr(enemy, 'health_system') and enemy.health_system.is_dead(): # Wenn Gegner tot ist
                if hasattr(enemy, 'is_dying'):
                    if not enemy.is_dying:
                        # Starte Death Animation
                        enemy.is_dying = True
                        enemy.death_finished = False
                        enemy.death_frame = 0
                        enemy.death_timer = 0.0
                    elif enemy.death_finished:
                        # Animation fertig -> Orb droppen + entfernen

                        self.drop_orbs(enemy, orb_list, arena)
                        self.enemies.remove(enemy)
                else:
                    # Keine Death Animation -> Sofort entfernen
                    self.drop_orbs(enemy, orb_list, arena) # Erstelle neuen Orb und füge ihn der Liste hinzu
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

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
            
            for effect in enemy.status_effects:
                if hasattr(effect, "draw"):
                    effect.draw()