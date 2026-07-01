import pygame
from Level_Buffs import LevelBuffs


class ShopScreen:

    NUMBER_KEYS = [
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6,
        pygame.K_7,
        pygame.K_8,
        pygame.K_9
    ]

    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(
            "Sprites/Shopmenu_Background.png"
            ).convert()

        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )
        self.level_relics = LevelBuffs()

        self.font_title = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 36)

        self.active_tab = "RELICS"


    def handle_event_buy_relic(self, game, relic):
        if (
                game.shop_points >= relic.cost and
                not game.is_shop_buff_unlocked(relic.key)
        ):
            game.shop_points -= relic.cost
            game.save_shop_points()
            game.unlock_shop_buff(relic.key)


    def handle_event_buy_map(self, game):
        if (
                game.shop_points >= 100 and
                not game.is_map_unlocked("labyrinth_map")
        ):
            game.shop_points -= 100
            game.save_shop_points()
            game.unlock_map("labyrinth_map")


    def handle_event_buy_upgrade(self, game, upgrade_key):
        game.buy_shop_upgrade(upgrade_key)


    def handle_event(self, event, game):

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            game.state = "MENU"
            return

        if event.key == pygame.K_r:
            self.active_tab = "RELICS"
            return

        if event.key == pygame.K_u:
            self.active_tab = "UPGRADES"
            return

        if self.active_tab == "RELICS":
            self.handle_relic_tab_event(event, game)

        elif self.active_tab == "UPGRADES":
            self.handle_upgrade_tab_event(event, game)


    def handle_relic_tab_event(self, event, game):

        relics = list(LevelBuffs.all_shop)

        for i, relic in enumerate(relics):
            if i >= len(self.NUMBER_KEYS):
                break

            if event.key == self.NUMBER_KEYS[i]:
                self.handle_event_buy_relic(game, relic)
                return

        map_index = len(relics)

        if map_index < len(self.NUMBER_KEYS):
            if event.key == self.NUMBER_KEYS[map_index]:
                self.handle_event_buy_map(game)


    def handle_upgrade_tab_event(self, event, game):

        upgrade_keys = list(game.SHOP_UPGRADES.keys())

        for i, upgrade_key in enumerate(upgrade_keys):
            if i >= len(self.NUMBER_KEYS):
                break

            if event.key == self.NUMBER_KEYS[i]:
                self.handle_event_buy_upgrade(game, upgrade_key)
                return


    def draw_tabs(self):
        relic_color = (255, 255, 255) if self.active_tab == "RELICS" else (120, 120, 120)
        upgrade_color = (255, 255, 255) if self.active_tab == "UPGRADES" else (120, 120, 120)

        relic_text = self.font.render("R - Relics", True, relic_color)
        upgrade_text = self.font.render("U - Upgrades", True, upgrade_color)

        self.screen.blit(relic_text, (100, 220))
        self.screen.blit(upgrade_text, (300, 220))


    def draw_relic_choice(self, game, y, index, levelbuff_relic):

        status = (
            "GEKAUFT"
            if game.is_shop_buff_unlocked(levelbuff_relic.key)
            else str(levelbuff_relic.cost) + " Coins"
        )

        text = self.font.render(
            f"{index} - {levelbuff_relic.name} ({status})",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (100, y))


    def draw_upgrade_choice(self, game, y, index, upgrade_key):

        upgrade = game.SHOP_UPGRADES[upgrade_key]
        level = game.get_upgrade_level(upgrade_key)

        if game.is_upgrade_maxed(upgrade_key):
            status = f"Level {level}/{upgrade['max_level']} - MAX"
        else:
            cost = game.get_upgrade_cost(upgrade_key)
            status = f"Level {level}/{upgrade['max_level']} - {cost} Coins"

        text = self.font.render(
            f"{index} - {upgrade['name']} (+{upgrade['amount']} pro Level) ({status})",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (100, y))


    def draw(self, game):

        SPACE = 70
        CHOICE_START = 300

        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface((420, 420), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))   # Schwarz mit Transparenz
        self.screen.blit(overlay, (300, 120))

        title = self.font_title.render(
            "SHOP",
            True,
            (255, 255, 255)
        )
        self.screen.blit(title, (380, 80))

        coins_text = self.font.render(
            f"Coins: {game.shop_points}",
            True,
            (255, 215, 0)
        )
        self.screen.blit(coins_text, (100, 180))

        self.draw_tabs()

        if self.active_tab == "RELICS":
            self.draw_relic_tab(game, CHOICE_START, SPACE)

        elif self.active_tab == "UPGRADES":
            self.draw_upgrade_tab(game, CHOICE_START, SPACE)

        esc_text = self.font.render(
            "ESC - Zurueck",
            True,
            (200, 200, 200)
        )
        self.screen.blit(esc_text, (100, 900))


    def draw_relic_tab(self, game, choice_start, space):

        relics = list(LevelBuffs.all_shop)

        for i, level_relic in enumerate(relics):
            if i >= len(self.NUMBER_KEYS):
                break

            index = i + 1
            y = choice_start + i * space

            self.draw_relic_choice(game, y, index, level_relic)

        map_index = len(relics)

        if map_index < len(self.NUMBER_KEYS):
            number = map_index + 1
            y = choice_start + map_index * space

            map_status = (
                "GEKAUFT"
                if game.is_map_unlocked("labyrinth_map")
                else "100 Coins"
            )

            map_text = self.font.render(
                f"{number} - Labyrinth Map ({map_status})",
                True,
                (255, 255, 255)
            )

            self.screen.blit(map_text, (100, y))

        info_text = self.font.render(
            "Freigeschaltete Relics koennen spaeter bei Level-Ups erscheinen.",
            True,
            (180, 180, 180)
        )
        self.screen.blit(info_text, (100, 820))


    def draw_upgrade_tab(self, game, choice_start, space):

        upgrade_keys = list(game.SHOP_UPGRADES.keys())

        for i, upgrade_key in enumerate(upgrade_keys):
            if i >= len(self.NUMBER_KEYS):
                break

            index = i + 1
            y = choice_start + i * space

            self.draw_upgrade_choice(game, y, index, upgrade_key)

        info_text = self.font.render(
            "Upgrades sind permanent und gelten fuer neue Runs.",
            True,
            (180, 180, 180)
        )
        self.screen.blit(info_text, (100, 820))