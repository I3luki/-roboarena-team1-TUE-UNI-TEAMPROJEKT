import pygame
from Level_Buffs import LevelBuffs, LevelHermesShoe

class ShopScreen:

    def __init__(self, screen):

        self.screen = screen
        self.level_relics = LevelBuffs()

        self.font_title = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 36)



    def handle_event_buy(self, game, relic):
        if (
            game.shop_points >= relic.cost and
            not game.is_shop_buff_unlocked(relic.key)
        ):
            game.shop_points -= relic.cost
            game.save_shop_points()
            game.unlock_shop_buff(relic.key)

    def draw_relic_choice(self, game, choice_start, index, space, levelbuff_relic):
        # Get Status
        status = (
            "GEKAUFT"
            if game.is_shop_buff_unlocked(levelbuff_relic.key)
            else str(levelbuff_relic.cost) +" Coins"
        )
        # Draw Text
        text = self.font.render(
            f"{index} - {levelbuff_relic.name} ({status})",
            True,
            (255, 255, 255)
        )
        self.screen.blit(text, (100, choice_start + index*space))



    def handle_event(self, event, game):

        if event.type == pygame.KEYDOWN:

            # check if player tries to buy smth, then try to buy
            index = 0
            for shop_buff in LevelBuffs.all_shop:           # iterate over all buyable levelbuffs, 
                keypress = getattr(pygame, f"K_{index}")    # with index as corresponding keypress
                
                if event.key == keypress:
                    self.handle_event_buy(game,shop_buff)

                index+=1
            
            # check for escape to menu
            if event.key == pygame.K_ESCAPE:
                game.state = "MENU"


    def draw(self, game):

        SPACE = 70              # height between choices
        CHOICE_START = 260      # starting height of choices

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

        # draw choices
        index = 0
        for level_relic in LevelBuffs.all_shop:
            self.draw_relic_choice(game, CHOICE_START, index, SPACE, level_relic)
            index += 1


        # Hinweis
        hinweis_offset = 20    # vergrößert den space um sich von choices abzuheben
        info_text = self.font.render(
            "Freigeschaltete Relics koennen spaeter bei Level-Ups erscheinen.",
            True,
            (180, 180, 180)
        )
        self.screen.blit(info_text, (100, CHOICE_START + index*SPACE + hinweis_offset))
    

        # Zurück
        index += 1
        choice_offset = 70  # vergrößert den space um sich von choices abzuheben
        esc_text = self.font.render(
            "ESC - Zurueck",
            True,
            (200, 200, 200)
        )
        self.screen.blit(esc_text, (100, CHOICE_START + (index*SPACE + choice_offset)))