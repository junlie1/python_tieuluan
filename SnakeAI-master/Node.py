class Node(object):
    """A node representing a single part of the snake."""

    def __init__(self,row,col):
        self.row = row
        self.col = col
        self.fVal = 0
        self.hVal = 0
        self.gVal = 0
        self.parent = None

