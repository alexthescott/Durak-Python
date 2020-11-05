import pygame
from math import ceil

# local imports
from cards import Deck, Card
from constants import *

# 


class Durak:
    def __init__(self):
        self.gameDeck = Deck()
        self.deckImages = {}
        self.load_image_assets()
        self.debugPrint = True

        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def load_image_assets(self):
        self.deckImages.update({"back": pygame.image.load('Res/Cards/BackCard.png').convert()})
        for s in self.gameDeck.suits:
            for r in self.gameDeck.ranks:
                card_name = s + str(r)
                card_path = "Res/Cards/" + card_name + ".png"
                self.deckImages.update({card_name: pygame.image.load(card_path).convert()})

    def draw_deck(self, screen):
        back_card = self.deckImages.get("back")
        # topCard = self.deckImages.get(topCard.suit + str(topCard.rank))
        deck_print_size = round(len(self.gameDeck)//1.5)
        cardWidth, cardHeight = back_card.get_rect().size
        deckX = (SCREENWIDTH // 2)
        deckY = (SCREENHEIGHT // 2) - (cardHeight // 2)

        for i in range(ceil(deck_print_size / 3)):
            screen.blit(back_card, (deckX + 5 + i * 2, deckY + i * 2))

        # self.screen.blit(topCard, (deckX - cardWidth - 5, deckY))

    def render(self, screen):
        self.draw_deck(screen)