import random
import pygame
from Level_Buffs import (
    LevelSpeedBuff,
    LevelDamageBuff,
    LevelAttackSpeedBuff,
    LevelAttackRangeBuff,
    LevelHealthBuff,
    LevelIceRelic,
    LevelRicochetRelic,
    LevelJinguBangRelic,
    LevelSwordmasterManualRelic,
    LevelHermesShoe,
    LevelDevilContractI,
    LevelDevilContractII,
    COMMON, RARE, EPIC       # probability of corresponding rarity
)

COLOR_COMMON = (128, 128, 128)
COLOR_RARE = (173, 216, 230)
COLOR_EPIC = (200, 180, 255)

class BuffManager:

    def __init__(self):

        self.font = pygame.font.SysFont(None, 36)
        self.font_name = pygame.font.SysFont(None, 36, bold=True)
        self.font_description = pygame.font.SysFont(None, 27)
        self.font_flavor = pygame.font.SysFont(None, 18, italic=True)
        self.font_rarity = pygame.font.SysFont("Papyrus", 34)
        self.big_font = pygame.font.SysFont(None, 60)

        self.available_buffs = [
            LevelHealthBuff(),
            LevelSpeedBuff(),
            LevelDamageBuff(),
            LevelAttackSpeedBuff(),
            LevelAttackRangeBuff(),
            LevelIceRelic(),
            LevelRicochetRelic(),
            LevelJinguBangRelic(),
            LevelSwordmasterManualRelic(),
            LevelHermesShoe(),
            LevelDevilContractI(),
            LevelDevilContractII()
        ]

        self.common_buffs = [buff for buff in self.available_buffs if buff.rarity == COMMON]
        self.rare_buffs = [buff for buff in self.available_buffs if buff.rarity == RARE]
        self.epic_buffs = [buff for buff in self.available_buffs if buff.rarity == EPIC]

        self.buff_lists = [self.common_buffs, self.rare_buffs, self.epic_buffs]
        self.weights = [COMMON, RARE, EPIC]  

        self.choices_amount = 3
        self.current_choices = []
        self.active = False
        

    def get_available_buffs(self, game):
        available_buffs = []

        for buff in self.available_buffs:
            if hasattr(buff, "shop_locked"):
                if game.is_shop_buff_unlocked(buff.key):
                    available_buffs.append(buff)
            else:
                available_buffs.append(buff)

        return available_buffs


    def get_buffs_by_rarity(self, buffs):
        common = [b for b in buffs if b.rarity == COMMON]
        rare = [b for b in buffs if b.rarity == RARE]
        epic = [b for b in buffs if b.rarity == EPIC]

        return [
            (common, COMMON),
            (rare, RARE),
            (epic, EPIC)
        ]


    def roll_buff_choices(self, rarity_groups):
        choices = []

        possible_groups = [
            (buff_list, weight)
            for buff_list, weight in rarity_groups
            if len(buff_list) > 0
        ]

        buff_lists = [group[0] for group in possible_groups]
        weights = [group[1] for group in possible_groups]

        for _ in range(self.choices_amount):
            chosen_list = random.choices(
                buff_lists,
                weights=weights,
                k=1
            )[0]

            chosen_buff = random.choice(chosen_list)
            choices.append(chosen_buff)

        return choices


    def generate_choices(self, game):
        available_buffs = self.get_available_buffs(game)
        rarity_groups = self.get_buffs_by_rarity(available_buffs)

        self.current_choices = self.roll_buff_choices(rarity_groups)
        self.active = True

    def apply_buff(self, index, robot, health):

        selected_buff = self.current_choices[index]
        selected_buff.apply_to(robot, health)

        self.active = False
        self.current_choices = []


    def draw(self, screen):

        if not self.active:
            return

        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = self.big_font.render(
            "LEVEL UP!",
            True,
            (255, 255, 255)
        )


        texts_names = []
        texts_descriptions = []
        texts_flavors = []
        texts_rarity = []
        colors_rarity = []
        
        # Generate rendered texts
        index = 1
        for choice in self.current_choices:
            # Generate name
            text = self.font_name.render(f"{index} - {choice.name}",
                                    True,
                                    (255, 255, 255))
            texts_names.append(text)

            # Generate Description
            text = self.font_description.render(f"{choice.description}",
                                    True,
                                    (255, 255, 255))
            texts_descriptions.append(text)

            # Generate Flavor texts
            text = self.font_flavor.render(f"{choice.flavor_text}",
                                    True,
                                    (255, 255, 255))
            texts_flavors.append(text)

            # Generate Rarity Texts
            text_rarity = ""
            if choice.rarity == COMMON:
                text_rarity = "Common"
                color_rarity = COLOR_COMMON
            elif choice.rarity == RARE:
                text_rarity = "Rare"
                color_rarity = COLOR_RARE
            elif choice.rarity == EPIC:
                text_rarity = "Epic"
                color_rarity = COLOR_EPIC
            text = self.font_rarity.render(f"{text_rarity}",
                                    True,
                                    (255, 255, 255))
            texts_rarity.append(text)
            colors_rarity.append(color_rarity)

            #update index
            index += 1


        # Generate Choice cards
        screen_width, screen_height = screen.get_size()
        CARD_WIDTH  = (screen_width / 4) * 3
        CARD_HEIGHT = (screen_height / 6)

        cards = []
        pos_name = (CARD_WIDTH/3, CARD_HEIGHT/7)
        pos_description = (CARD_WIDTH/3, CARD_HEIGHT/3)
        pos_flavor = (CARD_WIDTH/3, 2*(CARD_HEIGHT/3))
        pos_rarity = (CARD_WIDTH/8, CARD_HEIGHT/6)

            # blit everything on the card
        for i in range(self.choices_amount):
            surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
            color = colors_rarity[i] + (128,)    # add transparency value
            surf.fill(color)  

            surf.blit(texts_names[i], pos_name)
            surf.blit(texts_descriptions[i], pos_description)
            surf.blit(texts_flavors[i], pos_flavor)
            surf.blit(texts_rarity[i], pos_rarity)

            cards.append(surf)
        


        # Zeichne auf den screen
        space_top = CARD_HEIGHT*1.5
        space_left = 100
        space_between = CARD_HEIGHT / 3 

        screen.blit(title, (screen_width/3, CARD_HEIGHT/2)) #"LEVEL-UP" text

        for i in range(self.choices_amount):
            screen.blit(cards[i], (space_left, 
                                   space_top  + (i*(CARD_HEIGHT + space_between))))



