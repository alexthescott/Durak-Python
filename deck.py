# Alex Scott
# Durak War Games
# Deck Class

from card import Card
from random import shuffle

class Deck:
	def __init__(self):
		self.suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
		self.ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
		self.cards = list()
		self.build()
		self.shuffle()

	def build(self):
		for s in self.suits:
			for r in self.ranks:
				self.cards.append(Card(s,r))

	def shuffle(self):
		shuffle(self.cards)

	def isEmpty(self):
		return len(self.cards) == 0;

	def size(self):
		return len(self.cards)

	def pop(self):
		if not self.isEmpty():
			return self.cards.pop()
		else:
			print("We are out of cards what in the lord's name do you think you're doing")

