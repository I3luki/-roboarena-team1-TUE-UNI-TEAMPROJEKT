import pygame
import random


class WaveManager:

    def __init__(self, enemy_manager):

        self.enemy_manager = enemy_manager

        self.current_wave = 0

        self.wave_duration = 120 * 1000   # 120 Sekunden, gerne in Zukunft langsamer

        self.wave_start_time = pygame.time.get_ticks()

    def start_wave(self):

        enemy_count = 0 + self.current_wave * 1#Anzahl beim start mit jeder wave gibts erstmal einen Mehr war einfacher zum testen

        enemy_health = 10 + self.current_wave * 10#Health wird immer mehr

        enemy_damage = 0.01 + self.current_wave * 0.5#genauso wie der damage

        print(f"Wave {self.current_wave}")

        for i in range(enemy_count):

            x = random.randint(100, 3000)
            y = random.randint(100, 3000)

            self.enemy_manager.add_enemy(
                x,
                y,
                enemy_health,
                enemy_damage
            )
            self.enemy_manager.enemies[-1].randomize_position()

    def update(self):

        current_time = pygame.time.get_ticks()

        all_dead = len(self.enemy_manager.enemies) == 0

        timer_finished = (
                current_time - self.wave_start_time
                >= self.wave_duration
        )
        #Es soll immer eine neue Wave starten wenn alle tot oder zu viel Zeit verstrichen ist.
        if all_dead or timer_finished:

            self.current_wave += 1

            self.wave_start_time = current_time

            self.start_wave()
    def reset(self):

        self.current_wave = 0

        self.wave_start_time = pygame.time.get_ticks()

        self.enemy_manager.enemies.clear()

        self.start_wave()