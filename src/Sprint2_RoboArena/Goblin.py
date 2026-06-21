import pygame
from Enemy import Enemy
from Textures import Textures


class Goblin(Enemy):

    def __init__(self, arena, x, y, wave):
        health = 100 + wave * 20
        damage = 2 + wave * 2
        super().__init__(arena, x, y, health, damage)

        # Walk Animation
        self.walk_frames = Textures.GOBLIN_WALK_ANIMATION[0]
        self.walk_frames = [f.convert_alpha() for f in self.walk_frames]
        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.15

        # Death Animation
        self.death_frames = Textures.GOBLIN_DEATH_ANIMATION[0]
        self.death_frames = [f.convert_alpha() for f in self.death_frames]
        self.is_dying = False          # True = spielt Death-Animation
        self.death_frame = 0
        self.death_timer = 0.0
        self.death_speed = 0.1
        self.death_finished = False    # True = Animation komplett abgespielt

        self.facing_right = True
        self.frame_width = self.walk_frames[0].get_width()
        self.frame_height = self.walk_frames[0].get_height()

    def update(self, robot, budget_available):
        # STERBE-ZUSTAND: Keine Bewegung, nur Animation abspielen
        if self.is_dying:
            self.death_timer += 1 / 60
            if self.death_timer >= self.death_speed:
                self.death_timer = 0
                self.death_frame += 1
                if self.death_frame >= len(self.death_frames):
                    self.death_frame = len(self.death_frames) - 1
                    self.death_finished = True
            return False  # Keine A*-Berechnung für toten Gegner

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
        # STERBE-ZUSTAND: Death-Animation zeichnen
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