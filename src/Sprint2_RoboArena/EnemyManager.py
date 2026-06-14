from Enemy import Enemy
from Orb import Orb


# Updated Liste von Gegnern, die am Leben sind
class EnemyManager:
    def __init__(self, arena):
        self.arena = arena
        self.enemies = []

    # Fügt Gegner zu Gegnerliste hinzu
    def add_enemy(self, x, y, health=100, damage=0.1):
        new_enemy = Enemy(self.arena, x, y, health, damage)
        self.enemies.append(new_enemy)
        print("Gegner gespawned")

    # Updated Liste an lebenden Gegnern
    def update(self, robot, orb_list, arena):
        for enemy in self.enemies[:]:
            enemy.update_status_effects()
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

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()
            
            for effect in enemy.status_effects:
                if hasattr(effect, "draw"):
                    effect.draw()