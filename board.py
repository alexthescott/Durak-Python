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
        self.card_pos = {}

        # USED TO DRAW LOCATIONS
        for i in range(6):
            temp_card = self.deck.pop()
            self.attack_list.append(temp_card)
        # USED IF WE DON'T KNOW WHERE TO GO
        self.found_size = False

        self.back_image = self.deck.cards_list[-1].current_image.copy()
        self.deck_x, self.deck_y = (SCREENWIDTH // 2), (SCREENHEIGHT // 2) - (self.back_image.get_rect().size[1] // 2)

    def get_card_indexes(self, card_count):
        card_width, card_height = self.back_image.get_rect().size
        card_gap = 110
        bottom_row_y = (SCREENWIDTH - (3 * card_height // 2)) // 2

        # bottom row must be below (self.deck_y + card_height)
        for c_index in range(1, card_count+1):
            if c_index == 1:
                bottom_row_x = self.deck_x - card_width // 2
                temp_pos = (bottom_row_x, bottom_row_y)
                self.card_pos.update({c_index: [temp_pos]})
            elif c_index % 2 == 0:
                bottom_row_x = self.deck_x - card_width - card_gap // 4
                position_list = []
                for i in range(c_index):
                    if i == 0:
                        temp_x = bottom_row_x
                    elif i % 2 == 0:
                        temp_x = bottom_row_x - ((card_width + card_gap // 2) * (i - i // 2))
                    else:
                        temp_x = bottom_row_x + ((card_width + card_gap // 2) * (i - i // 2))
                    temp_pos = (temp_x, bottom_row_y)
                    position_list.append(temp_pos)
                self.card_pos.update({c_index: position_list})
            elif c_index % 2 == 1:
                bottom_row_x = self.deck_x - card_width // 2
                position_list = []
                for i in range(c_index):
                    if i % 2 == 1:
                        # to the right of our first attack
                        temp_x = bottom_row_x + ((card_width + card_gap // 2) * (i - i // 2))
                    else:
                        if i != 0:
                            temp_x = bottom_row_x - ((card_width + card_gap // 2) * (i - i // 2))
                        else:
                            temp_x = bottom_row_x
                    temp_pos = (temp_x, bottom_row_y)
                    position_list.append(temp_pos)
                self.card_pos.update({c_index: position_list})
        print(self.card_pos)

    def update(self):
        self.dt = self.pygame_clock.tick(60) / 1000.0
        self.mx, self.my = pygame.mouse.get_pos()

    def render(self, screen):
        # GOAL->Draw for each space for each row given the size
        card_width, card_height = self.back_image.get_rect().size
        card_gap = 110
        bottom_row_y = (SCREENWIDTH - (3 * card_height // 2)) // 2

        # bottom row must be below (self.deck_y + card_height)
        build_size_width = card_width
        card_count_x = 1
        while not self.found_size:
            if build_size_width + card_gap + card_width <= SCREENWIDTH - (2 * card_height // 3):
                build_size_width = build_size_width + card_gap // 2 + card_width
                card_count_x += 1
            else:
                self.found_size = True
                print("SCREENWIDTH", SCREENWIDTH - (2 * card_height // 3))
                print("build_size_width", build_size_width)
                print(card_count_x, "cards can be played horizontally")
                print(card_width + card_gap)
                self.get_card_indexes(card_count_x)

        # Draw all cards
        if len(self.card_pos) == 0:
            self.get_card_indexes(card_count_x)
        attack_card_points = self.card_pos[len(self.attack_list)]
        # Positions to draw
        for i, c in enumerate(self.attack_list):
            screen.blit(c.front_image, attack_card_points[i])

        # temp_rect = pygame.rect.Rect()
        # draw all played cards in the correct place lol

    def mouse_click(self):
        self.click = True

    def get_menu_click(self):
        # do something like move card if clicked?
        return 0
