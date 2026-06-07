import time
import math
import random
from Arena_Matrix import Arena_Matrix

class Enemy_Movement:

    CLOSE_DISTANCE = 300
    FAR_DISTANCE = 1200

    MIN_INTERVAL = 0.6
    MAX_INTERVAL = 5

    def __init__(self):
        self.CELL_SIZE = Arena_Matrix.CELL_SIZE
        self.path = []
        # Zufälliger Offset damit nicht alle Gegner gleichzeitig berechnen
        self.last_path_update = time.time() - random.uniform(0, self.MAX_INTERVAL)

    def update(self, enemy, robot, arena):
        now = time.time()

        # Distanz zum Spieler berechnen
        dx = robot.x - enemy.x
        dy = robot.y - enemy.y
        distance = math.hypot(dx, dy)

        # Dynamisches Intervall basierend auf Distanz zum Spieler
        if distance <= self.CLOSE_DISTANCE:
            dynamic_interval = self.MIN_INTERVAL
        elif distance >= self.FAR_DISTANCE:
            dynamic_interval = self.MAX_INTERVAL
        else:
            # Rechnet Wert fließend zwischen MIN_INTERVAL und MAX_INTERVAL um
            ratio = (distance - self.CLOSE_DISTANCE) / (self.FAR_DISTANCE - self.CLOSE_DISTANCE)
            dynamic_interval = self.MIN_INTERVAL + ratio * (self.MAX_INTERVAL - self.MIN_INTERVAL)

        # Pfad alle 0.5s neu berechnen
        if now - self.last_path_update > dynamic_interval:
            self.path = self.find_path(arena.pf_grid, arena.finder, (enemy.x, enemy.y), (robot.x, robot.y))
            self.last_path_update = now

        # Zum nächsten Wegpunkt bewegen und Pfad vorwärtsschreiten
        if len(self.path) > 1:
            next_cell = self.path[1]
            target_x = next_cell[0] * self.CELL_SIZE + self.CELL_SIZE // 2
            target_y = next_cell[1] * self.CELL_SIZE + self.CELL_SIZE // 2

            dx = target_x - enemy.x
            dy = target_y - enemy.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist < self.CELL_SIZE * 0.7:
                # Wegpunkt erreicht: einen Schritt im Pfad vorwärts
                self.path.pop(0)
            else:
                enemy.x += (dx / dist) * enemy.speed
                enemy.y += (dy / dist) * enemy.speed

                enemy.aabb.update(
                    enemy.x - enemy.radius,
                    enemy.y - enemy.radius,
                    enemy.x + enemy.radius,
                    enemy.y + enemy.radius
                )

    def find_path(self, grid, finder, enemy_pos, player_pos):
        grid.cleanup()

        rows = len(grid.nodes)
        cols = len(grid.nodes[0]) if rows else 0

        ex, ey = int(enemy_pos[0] // self.CELL_SIZE), int(enemy_pos[1] // self.CELL_SIZE)
        px, py = int(player_pos[0] // self.CELL_SIZE), int(player_pos[1] // self.CELL_SIZE)

        ex = max(0, min(ex, cols - 1))
        ey = max(0, min(ey, rows - 1))
        px = max(0, min(px, cols - 1))
        py = max(0, min(py, rows - 1))

        # Sicherstellen, dass die Knoten im Grid existieren
        try:
            start = grid.node(ex, ey)
            end = grid.node(px, py)
        except IndexError:
            return self.path  # Falls außerhalb, alten Pfad behalten

        # Prüfen, ob Start oder Ziel überhaupt begehbar sind
        if start is None or end is None:
            return self.path  # Alten Pfad behalten, statt Absturz

        if not start.walkable or not end.walkable:
            # Wenn der Spieler in der Wand steht, gib den aktuellen Pfad zurück.
            # So läuft der Gegner weiter zur letzten bekannten Position des Spielers.
            return self.path

        # Pfadfindung in einem try-except Block absichern
        try:
            path, _ = finder.find_path(start, end, grid)
            return [(node.x, node.y) for node in path]
        except Exception:
            return self.path
