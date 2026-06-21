import pygame


class ShopScreen:

    def __init__(self, screen):

        self.screen = screen

        self.font_title = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 36)

    def handle_event(self, event, game):

        if event.type == pygame.KEYDOWN:

            # Ice Relic kaufen
            if event.key == pygame.K_1:

                if (
                        game.shop_points >= 20 and
                        not game.is_shop_buff_unlocked("ice_relic")
                ):
                    game.shop_points -= 20
                    game.save_shop_points()
                    game.unlock_shop_buff("ice_relic")

            # Ricochet Relic kaufen
            elif event.key == pygame.K_2:

                if (
                        game.shop_points >= 50 and
                        not game.is_shop_buff_unlocked("ricochet_relic")
                ):
                    game.shop_points -= 50
                    game.save_shop_points()
                    game.unlock_shop_buff("ricochet_relic")

            elif event.key == pygame.K_ESCAPE:
                game.state = "MENU"

    def draw(self, game):

        self.screen.fill((20, 20, 20))

        # Titel
        title = self.font_title.render(
            "SHOP",
            True,
            (255, 255, 255)
        )
        self.screen.blit(title, (380, 80))

        # Coins
        coins_text = self.font.render(
            f"Coins: {game.shop_points}",
            True,
            (255, 215, 0)
        )
        self.screen.blit(coins_text, (100, 180))

        # Ice Relic
        ice_status = (
            "GEKAUFT"
            if game.is_shop_buff_unlocked("ice_relic")
            else "20 Coins"
        )

        ice_text = self.font.render(
            f"1 - Skadi's Blessing ({ice_status})",
            True,
            (255, 255, 255)
        )
        self.screen.blit(ice_text, (100, 260))

        # Ricochet Relic
        ricochet_status = (
            "GEKAUFT"
            if game.is_shop_buff_unlocked("ricochet_relic")
            else "50 Coins"
        )

        ricochet_text = self.font.render(
            f"2 - A Pile of Ricochets ({ricochet_status})",
            True,
            (255, 255, 255)
        )
        self.screen.blit(ricochet_text, (100, 330))

        # Hinweis
        info_text = self.font.render(
            "Freigeschaltete Relics koennen spaeter bei Level-Ups erscheinen.",
            True,
            (180, 180, 180)
        )
        self.screen.blit(info_text, (100, 420))

        # Zurück
        esc_text = self.font.render(
            "ESC - Zurueck",
            True,
            (200, 200, 200)
        )
        self.screen.blit(esc_text, (100, 500))