import time
import math
from Arena_Matrix import Arena_Matrix
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.finder.a_star import AStarFinder

class Enemy_Movement:

    def __init__(self):
        self.CELL_SIZE = Arena_Matrix.CELL_SIZE
        self.path = []
        self.last_path_update = 0

    def update(self, enemy, robot, matrix):
        now = time.time()

        # Pfad alle 0.5s neu berechnen
        if now - self.last_path_update > 0.5 or not self.path:
            self.path = self.find_path(matrix, (enemy.x, enemy.y), (robot.x, robot.y))
            self.last_path_update = now

        # Zum nächsten Wegpunkt bewegen
        if len(self.path) > 1:
            next_cell = self.path[1]
            target_x = next_cell[0] * self.CELL_SIZE + self.CELL_SIZE // 2
            target_y = next_cell[1] * self.CELL_SIZE + self.CELL_SIZE // 2

            dx = target_x - enemy.x
            dy = target_y - enemy.y
            dist = math.sqrt(dx**2 + dy**2)

            if dist > 2:
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
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

        ex, ey = int(enemy_pos[0] // self.CELL_SIZE), int(enemy_pos[1] // self.CELL_SIZE)
        px, py = int(player_pos[0] // self.CELL_SIZE), int(player_pos[1] // self.CELL_SIZE)

        start = grid.node(ex, ey)
        end = grid.node(px, py)

        path, _ = finder.find_path(start, end, grid)
        return [(node.x, node.y) for node in path]