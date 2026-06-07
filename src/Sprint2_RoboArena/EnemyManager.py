from Enemy import Enemy


# Updated Liste von Gegnern, die am Leben sind
class EnemyManager:
    def __init__(self, arena):
        self.arena = arena
        self.enemies = []

    # Fügt Gegner zu Gegnerliste hinzu
    def add_enemy(self, x, y):
        new_enemy = Enemy(self.arena, x, y)
        self.enemies.append(new_enemy)

    # Updated Liste an lebenden Gegnern
    # Sobald ein Gegner hinzugefügt/entfernt wird, wird eine neue Liste mit/ohne den Gegner erstellt
    def update(self, robot):
        self.enemies = [
            e for e in self.enemies
            if not (hasattr(e, 'health_system') and e.health_system.is_dead())
        ]

        MAX_CALCS_PER_FRAME =  2 # Maximale Anzahl an A* Berechnungen pro Frame
        calcs_done_this_frame = 0

        for enemy in self.enemies:
            # Prüfen ob für diesen Frame noch Budget frei ist
            budget_available = MAX_CALCS_PER_FRAME > calcs_done_this_frame

            # Ergebnis abrufen: Hat Gegner wirklich gerechnet?
            did_calculate = enemy.update(robot, budget_available)

            if did_calculate:
                calcs_done_this_frame += 1

    def get_dead_positions(self):
        dead_positions = [
            (e.x, e.y) for e in self.enemies
            if hasattr(e, 'health_system') and e.health_system.is_dead()
        ]
        return dead_positions