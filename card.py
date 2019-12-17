# Alex Scott
# Durak War Games
# Card Class

class Card(object):
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	# Print Related Functions
	def show(self):
		print("{} of {}".format(self.rank, self.suit))
	def showChoice(self, uberSuit):
		if self.suit == uberSuit:
			print("+ {} of {}".format(self.rank, self.suit))
		else:
			print("- {} of {}".format(self.rank, self.suit))
	def printrank(self): 
		return str(self.rank) + " of " + self.suit

	# Comparison Functions
	def sameSuit(self, card):
		return self.suit == card.suit
	def sameRank(self, card):
		return self.rank == card.rank
	def isGreater(self, card):
		return self.rank > card.rank