import pygame
from constants import *

from math import log


class Board:
    def __init__(self, pygame_clock, deck):
        # Get clock so we can do dt animation math
        self.pygame_clock = pygame_clock

        # mouse position
        self.mx, self.my = 0, 0
        self.dt = 0
        self.click = False
        self.deck = deck
        self.attack_list = []
        self.defense_list = []
        self.index_list = []

        for i in range(6):
            temp_card = self.deck.pop()
            print(temp_card)
            self.attack_list.append(temp_card)

        self.back_image = self.deck.cards_list[-1].current_image.copy()
        self.deck_x, self.deck_y = (SCREENWIDTH // 2), (SCREENHEIGHT // 2) - (self.back_image.get_rect().size[1] // 2)

    def get_card_indexes(self):
        # If we don't know where to place cards, find it, and store those locations
        pass

    def update(self):
        self.dt = self.pygame_clock.tick(60) / 1000.0
        self.mx, self.my = pygame.mouse.get_pos()

    def render(self, screen):
        # GOAL->Draw for each space for each row given the size
        card_width, card_height = self.back_image.get_rect().size
        card_gap = 110
        bottom_row_y = (SCREENWIDTH - (3 * card_height // 2)) // 2

        # bottom row must be below (self.deck_y + card_height)
        if len(self.attack_list) == 1:
            bottom_row_x = self.deck_x - card_width // 2
            pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect(bottom_row_x, bottom_row_y, card_width, card_height))
        elif len(self.attack_list) % 2 == 0:
            table_width = 2 * card_width + card_gap
            bottom_row_x = self.deck_x - card_width - card_gap // 4
            for i in range(len(self.attack_list)):
                if i == 0:
                    temp_x = bottom_row_x
                elif i % 2 == 0:
                    temp_x = bottom_row_x - ((card_width + card_gap // 2) * (i - i // 2))
                else:
                    temp_x = bottom_row_x + ((card_width + card_gap // 2) * (i - i // 2))
                pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect(temp_x, bottom_row_y, card_width, card_height))
        elif len(self.attack_list) % 2 == 1:
            bottom_row_x = self.deck_x - card_width // 2
            for i in range(len(self.attack_list)):
                if i % 2 == 1:
                    # to the right of our first attack
                    temp_x = bottom_row_x + ((card_width + card_gap // 2) * (i - i // 2))
                else:
                    if i != 0:
                        temp_x = bottom_row_x - ((card_width + card_gap // 2) * (i - i // 2))
                    else:
                        temp_x = bottom_row_x
                pygame.draw.rect(screen, (0, 0, 0), pygame.rect.Rect(temp_x, bottom_row_y, card_width, card_height))

        # draw attacks
        # draw defences
        pass

        # temp_rect = pygame.rect.Rect()
        # draw all played cards in the correct place lol

    def mouse_click(self):
        self.click = True

    def get_menu_click(self):
        # do something like move card if clicked?
        return 0
