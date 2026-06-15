from Enemy import Enemy

class Goblin(Enemy):

    def __init__(self, arena, x, y, wave):

        health = 100 + wave * 20
        damage = 2 + wave * 2

        super().__init__(
            arena,
            x,
            y,
            health,
            damage
        )

        self.color = (0, 180, 0)