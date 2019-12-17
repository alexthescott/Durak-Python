# Alex Scott
# Durak War Games
# SimpleAgent Class

# Always attack with the lowest attack
# Always add non-trump if possible, unless endgame
# Always defend to the fullest

from player import Player;

class SimpleAgent(Player):
	def __init__(self, name):
		Player.__init__(self, name)

	def startAttack(self, tablePlayed, defencePlayed):
		# First attack, play the lowest card
		if(len(defencePlayed) == 0):
			throw = self.hand.pop(0)

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
		throw = self.hand.pop(playableIndex[0] - 1)
		if throw.suit == self.uberSuit: 
			self.uberCount -= 1
		return throw