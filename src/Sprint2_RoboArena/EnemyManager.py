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
        for enemy in self.enemies:
            enemy.update(robot)

    def get_dead_positions(self):
        dead_positions = [
            (e.x, e.y) for e in self.enemies
            if hasattr(e, 'health_system') and e.health_system.is_dead()
        ]
        return dead_positions