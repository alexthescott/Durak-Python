#!/usr/bin/env python3
""" Inspired in part by https://github.com/k41n/durak-python
Alex Scott
alphaDurak 
Summer 2019
"""
import sys, pygame
import random
from card import Card
from player import Player
from deck import Deck

class UI(Player):
	def __init__(self, name):
		Player.__init__(self, name)
		self.input = False
		self.cardIndex = -1
		self.lastInput = None

	def getInput(self, key):
		self.lastInput = key
		print(key)

	def startAttack(self, tablePlayed, defencePlayed):
		self.input = True
		attack = None
		if(len(defencePlayed) == 0):
			index = -1
			while index <= self.size():
				index = self.getIndex()
			"""

			attack = self.hand.pop(index - 1)

			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key.name().isdigit() and event.key.name() <= self.size():
						attack = self.hand.pop(event.key.name() - 1)
						return

			
		else:

			playableIndex = self.getAttackable(tablePlayed, defencePlayed)
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key.name().isdigit() and int(event.key.name()) in playableIndex:
						attack = self.hand.pop(event.key.name() - 1)
						return
					if event.key == pygame.K_n:
						return
		"""

		if attack != None and attack.suit == self.uberSuit: self.uberCount -= 1
		return attack

	def startDefence(self, tablePlayed):
		defence = None
		playableIndex = self.getDefendable(tablePlayed)
		bouncableIndex = self.getBounceable(tablePlayed)
		# pick from index

		if defence != None:
			if defence.suit == self.uberSuit: self.uberCount -= 1
			return defence

	def getIndex(self):
		return self.cardIndex
	def setIndex(self, index):
		self.cardIndex = index

	def execute(self):
		print("FUCK controller.execute()")
		"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key().isdigit() and self.input == True:
					self.setIndex(event.key())
					event.key()
		"""


