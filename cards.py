import pygame
from pygame.locals import *
from random import shuffle

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.uber = False



        # Image asset
        self.back_card_image = None
        self.card_image = None

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

    def load_image_assets(self):
        self.back_card_image = pygame.image.load('Res/Cards/BackCard.png').convert_alpha()
        card_path = "Res/Cards/{}{}.png".format(self.suit, str(self.rank))
        self.card_image = pygame.image.load(card_path).convert_alpha()



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

