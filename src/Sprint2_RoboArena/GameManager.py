import pygame


class GameManager:
    def __init__(self):
        self.state = "PLAYING"
        self.score = 0
        self.orbs = 0
        self.highscore = self.load_highscore()
        # Einfach erweiterbar (was wollen wir kills? damage vllt? oder Health lost etc müsste man nur überelgen wie man stats enpfelgt

    def check_game_over(self, health):
        if health.is_dead():
            self.state = "GAME_OVER"

            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()

    def handle_event(self, event, health, stamina, robot, arena, enemy_manager, orb_list, level):
        if self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset(health, stamina, robot, arena, enemy_manager, orb_list, level)


    def reset(self, health, stamina, robot, arena, enemy_manager, orb_list, level):


        robot.x = arena.WIDTH / 2
        robot.y = arena.HEIGHT / 2
        robot.update_aabb()

        self.score = 0
        self.orbs =  0

        # Player reset
        health.current_health = health.max_health
        stamina.current_stamina = stamina.max_stamina


        # Orbs reset
        for orb in orb_list:
            orb.randomize_position()

        # Enemies reset
        enemy_manager.enemies.clear()
        for _ in range(2):
            enemy_manager.add_enemy(0, 0)

        for enemy in enemy_manager.enemies:
            enemy.randomize_position()

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


    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.highscore))