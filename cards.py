import pygame
from pygame.locals import *
from random import shuffle
from constants import *
from math import ceil, floor

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.uber = False


        # current and goal vars for animation
        self.regular_card_factor = 0.8
        self.is_animating = False
        self.c_pos, g_pos = (0, 0), (0, 0)
        self.c_roto, self.g_roto = 0, 0
        self.c_flip, self.g_flip = 0, 0

        # Image asset
        self.back_image = None
        self.front_image = None
        self.current_image = None

    def flip_card(self):
        self.g_flip = 16 if self.c_flip == 0 else 0
        self.is_animating = True

    def set_new_pos(self, start, end, rotation=0):
        self.c_pos = start
        self.g_pos = end
        self.g_roto = rotation
        self.is_animating = True

    def update_pos(self, animate_const=3):
        """
        Uses c_var and g_var to update rotation, position, and flipping of card object
        :param animate_const: denominator by which easy ease in distance to travel is calculated
        :return: pygame.screen -> updats based on c_rot, r_flip, placed after returned with c_pos
        """
        self.is_animating = self.c_pos != self.g_pos or self.c_roto != self.g_roto or self.c_flip != self.g_flip

        # if no animation is needed, return our image with rotation applied
        if not self.is_animating:
            return pygame.transform.rotate(self.current_image, self.c_roto)

        if self.c_roto != self.g_roto:
            angle_dif = self.g_roto - self.c_roto
            move_angle = ceil(angle_dif / animate_const) if angle_dif > 0 else floor(angle_dif / animate_const)
            self.c_roto += move_angle

        if self.c_pos != self.g_pos:
            x_dif, y_dif = self.g_pos[0] - self.c_pos[0], self.g_pos[1] - self.c_pos[1]
            move_x = ceil(x_dif / animate_const) if x_dif > 0 else floor(x_dif / animate_const)
            move_y = ceil(y_dif / animate_const) if y_dif > 0 else floor(y_dif / animate_const)
            self.c_pos = (self.c_pos[0] + move_x, self.c_pos[1] + move_y)

        if self.c_flip != self.g_flip:
            self.current_image = self.back_image if self.c_flip <= 7 else self.front_image
            lift_const = 1 if self.c_flip == 0 or self.c_flip == 15 else 1.1
            c_width, c_height = self.current_image.get_rect().size
            c_width, c_height = round(c_width * lift_const), round(c_height * lift_const)

            if self.c_flip <= 7:
                c_width = round(c_width * (1 - self.c_flip / 8))
                shift_x = (self.current_image.get_rect().size[0] - c_width) // 2
                self.g_pos = (self.c_pos[0] + shift_x, self.c_pos[1])
            else:
                c_width = round(c_width * (1 - (15 - self.c_flip) / 8))
                shift_x = (self.current_image.get_rect().size[0] - c_width) // 2
                self.g_pos = (self.c_pos[0] - shift_x, self.c_pos[1])

            self.c_flip += 1 if self.c_flip < self.g_flip else -1
            scaled_card_surface = pygame.transform.smoothscale(self.current_image, (c_width, c_height))
            return pygame.transform.rotate(scaled_card_surface, self.c_roto)

        return pygame.transform.rotate(self.current_image, self.c_roto)

    def load_image_assets(self):
        self.back_image = pygame.image.load('Res/Cards/BackCard.png').convert_alpha()
        self.front_image = pygame.image.load("Res/Cards/{}{}.png".format(self.suit, str(self.rank))).convert_alpha()
        new_width = int(self.back_image.get_rect().size[0] * self.regular_card_factor)
        new_height = int(self.back_image.get_rect().size[1] * self.regular_card_factor)
        self.back_image = pygame.transform.smoothscale(self.back_image, (new_width, new_height))
        self.front_image = pygame.transform.smoothscale(self.front_image, (new_width, new_height))
        self.current_image = self.back_image

    def __str__(self):
        if self.suit != self.uber:
            return "{} of {}".format(self.rank, self.suit)
        else:
            return "{} of {}-->".format(self.rank, self.suit)

    def __gt__(self, other):
        # self > other
        # Needs to be tested
        if self.uber and other.uber:
            return self.rank > other.rank
        elif self.uber and not other.uber:
            return True
        elif not self.uber and other.uber:
            return False
        elif self.suit == other.suit:
            return self.rank > other.rank
        else:
            print("Incorrectly comparing two cards")
            return None

class Deck:
    def __init__(self):
        self.suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        self.ranks = list(range(2, 15))
        self.cards_list = []
        self.uber = None
        self.top_card = None
        self.build()

    def build(self):
        for s in self.suits:
            for r in self.ranks:
                self.cards_list.append(Card(r, s))
        self.shuffle()
        self.flip_top_card()

    def flip_top_card(self):
        # To be called at the start of the game, before cards are dealt
        self.top_card = self.pop()
        self.uber = self.top_card.suit
        for c in self.cards_list:
            c.uber = self.uber
        self.cards_list.insert(0, self.top_card)

    def shuffle(self):
        shuffle(self.cards_list)

    def pop(self):
        return self.cards_list.pop()

    def __len__(self):
        return len(self.cards_list)

    def __str__(self):
        return "Deck has {} cards left".format(len(self.cards_list))
