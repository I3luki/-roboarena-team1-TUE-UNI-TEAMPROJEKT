import pygame
import random


class WaveManager:

    def __init__(self, enemy_manager):
        self.enemy_manager = enemy_manager
        self.current_wave = 1
        self.wave_duration = 60 * 1000
        self.wave_start_time = pygame.time.get_ticks()
        self.wave_running = False

        # Variablen für das zeitversetzte Spawnen (Trickle-Spawn)
        self.enemies_to_spawn = 0
        self.enemies_spawned_this_wave = 0
        self.spawn_cooldown = 1000  # Zeit in ms zwischen den Spawns
        self.last_spawn_time = 0
        self.enemy_weights = {}
        self.font = pygame.font.SysFont(None, 36)

    def start_wave(self):
        self.wave_running = True
        self.wave_start_time = pygame.time.get_ticks()
        self.last_spawn_time = pygame.time.get_ticks()
        self.enemies_spawned_this_wave = 0

        # --- BALANCING: ANZAHL DER GEGNER ---
        # Formel: 6 + (Welle * 3)
        # Welle 1: 9 | Welle 5: 21 | Welle 10: 36 | Welle 20: 66 Gegner.
        self.enemies_to_spawn = 6 + (self.current_wave * 3)

        # Der Spawn-Intervall wird in höheren Wellen schneller
        # Welle 1: Alle 1.5s ein Gegner | Welle 10+: Alle 0.5s ein Gegner
        self.spawn_cooldown = max(500, 1500 - (self.current_wave * 100))

        print(f"--- Welle {self.current_wave} gestartet! ({self.enemies_to_spawn} Gegner) ---")

        # --- BALANCING: GEGNER-MISCHUNG ---
        if self.current_wave == 1:
            self.enemy_weights = {"goblin": 100}
        elif self.current_wave == 2:
            self.enemy_weights = {"goblin": 80, "slime": 20}
        elif self.current_wave < 3:
            self.enemy_weights = {"goblin": 60, "slime": 40}
        elif self.current_wave < 4:
            self.enemy_weights = {"goblin": 40, "slime": 30, "bee": 30}
        else:
            # Late Game: Goblins werden seltener, Wölfe und Bienen dominieren
            self.enemy_weights = {"goblin": 20, "slime": 25, "bee": 30, "wolf": 25}

        # Sofort-Burst zu Beginn: 20% der Welle spawnen direkt, damit sofort Action da ist
        initial_burst = max(2, int(self.enemies_to_spawn * 0.40))
        for _ in range(initial_burst):
            self.spawn_single_enemy()

        # Boss-Spawn alle 5 Wellen (spawnt sofort zusätzlich)
        if self.current_wave % 3 == 0:
            self.spawn_boss()

    def spawn_single_enemy(self):
        """Hilfsmethode, um einen einzelnen regulären Gegner zu spawnen"""
        if self.enemies_spawned_this_wave >= self.enemies_to_spawn:
            return

        x = random.randint(100, 3000)
        y = random.randint(100, 3000)

        enemy_type = random.choices(
            list(self.enemy_weights.keys()),
            weights=list(self.enemy_weights.values()),
            k=1
        )[0]

        self.enemy_manager.add_enemy(enemy_type, x, y, self.current_wave)
        self.enemy_manager.enemies[-1].randomize_position()

        self.enemies_spawned_this_wave += 1

    def update(self):
        if not self.wave_running:
            self.start_wave()
            return

        current_time = pygame.time.get_ticks()

        # --- TRICKLE SPAWN LOGIK ---
        # Wenn noch Gegner in der Warteschlange sind und der Cooldown abgelaufen ist:
        if (self.enemies_spawned_this_wave < self.enemies_to_spawn and
                current_time - self.last_spawn_time >= self.spawn_cooldown):
            self.spawn_single_enemy()
            self.last_spawn_time = current_time

        # WICHTIG fürs Wellenende: Es dürfen keine Gegner mehr auf dem Feld sein
        # UND es dürfen keine Gegner mehr in der Warteschlange stecken.
        all_dead = (len(self.enemy_manager.enemies) == 0 and
                    self.enemies_spawned_this_wave >= self.enemies_to_spawn)

        timer_finished = (current_time - self.wave_start_time >= self.wave_duration)

        if all_dead or timer_finished:
            self.current_wave += 1
            self.start_wave()

    def spawn_boss(self):
        boss_types = ["goblin", "bee", "wolf"]
        boss_type = random.choice(boss_types)

        x = random.randint(100, 3000)
        y = random.randint(100, 3000)

        self.enemy_manager.add_enemy(
            boss_type,
            x,
            y,
            self.current_wave,
            is_boss=True
        )
        self.enemy_manager.enemies[-1].randomize_position()
        print(f"⚠️ BOSS GESPAWNED: {boss_type.upper()} ⚠️")

    def draw_wave_bar(self, screen):
        is_boss_wave = self.current_wave % 5 == 0
        text_color = (220, 40, 40) if is_boss_wave else (255, 255, 255)

        text = f"Boss Wave {self.current_wave}" if is_boss_wave else f"Wave {self.current_wave}"

        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(1000 // 2, 40))

        screen.blit(text_surface, text_rect)

    def reset(self):
        self.current_wave = 1
        self.enemy_manager.enemies.clear()
        self.wave_running = False
        self.enemies_spawned_this_wave = 0
        self.enemies_to_spawn = 0