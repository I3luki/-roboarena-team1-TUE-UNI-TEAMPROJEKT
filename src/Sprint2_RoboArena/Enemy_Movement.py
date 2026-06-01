import time
import math
import random
from Arena_Matrix import Arena_Matrix
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder

PATH_INTERVAL = 0.5  # Sekunden zwischen Pfad-Neuberechnungen

class Enemy_Movement:

    def __init__(self):
        self.CELL_SIZE = Arena_Matrix.CELL_SIZE
        self.path = []
        # Zufälliger Offset damit nicht alle Gegner gleichzeitig berechnen
        self.last_path_update = time.time() - random.uniform(0, PATH_INTERVAL)

    def update(self, enemy, robot, matrix):
        now = time.time()

        # Pfad alle 0.5s neu berechnen
        if now - self.last_path_update > PATH_INTERVAL or not self.path:
            self.path = self.find_path(matrix, (enemy.x, enemy.y), (robot.x, robot.y))
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

    def find_path(self, matrix, enemy_pos, player_pos):
        grid = Grid(matrix=matrix)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0

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