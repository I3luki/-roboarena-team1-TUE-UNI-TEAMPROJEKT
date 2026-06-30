import pygame
import os

#fürs öffnen von den txt dateien
#"r" = lesen
#"w" = schreiben/überschreiben
#"a" = anhängen
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATS_FILE = os.path.join(BASE_DIR, "Data", "stats.txt")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "Data", "highscore.txt")
SHOP_POINTS_FILE = os.path.join(BASE_DIR, "Data", "shop_points.txt")
SHOP_UNLOCKS_FILE = os.path.join(BASE_DIR, "Data", "shop_unlocks.txt")
SHOP_UPGRADES_FILE = os.path.join(BASE_DIR, "Data", "shop_upgrades.txt")

class GameManager:
    def __init__(self):
        self.state = "PLAYING"
        self.score = 0
        self.orbs = 0
        self.highscore = self.load_highscore()
        self.shop_points = self.load_shop_points()
        self.unlocked_shop_buffs = self.load_shop_unlocks()
        self.shop_upgrades = self.load_shop_upgrades()
        self.selected_map = None
        self.labyrinth_map_unlocked = False
        self.labyrinth_map_cost = 50
        # Einfach erweiterbar (was wollen wir kills? damage vllt? oder Health lost etc müsste man nur überelgen wie man stats enpfelgt

    def check_game_over(self, health):
        if health.is_dead() and self.state != "GAME_OVER":
            self.save_run()
            self.state = "GAME_OVER"

            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()

    def handle_event(self, event, health, stamina, robot, arena, enemy_manager, orb_list, level, wave_manager):
        if self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset(health, stamina, robot, arena, enemy_manager, orb_list, level, wave_manager)


    def reset(self, health, stamina, robot, arena, enemy_manager, orb_list, level, wave_manager):


        robot.x = arena.player_spawn[0]
        robot.y = arena.player_spawn[1]
        robot.update_aabb()

        self.score = 0
        self.orbs =  0

        # Player reset

        # Player reset
        robot.reset()
        self.apply_permanent_upgrades(robot, health)
        health.current_health = health.max_health
        #kamera reset
        arena.camera.x = robot.x
        arena.camera.y = robot.y
        # Orbs reset
        for orb in orb_list:
            orb.randomize_position()

        # Enemies reset
        wave_manager.reset()

        level.reset()



        self.state = "PLAYING"

    def draw_game_over(self, screen):
        font = pygame.font.Font(None, 80)

        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (300, 300))

        text2 = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(text2, (250, 400))

        score_text = font.render(f"Score: {self.score}",True, (255, 255, 255))
        screen.blit(score_text, (250, 500))

        high_text = font.render(f"Highscore: {self.highscore}",True, (255, 215, 0))
        screen.blit(high_text, (250, 550))

        orbs_text = font.render(f"Orbs gesammelt: {self.orbs}",True, (255, 255, 255))
        screen.blit(orbs_text, (250, 600))

    SHOP_UPGRADES = {
        "max_health": {
            "name": "Mehr Leben",
            "base_cost": 100,
            "cost_increase": 75,
            "amount": 100,
            "max_level": 15
        },
        "speed": {
            "name": "Mehr Speed",
            "base_cost": 120,
            "cost_increase": 80,
            "amount": 0.20,
            "max_level": 15
        },
        "attack_damage": {
            "name": "Mehr Damage",
            "base_cost": 150,
            "cost_increase": 100,
            "amount": 25,
            "max_level": 15
        }
    }



    def load_shop_upgrades(self):
        upgrades = {}

        for upgrade_key in self.SHOP_UPGRADES:
            upgrades[upgrade_key] = 0

        try:
            with open(SHOP_UPGRADES_FILE, "r") as f:
                for line in f:
                    line = line.strip()

                    if ":" in line:
                        key, value = line.split(":")

                        if key in upgrades:
                            upgrades[key] = int(value)

        except (FileNotFoundError, ValueError):
            pass

        return upgrades


    def save_shop_upgrades(self):
        with open(SHOP_UPGRADES_FILE, "w") as f:
            for upgrade_key, level in self.shop_upgrades.items():
                f.write(f"{upgrade_key}:{level}\n")


    def get_upgrade_level(self, upgrade_key):
        return self.shop_upgrades.get(upgrade_key, 0)


    def get_upgrade_cost(self, upgrade_key):
        upgrade = self.SHOP_UPGRADES[upgrade_key]
        level = self.get_upgrade_level(upgrade_key)

        return upgrade["base_cost"] + level * upgrade["cost_increase"]


    def is_upgrade_maxed(self, upgrade_key):
        upgrade = self.SHOP_UPGRADES[upgrade_key]
        level = self.get_upgrade_level(upgrade_key)

        return level >= upgrade["max_level"]


    def buy_shop_upgrade(self, upgrade_key):
        if upgrade_key not in self.SHOP_UPGRADES:
            return

        if self.is_upgrade_maxed(upgrade_key):
            return

        cost = self.get_upgrade_cost(upgrade_key)

        if self.shop_points >= cost:
            self.shop_points -= cost
            self.shop_upgrades[upgrade_key] += 1

            self.save_shop_points()
            self.save_shop_upgrades()


    def apply_permanent_upgrades(self, robot, health):
        health_level = self.get_upgrade_level("max_health")
        speed_level = self.get_upgrade_level("speed")
        damage_level = self.get_upgrade_level("attack_damage")

        health_bonus = health_level * self.SHOP_UPGRADES["max_health"]["amount"]
        speed_bonus = speed_level * self.SHOP_UPGRADES["speed"]["amount"]
        damage_bonus = damage_level * self.SHOP_UPGRADES["attack_damage"]["amount"]

        # Originalwerte einmal merken, damit Upgrades nicht mehrfach gestackt werden
        if not hasattr(health, "shop_base_max_health"):
            health.shop_base_max_health = health.max_health

        if not hasattr(robot, "shop_base_speed_base"):
            robot.shop_base_speed_base = robot.default_speed_base

        if not hasattr(robot, "shop_base_speed_current"):
            robot.shop_base_speed_current = robot.default_speed_current

        if not hasattr(robot, "shop_base_attack_damage"):
            robot.shop_base_attack_damage = robot.default_attack_damage

        # Leben upgraden
        health.max_health = health.shop_base_max_health + health_bonus
        health.current_health = health.max_health

        # Speed upgraden
        robot.default_speed_base = robot.shop_base_speed_base + speed_bonus
        robot.default_speed_current = robot.shop_base_speed_current + speed_bonus
        robot.speed_base = robot.default_speed_base
        robot.speed_current = robot.default_speed_current

        # Damage upgraden
        robot.default_attack_damage = robot.shop_base_attack_damage + damage_bonus
        robot.attack_damage = robot.default_attack_damage

    def load_highscore(self):
        try:
            with open(HIGHSCORE_FILE, "a") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.highscore))

    def load_shop_points(self):
        try:
            with open(SHOP_POINTS_FILE, "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except (FileNotFoundError, ValueError):
            return 0


    def save_shop_points(self):
        with open(SHOP_POINTS_FILE, "w") as f:
            f.write(str(self.shop_points))

    def load_shop_unlocks(self):
        try:
            with open(SHOP_UNLOCKS_FILE, "r") as f:
                return f.read().splitlines()
        except FileNotFoundError:
            return []


    def save_shop_unlocks(self):
        with open(SHOP_UNLOCKS_FILE, "w") as f:
            for buff_key in self.unlocked_shop_buffs:
                f.write(buff_key + "\n")

    #Für Buffs freischalten
    def unlock_shop_buff(self, buff_key):
        if buff_key not in self.unlocked_shop_buffs:
            self.unlocked_shop_buffs.append(buff_key)
            self.save_shop_unlocks()


    def is_shop_buff_unlocked(self, buff_key):
        return buff_key in self.unlocked_shop_buffs

    #Map 2 freischalten mit shop_buff points
    def unlock_map(self, map_key):
        if map_key not in self.unlocked_shop_buffs:
            self.unlocked_shop_buffs.append(map_key)
            self.save_shop_unlocks()


    def is_map_unlocked(self, map_key):
        return map_key in self.unlocked_shop_buffs


   #speichert run in stats.txt
    def save_run(self):
        # a für anhängen
        with open(STATS_FILE, "a") as f:
            f.write(f"{self.score}\n")
        self.shop_points += self.score
        self.save_shop_points()
    #gamestats
    def start_game(self):
        self.state = "PLAYING"

    def pause_game(self):
        self.state = "PAUSE"

    def resume_game(self):
        self.state = "PLAYING"

    def go_to_menu(self):
        self.state = "MENU"