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

        # Berserker Werte
        self.max_health = health
        self.berserker_active = False

        self.normal_damage = self.damage
        self.normal_speed = self.speed_base
        self.normal_radius = self.radius

        self.berserker_damage_multiplier = 1.5
        self.berserker_speed_multiplier = 1.4
        self.berserker_size_multiplier = 3.1

    def activate_berserker_mode(self):
        if self.berserker_active:
            return

        self.berserker_active = True

        # Mehr Schaden
        self.damage = self.normal_damage * self.berserker_damage_multiplier

        # Schneller
        self.speed_base = self.normal_speed * self.berserker_speed_multiplier
        self.speed_current = self.speed_base

        # X * größer
        self.radius = int(self.normal_radius * self.berserker_size_multiplier)
        self.damage_radius =int(self.damage_radius * self.berserker_speed_multiplier)

        # AABB wegen neuer Größe aktualisieren
        self.aabb.x_min = self.x - self.radius
        self.aabb.y_min = self.y - self.radius
        self.aabb.x_max = self.x + self.radius
        self.aabb.y_max = self.y + self.radius

        # Andere Farbe im Berserker-Modus
        self.color = (0, 100, 0)

    def update(self, robot, budget_available):
        current_health = self.health_system.current_health

        if current_health <= self.max_health * 0.3:
            self.activate_berserker_mode()

        return super().update(robot, budget_available)