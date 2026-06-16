import pygame
import random


class WaveManager:

    def __init__(self, enemy_manager):

        self.enemy_manager = enemy_manager

        self.current_wave = 0

        self.wave_duration = 120 * 1000   # 120 Sekunden, gerne in Zukunft langsamer

        self.wave_start_time = pygame.time.get_ticks()

    def start_wave(self):

        enemy_count = 1 + self.current_wave * 1#Anzahl beim start mit jeder wave gibts erstmal einen Mehr war einfacher zum testen

        print(f"Wave {self.current_wave}")

        if self.current_wave < 3:

            enemy_weights = {
                "goblin": 100

            }

        elif self.current_wave < 5:

            enemy_weights = {
            "goblin": 70,
            "slime": 30
        }

        elif self.current_wave < 9:

            enemy_weights = {
            "goblin": 65,
            "slime": 15,
            "bee": 20
        }

        else:

            enemy_weights = {
            "goblin": 50,
            "slime": 15,
            "bee": 15,
            "wolf": 20
        }

        for i in range(enemy_count):

            x = random.randint(100, 3000)
            y = random.randint(100, 3000)

            enemy_type = random.choices(
                list(enemy_weights.keys()),
                weights=list(enemy_weights.values()),
                k=1
            )[0]

            self.enemy_manager.add_enemy(
                enemy_type,
                x,
                y,
                self.current_wave
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