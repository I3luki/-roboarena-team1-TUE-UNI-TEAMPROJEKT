import pygame
from Enemy import Enemy
from Textures import Textures


class Goblin(Enemy):

    def __init__(self, arena, x, y, wave, is_boss):
        health = 100 + wave * 20
        damage = 2 + wave * 2
        self.is_boss = is_boss
        if self.is_boss:
            health *=5
            damage *=2
        super().__init__(arena, x, y, health, damage)

        # Walk Animation (Original-Frames für Neuskalierung speichern)
        self.walk_frames_original = Textures.GOBLIN_WALK_ANIMATION[0]
        self.walk_frames_original = [f.convert_alpha() for f in self.walk_frames_original]
        self.walk_frames = [f.copy() for f in self.walk_frames_original]
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.15

        # Death Animation (ebenfalls Original speichern)
        self.death_frames_original = Textures.GOBLIN_DEATH_ANIMATION[0]
        self.death_frames_original = [f.convert_alpha() for f in self.death_frames_original]
        self.death_frames = [f.copy() for f in self.death_frames_original]
        self.is_dying = False
        self.death_frame = 0
        self.death_timer = 0.0
        self.death_speed = 0.1
        self.death_finished = False

        self.facing_right = True
        self.frame_width = self.walk_frames[0].get_width()
        self.frame_height = self.walk_frames[0].get_height()
        self.height = self.frame_height
        if self.is_boss:
            boss_size_multiplier = 2

            self.walk_frames = self._rescale_frames(
                self.walk_frames_original,
                boss_size_multiplier
            )

            self.death_frames = self._rescale_frames(
                self.death_frames_original,
                boss_size_multiplier
            )

            self.frame_width = self.walk_frames[0].get_width()
            self.frame_height = self.walk_frames[0].get_height()
            self.height = self.frame_height

        self.damage_radius = 45
        if self.is_boss:
            self.speed_base *= 0.5
            self.speed_current *= 0.5
            self.damage_radius = int(self.damage_radius * 2)

        # Berserker Werte
        self.max_health = health
        self.berserker_active = False

        self.normal_damage = self.damage
        self.normal_speed_base = self.speed_base
        self.normal_speed_current = self.speed_current
        self.normal_damage_radius = self.damage_radius

        self.berserker_damage_multiplier = 1.5
        self.berserker_speed_multiplier = 2
        self.berserker_size_multiplier = 2

    def _rescale_frames(self, frames_original, scale):
        """Skaliert Frames mit dem gleichen Prinzip wie animation_scaling."""
        return [
            pygame.transform.scale(
                frame,
                (int(frame.get_width() * scale), int(frame.get_height() * scale))
            )
            for frame in frames_original
        ]

    def activate_berserker_mode(self):
        if self.berserker_active:
            return

        self.berserker_active = True

        # Mehr Schaden
        self.damage = self.normal_damage * self.berserker_damage_multiplier

        # Schneller
        self.speed_base = self.normal_speed_base * self.berserker_speed_multiplier
        self.speed_current = self.normal_speed_current * self.berserker_speed_multiplier

        # Größer (Kollisionsradius)
        self.damage_radius = int(self.normal_damage_radius * self.berserker_size_multiplier)

        # === ANIMATION GRÖßER MACHEN ===
        self.walk_frames = self._rescale_frames(
            self.walk_frames_original, self.berserker_size_multiplier
        )
        self.death_frames = self._rescale_frames(
            self.death_frames_original, self.berserker_size_multiplier
        )
        # Frame-Größe aktualisieren
        self.frame_width = self.walk_frames[0].get_width()
        self.frame_height = self.walk_frames[0].get_height()

        # AABB wegen neuer Größe aktualisieren
        self.aabb.x_min = self.x - self.radius
        self.aabb.y_min = self.y - self.radius
        self.aabb.x_max = self.x + self.radius
        self.aabb.y_max = self.y + self.radius

        # Andere Farbe im Berserker-Modus
        self.color = (0, 100, 0)

    def update(self, robot, budget_available):
        # STERBE-ZUSTAND
        if self.is_dying:
            self.death_timer += 1 / 60
            if self.death_timer >= self.death_speed:
                self.death_timer = 0
                self.death_frame += 1
                if self.death_frame >= len(self.death_frames):
                    self.death_frame = len(self.death_frames) - 1
                    self.death_finished = True
            return False

        # Berserker-Modus prüfen
        current_health = self.health_system.current_health
        if current_health <= self.max_health * 0.3:
            self.activate_berserker_mode()

        # NORMAL: Bewegung + Walk-Animation
        old_x = self.x
        did_calculate = super().update(robot, budget_available)

        dx = self.x - old_x
        if abs(dx) > 0.01:
            self.facing_right = dx > 0

        self.animation_timer += 1 / 60
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)

        return did_calculate

    def draw(self):
        # STERBE-ZUSTAND
        if self.is_dying:
            frame = self.death_frames[self.death_frame]
            x_screen, y_screen = self.camera.global_to_screen(self)
            draw_x = x_screen - frame.get_width() // 2
            draw_y = y_screen - frame.get_height() // 2
            self.screen.blit(frame, (draw_x, draw_y))
            return

        # NORMAL: Walk-Animation zeichnen
        frame = self.walk_frames[self.current_frame]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False).convert_alpha()

        x_screen, y_screen = self.camera.global_to_screen(self)
        draw_x = x_screen - self.frame_width // 2
        draw_y = y_screen - self.frame_height // 2
        self.screen.blit(frame, (draw_x, draw_y))

        self.health_system.draw(self.screen, x_screen, y_screen - self.frame_height // 2 - 10)