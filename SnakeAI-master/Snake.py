

class Snake(object):
    snakeLength = 0

    def __init__(self):
        # Snake class
        self.snakeHead = {}  # store the row, and col location of the snake's head
        self.snakeSegments = []  # store row,col location of the snake segments except the head
        self.direction = ""

    def setSnakeLength(self):
        """Returns the current length of the snake"""
        highestVal = 0
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                highestVal = max(highestVal,self.snakeBoard[row][col])
        self.snakeLength = highestVal