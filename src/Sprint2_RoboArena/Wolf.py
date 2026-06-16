from Enemy import Enemy

class Wolf(Enemy):

    def __init__(self, arena, x, y, wave):

        health = 200 + wave * 20
        damage = 40 + wave * 3
        super().__init__(
            arena,
            x,
            y,
            health,
            damage
        )

        self.speed = 2.5
        self.color = (120, 120, 120)