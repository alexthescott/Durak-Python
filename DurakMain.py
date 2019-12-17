#!/usr/bin/env python3
""" Inspired in part by https://github.com/k41n/durak-python
Alex Scott
alphaDurak 
Summer 2019
"""
import sys, pygame
import random
from DurakController import UI
from simpleAgent import SimpleAgent
from stupidAgent import StupidAgent
from DurakModel import Game
from DurakGUI import GUI

class Main(object):
	def __init__(self):
		self.isRunning = True
		self.Game = Game()
		self.GUI = GUI(self.Game)

		Alex = UI("Alex")
		Alpha = SimpleAgent("Alpha")
		Beta = StupidAgent("Beta")
		BetaTwo = StupidAgent("BetaTwo")

		self.Game.addPlayer(Alex)
		self.Game.addPlayer(Alpha)
		self.Game.addPlayer(Beta)
		#self.Game.addPlayer(BetaTwo)

	def getPlayerStringState(self):
		# Main must create self.Game
		defenderIndex = self.Game.getDefenderIndex()
		attackerIndex = self.Game.getAttackerIndex()

		playerString = ""
		for i, p in enumerate(self.Game.players):
			temp = p.name
			if i == defenderIndex: temp = p.name.lower()
			elif i == attackerIndex: temp = p.name.upper()
			playerString = playerString + temp + ", "

		return playerString

	def runGame(self):
		self.Game.start()

		while self.isRunning:
			self.GUI.displayWindow()
			self.GUI.displayTable()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE: return
					key = None
					
					if event.key == ord("1"): key = 1
					elif event.key == ord("2"): key = 2
					elif event.key == ord("3"): key = 3
					elif event.key == ord("4"): key = 4
					elif event.key == ord("5"): key = 5
					elif event.key == ord("6"): key = 6
					elif event.key == ord("7"): key = 7
					elif event.key == ord("8"): key = 8
					elif event.key == ord("9"): key = 9
					elif event.key == ord("0"): key = 0
					elif event.key == ord("n"): key = "n"
					elif event.key == ord("d"): key = "d"
					if key != None:
						self.Game.getPlayer("Alex").getInput(key)
					if key == "n":
						self.Game.nextPhase()
					if key == "d":
						print("Debug Game:")
						print(self.getPlayerStringState())





main = Main()
main.runGame()