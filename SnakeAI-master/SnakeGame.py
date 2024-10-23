# from snakeGUI import SnakeGUI
from snakeLogic import SnakeLogic
from tkinter import *
from snakeGUI1 import SnakeGUI
class SnakeGame(object):
    def __init__(self):
        self.GUI = SnakeGUI()
        self.logic = SnakeLogic()
    def run(self):
        self.GUI.timerFired(self.logic)
    def updateGUI(self):
        self.GUI.updateBoard(self.logic.getBoard())
    def makeNewGame(self):
        self.logic.loadSnakeBoard(10)
    def isGameOver(self):
        return self.logic.gameOver
game = SnakeGame()
game.updateGUI()
game.run()
game.GUI.root.mainloop()