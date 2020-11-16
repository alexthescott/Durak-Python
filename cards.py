import pygame
from pygame.locals import *
from random import shuffle
from math import ceil, floor

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.uber = False

        # current and goal vars for animation
        self.is_animating = False
        self.c_pos = (0, 0)
        self.g_pos = (0, 0)
        self.c_roto = 0
        self.g_roto = 0
        # flip should take .3 seconds (18 frames @ 60FPS)
        self.c_flip = 0
        self.g_flip = 0

        # Image asset
        self.back_image = None
        self.front_image = None
        self.current_image = None

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

    def flip_card(self):
        # frames to transform
        # flip
        # frames to unflip
        self.c_flip = 16
        self.is_animating = False
        print("Implement flip_card")
        pass

    def animate_card(self, start, end, rotation=0):
        self.c_pos = start
        self.g_pos = end
        self.g_roto = rotation
        self.is_animating = True

    def update_pos(self, animate_const=1):
        if self.c_pos == self.g_pos:
            self.is_animating = False
            return pygame.transform.rotate(self.back_image, self.c_roto)
        x_dif, y_dif = self.g_pos[0] - self.c_pos[0], self.g_pos[1] - self.c_pos[1]
        move_x = ceil(x_dif / animate_const) if x_dif > 0 else floor(x_dif / animate_const)
        move_y = ceil(y_dif / animate_const) if y_dif > 0 else floor(y_dif / animate_const)

        if self.g_roto != self.c_roto:
            angle_dif = self.g_roto - self.c_roto
            move_angle = ceil(angle_dif / animate_const) if angle_dif > 0 else floor(angle_dif / animate_const)
            self.c_roto += move_angle
        temp_screen = pygame.transform.rotate(self.back_image, self.c_roto)

        temp_rect = self.back_image.get_rect()
        self.c_pos = (self.c_pos[0] + move_x, self.c_pos[1] + move_y)
        temp_rect.move_ip(move_x, move_y)
        return temp_screen

    def load_image_assets(self):
        self.back_image = pygame.image.load('Res/Cards/BackCard.png').convert_alpha()
        self.current_image = self.back_image
        card_path = "Res/Cards/{}{}.png".format(self.suit, str(self.rank))
        self.front_image = pygame.image.load(card_path).convert_alpha()


class Deck:
    def __init__(self):
        self.suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        self.ranks = list(range(2, 15))
        self.cards_list = []
        self.uber = None
        self.top_card = None
        self.build()

    def __len__(self):
        return len(self.cards_list)

    def __str__(self):
        return "Deck has {} cards left".format(len(self.cards_list))

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

