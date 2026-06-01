import math
class Arena_Matrix:

    CELL_SIZE = 20

    def build_grid(self, arena_width, arena_height, walls):
        cols = arena_width // self.CELL_SIZE
        rows = arena_height // self.CELL_SIZE
        matrix = [[1] * cols for _ in range(rows)]

        for wall in walls:
            # Welche Gitterzellen überlappt diese Wand?
            x1 = wall.aabb.x // self.CELL_SIZE
            y1 = wall.aabb.y // self.CELL_SIZE
            x2 = math.ceil(wall.aabb.x_max / self.CELL_SIZE)
            y2 = math.ceil(wall.aabb.y_max / self.CELL_SIZE)
            for gy in range(y1, min(y2, rows)):
                for gx in range(x1, min(x2, cols)):
                    matrix[gy][gx] = 0  # 0 = blockiert

        return matrix