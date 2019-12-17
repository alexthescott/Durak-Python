# Alex Scott
# Durak War Games
# Stupid Agent Class

# Attack with random card
# Never add cards to existing attack
# Always defend to the fullest

import random
from player import Player;

class StupidAgent(Player):
	def __init__(self, name):
		Player.__init__(self, name)

	def startAttack(self, tablePlayed, defencePlayed):
		# First attack, play random card
		if(len(defencePlayed) == 0):
			randomCardIndex = random.randint(0, len(self.hand) - 1)
			throw = self.hand.pop(randomCardIndex)

			if throw.suit == self.uberSuit: 
				self.uberCount -= 1
			return throw

		else:
			playableIndex = self.getPlayable(tablePlayed, defencePlayed)
			throw = self.hand.pop(playableIndex[0] - 1)

			if throw != None and self.endgame == False and throw.suit == self.uberSuit: 
				self.hand.insert(0, throw)
			else:
				return throw
				

	def startDefence(self, tablePlayed):
		# always defend regardless of cost
		attack = tablePlayed[0]
		playableIndex = self.getDefendable(tablePlayed)
		throw = self.hand[playableIndex[0] - 1]
		if throw.suit == self.uberSuit: 
			self.uberCount -= 1
		return throw