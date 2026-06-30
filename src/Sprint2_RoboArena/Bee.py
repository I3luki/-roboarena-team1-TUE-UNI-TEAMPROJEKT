from Enemy import Enemy
import math
from Status_Effects import Poison_Debuff
from Textures import Textures
import pygame


class Bee(Enemy):

    def __init__(self, arena, x, y, wave, is_boss=False):
        health = 20 + wave * 10
        damage = 5 + wave * 3
        self.is_boss =is_boss
        if self.is_boss:
            health *= 5
            damage *= 3

        super().__init__(arena, x, y, health, damage)

        self.speed = 2.5
        self.damage_radius = 30
        self.color = (255, 255, 0)
        self.attack_cooldown_max = 3 * 60
        self.attack_cooldown = 0
        self.poison_duration = 3 * 60
        self.poison_damage = 5
        if self.is_boss:
            self.poison_duration = 15 * 60
            self.poison_damage = 10

        # Walk Animation
        self.walk_frames_original = Textures.BEE_WALK_ANIMATION[0]
        self.walk_frames_original = [f.convert_alpha() for f in self.walk_frames_original]
        self.walk_frames = [f.copy() for f in self.walk_frames_original]
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.15

        # Death Animation
        self.death_frames_original = Textures.BEE_DEATH_ANIMATION[0]
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

            self.speed *= 0.8
            self.damage_radius = int(self.damage_radius * 2)

    def _rescale_frames(self, frames_original, scale):
        return [
            pygame.transform.scale(
                frame,
                (int(frame.get_width() * scale), int(frame.get_height() * scale))
            )
            for frame in frames_original
        ]

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

        # ORIGINALE BEE-LOGIK (unverändert)
        dx = robot.x - self.x
        dy = robot.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

            # Richtung für Animation
            if abs(dx) > 0.01:
                self.facing_right = dx > 0

        self.aabb.update(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )

        # Walk-Animation
        self.animation_timer += 1 / 60
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)

        return False

    def check_damage_player(self, robot, health):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            return

        dx = robot.x - self.x
        dy = robot.y - self.y
        distance = math.hypot(dx, dy)

        if distance < self.damage_radius:
            robot.add_status_effect(
                Poison_Debuff(self.poison_duration, self.poison_damage)
            )
            self.attack_cooldown = self.attack_cooldown_max

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