import pygame
import math
from Enemy import Enemy
from Collision import AABB
from Textures import Textures


class Wolf(Enemy):

    def __init__(self, arena, x, y, wave, is_boss=False):
        health = 50 + wave * 15
        damage = 6 + wave * 2
        self.is_boss=is_boss
        if self.is_boss:
            health *= 5
            damage *= 1.5

        super().__init__(arena, x, y, health, damage)

        self.speed = 3.8
        self.damage_radius = 45

        # Walk Animation
        self.walk_frames_original = Textures.WOLF_WALK_ANIMATION[0]
        self.walk_frames_original = [f.convert_alpha() for f in self.walk_frames_original]
        self.walk_frames = [f.copy() for f in self.walk_frames_original]
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.15

        # Death Animation
        self.death_frames_original = Textures.WOLF_DEATH_ANIMATION[0]
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

            self.speed_base *= 0.8
            self.speed_current *= 0.8
            self.damage_radius = int(self.damage_radius * 2)

        # === DASH ALS SPEED-BUFF ===
        self.dash_range = 250
        self.dash_speed_multiplier = 4.0
        self.dash_duration = 0.3
        self.dash_cooldown = 6.0

        self.is_dashing = False
        self.dash_timer = 0.0
        self.dash_cooldown_timer = 0.0
        self.normal_speed = self.speed_base
        self.dash_direction_x = 0.0
        self.dash_direction_y = 0.0

    def _rescale_frames(self, frames_original, scale):
        return [
            pygame.transform.scale(
                frame,
                (int(frame.get_width() * scale), int(frame.get_height() * scale))
            )
            for frame in frames_original
        ]

    def _check_wall_collision(self, new_x, new_y):
        """Prüft, ob die neue Position mit einer Wand kollidiert."""
        temp_aabb = AABB(
            new_x - self.radius,
            new_y - self.radius,
            new_x + self.radius,
            new_y + self.radius
        )
        return any(temp_aabb.check_collision(wall.aabb) for wall in self.arena.walls)

    def _try_move(self, dx, dy):
        """Versucht zu bewegen, stoppt bei Wandkollision."""
        new_x = self.x + dx
        new_y = self.y + dy

        # X-Achse testen
        if not self._check_wall_collision(new_x, self.y):
            self.x = new_x
        # Y-Achse testen
        if not self._check_wall_collision(self.x, new_y):
            self.y = new_y

        # AABB aktualisieren
        self.aabb.x_min = self.x - self.radius
        self.aabb.y_min = self.y - self.radius
        self.aabb.x_max = self.x + self.radius
        self.aabb.y_max = self.y + self.radius

    def start_dash(self, robot):
        """Startet den Dash in Richtung Spieler."""
        if self.is_dashing or self.dash_cooldown_timer > 0:
            return

        dx = robot.x - self.x
        dy = robot.y - self.y
        distance = math.hypot(dx, dy)

        if distance == 0:
            return

        self.dash_direction_x = dx / distance
        self.dash_direction_y = dy / distance

        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cooldown_timer = self.dash_cooldown

        self.speed_base = self.normal_speed * self.dash_speed_multiplier
        self.speed_current = self.speed_base

    def end_dash(self):
        """Beendet den Dash und setzt Speed zurück."""
        self.is_dashing = False
        self.speed_base = self.normal_speed
        self.speed_current = self.normal_speed

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

        # === DASH TIMER UPDATEN ===
        if self.is_dashing:
            self.dash_timer -= 1 / 60
            if self.dash_timer <= 0:
                self.end_dash()

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1 / 60

        # === BEWEGUNG ===
        if self.is_dashing:
            old_x = self.x

            # Bewegung mit Wandkollision
            move_x = self.dash_direction_x * self.speed_current
            move_y = self.dash_direction_y * self.speed_current
            self._try_move(move_x, move_y)

            # Dash früh beenden, wenn an Wand gestoßen (kaum Bewegung)
            actual_move = math.hypot(self.x - old_x, self.y - (old_x + move_y))
            if actual_move < self.speed_current * 0.1:
                self.end_dash()

            did_calculate = False

            # Blickrichtung
            dx = self.x - old_x
            if abs(dx) > 0.01:
                self.facing_right = dx < 0

        else:
            old_x = self.x
            did_calculate = super().update(robot, budget_available)

            dx = self.x - old_x
            if abs(dx) > 0.01:
                self.facing_right = dx < 0

            # Dash prüfen
            distance = math.hypot(robot.x - self.x, robot.y - self.y)
            if distance <= self.dash_range and self.dash_cooldown_timer <= 0:
                self.start_dash(robot)

        # Animation
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

        # NORMAL
        frame = self.walk_frames[self.current_frame]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False).convert_alpha()

        x_screen, y_screen = self.camera.global_to_screen(self)
        draw_x = x_screen - self.frame_width // 2
        draw_y = y_screen - self.frame_height // 2
        self.screen.blit(frame, (draw_x, draw_y))

        self.health_system.draw(self.screen, x_screen, y_screen - self.frame_height // 2 - 10)