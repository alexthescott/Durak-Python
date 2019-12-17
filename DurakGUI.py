#!/usr/bin/env python3
""" Inspired in part by https://github.com/k41n/durak-python
Alex Scott
alphaDurak 
Summer 2019
"""
import sys, pygame
import random, math
from DurakController import UI


backCard = pygame.image.load('Cards/BackCard.png')
cardWidth, cardHeight = backCard.get_rect().size
print("cardWidth " + str(cardWidth))
print("cardHeight " + str(cardHeight))
#middleX = (width / 2) - (cardWidth / 2)
#middleY = (height / 2) - (cardHeight / 2)
""" """

class GUI(object):
	def __init__(self, durakGame):
		pygame.init()
		self.Game = durakGame
		self.green = 7, 99, 36
		self.deckImages = {}
		self.suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
		self.ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
		self.size = self.width, self.height = 1200, 750
		self.screen = pygame.display.set_mode(self.size)
		self.loadDeck()

		pygame.display.set_caption("Durak")
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill(self.green)

	def displayWindow(self):
		self.screen.blit(self.background, (0, 0))
		self.displayDeck(self.Game.deck, self.Game.topCard)
		self.displayPlayers(self.Game.players)
		pygame.display.flip()

	def displayDeck(self, deck, topCard):
		backCard = self.deckImages.get("back")
		topCard = self.deckImages.get(topCard.suit + str(topCard.rank))
		deckPrintSize = math.ceil(deck.size() / 4)
		cardWidth, cardHeight = backCard.get_rect().size
		deckX = (self.width / 2)
		deckY = (self.height / 2) - (cardHeight / 2)

		for i in range(int(deckPrintSize)):
			self.screen.blit(backCard, (deckX + i + 5, deckY + i))

		self.screen.blit(topCard, (deckX - cardWidth - 5, deckY))

	def displayTable(self):
		if len(self.Game.tablePlayed) != 0:
			#backCard = self.deckImages.get("back")
			tableString = ""
			for c in self.Game.tablePlayed:
				tableString = tableString + str(c.rank) + c.suit + " "
			print(tableString)



	def displayPlayers(self, players):
		playerCount = len(players)
		tempPlayers = players.copy()
		tempPlayers.sort(key = lambda x: isinstance(x, UI), reverse=True)
		self.displayUser(tempPlayers[0], self.width / 6, self.height - (self.height * .08))
		tempPlayers.pop(0)
		if playerCount == 2:
			self.displayBotHorizontal(players[0], self.width / 6, - (self.height / 5.769), (self.width / 1.5))
		elif playerCount == 3:
			for i, p in enumerate(tempPlayers):
				if i == 0: self.displayBotVertical(p, -self.width * .104, self.height / 6, self.height / 1.5)
				else: self.displayBotVertical(p, self.width * .933, self.height / 6, self.height / 1.5)
		elif playerCount == 4: 
			for i, p in enumerate(tempPlayers):
				if i == 0: self.displayBotHorizontal(p, self.width / 6, - (self.height / 5.769), (self.width / 1.5))
				elif i == 1: self.displayBotVertical(p, -self.width * .104, self.height / 6, self.height / 1.5)
				else: self.displayBotVertical(p, self.width * .933, self.height / 6, self.height / 1.5)
		elif playerCount == 5:
			for i, p in enumerate(tempPlayers):
				if i == 0: self.displayBotHorizontal(p, 60, -70, 220)
				elif i == 1: self.displayBotHorizontal(p, 540, -70, 220)
				elif i == 2: self.displayBotVertical(p, -70, 120, 220)
				else: self.displayBotVertical(p, 840, 120, 220)
		pygame.display.flip()

	def displayBotVertical(self, player, x, y, dist):
		if len(player.hand) <= 6: yDistance = dist / 6
		else: yDistance = dist / len(player.hand)
		for i, c in enumerate(player.hand, 0):
			center = self.deckImages.get("back").get_rect().center
			rotated_card = pygame.transform.rotate(self.deckImages.get("back"), 90)
			self.screen.blit(rotated_card, (x, y + (i * yDistance)))

	def displayBotHorizontal(self, player, x, y, dist):
		if len(player.hand) <= 6: xDistance = dist / 6
		else: xDistance = dist / len(player.hand)
		for i, c in enumerate(player.hand, 0):
			tempCard = self.deckImages.get("back")
			self.screen.blit(tempCard, (x + (i * xDistance), y))

	def displayUser(self, player, x, y):
		if len(player.hand) <= 6: xDistance = (self.width / 1.5) / 6
		else: xDistance = (self.width / 1.5) / len(player.hand)
		for i, c in enumerate(player.hand, 0):
			tempCard = self.deckImages.get(c.suit + str(c.rank))
			self.screen.blit(tempCard, (x + (i * xDistance), y))

	def loadDeck(self):
		self.deckImages.update( {"back" : pygame.image.load('Cards/BackCard.png')})
		for s in self.suits:
			for r in self.ranks:
				cardName = s + str(r)
				cardPath = "Cards/" + cardName + ".png"
				self.deckImages.update( {cardName: pygame.image.load(cardPath)})
