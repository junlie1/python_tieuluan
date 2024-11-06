import random

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.fVal = 0
        self.hVal = 0
        self.gVal = 0
        self.parent = None

class SnakeLogic(object):
    def __init__(self):
        self.gameOver = False
        self.score = 0
        self.gameStarted = False
        self.canMove = True

        self.boardSize = 10 
        self.snakeBoard = []  

        self.snakeHead = {}  # lưu trữ hàng và cột của đầu rắn
        self.snakeSegments = []  # lưu trữ thân rắn ngoại trừ phần đầu, mục đích để giúp đầu tránh thân
        self.direction = ""

        self.foodPosition = {}  # lưu trữ vị trí của thức ăn
        self.obstaclePosition = {}

        self.loadSnakeBoard(self.boardSize)
        

    def isGameRunning(self):
        return self.gameStarted and not self.gameOver

    def isA_StarGameRunning(self):
        return self.comp

    def getBoard(self):
        return self.snakeBoard

    def snakeLength(self): 
        """Mục tiêu hàm này là trả về giá trị hiện tại của rắn"""
        highestVal = 0
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                highestVal = max(highestVal, self.snakeBoard[row][col])
        return highestVal

    def isGameOver(self, headRow, headCol):
        """Kiểm tra xem trò chơi kết thúc chưa
           1) Rắn đâm đầu vào tường
           2) Rắn tự đâm vào cơ thể của nó
           3) Rắn đâm vào chướng ngại vật
        """
        if headRow < 0 or headRow >= self.boardSize:
            self.gameOver = True
            return True
        if headCol < 0 or headCol >= self.boardSize:
            self.gameOver = True
            return True
        if self.isCollidingWithSelf(headRow, headCol):
            self.gameOver = True
            return True
        if self.isCollidingWithObstacles(headRow, headCol):
            self.gameOver = True
            return True
        return False

    def isCollidingWithSelf(self, headRow, headCol):
        """Kiểm tra đầu rắn với thân rắn có va chạm không"""
        self.setPositions() 
        for segment in self.snakeSegments:
            if segment['row'] == headRow and segment['col'] == headCol:
                return True
        return False
    
    def isCollidingWithObstacles(self, headRow, headCol):
        self.setPositions()
        if self.snakeBoard[headRow][headCol] == -3:
            return True
        return False

    def makeMove(self, direction):
        if not self.canMove:
            return
        self.direction = direction
        if self.direction == "Left":
            self.moveSnake(0, -1)
        elif self.direction == "Right":
            self.moveSnake(0, 1)
        elif self.direction == "Up":
            self.moveSnake(-1, 0)
        elif self.direction == "Down":
            self.moveSnake(1, 0)

    def loadSnakeBoard(self, size):
        """Khởi tạo danh sách 2D của snakeboard, đặt mặc định đầu rắn sẽ ở giữa màn hình
           thức ăn đặt rando
           0 = empty space
           -1 = food
           -3 = obstacle
           >1 = snake"""
        self.boardSize = size
        self.snakeBoard = [[0 for x in range(size)] for x in range(size)] #khởi tạo kích thước bảng là size x size
        self.snakeBoard[int(size / 2)][int(size / 2)] = 1
        self.makeFood()
        self.makeObstacles()

    def setPositions(self):
        """đảm bảo rằng các logic di chuyển, kiểm tra va chạm, và tìm đường trong trò chơi hoạt động đúng cách"""
        maxVal = self.snakeLength()
        self.snakeSegments = []
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.snakeBoard[row][col] == maxVal:
                    self.snakeHead['row'] = row
                    self.snakeHead['col'] = col
                elif self.snakeBoard[row][col] >= 1 and self.snakeBoard[row][col] < maxVal:
                    snakePart = {'row': row, 'col': col}
                    self.snakeSegments.append(snakePart)

    def removeTail(self):
        """rắn di chuyển mà không để lại dấu vết trên bảng"""
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                if self.snakeBoard[row][col] > 0:
                    self.snakeBoard[row][col] -= 1

    def getScore(self):
        return self.score

    def moveSnake(self, rowDiff, colDiff):
        """ Kiểm tra vị trị mới đầu rắn có gây kết thức game không
            Kiểm tra xem đã ăn thức ăn chưa
        """
        if not self.gameOver:
            self.setPositions()
            newHeadRow = self.snakeHead['row'] + rowDiff
            newHeadCol = self.snakeHead['col'] + colDiff
            if self.isGameOver(newHeadRow, newHeadCol):
                self.gameOver = True
                return
            headRank = self.snakeLength()
            if self.snakeBoard[newHeadRow][newHeadCol] == -1:
                self.snakeBoard[newHeadRow][newHeadCol] = headRank + 1
                self.score += 1
                self.makeFood()
            else:
                self.removeTail()
                self.snakeBoard[newHeadRow][newHeadCol] = headRank

    def makeFood(self):
        """Tạo thức ăn cho 1 vị trí trống"""
        width = self.boardSize
        row = random.choice(range(width))
        col = random.choice(range(width))
        # kiểm tra xem có phải ô trống không
        while self.snakeBoard[row][col] != 0:
            row = random.choice(range(width))
            col = random.choice(range(width))

        self.snakeBoard[row][col] = -1
        self.foodPosition['row'] = row
        self.foodPosition['col'] = col
        self.calculateManhattanBoard()

    def makeObstacles(self):
        """Tạo chướng ngại vật"""
        for _ in range(3): 
            width = self.boardSize
            row = random.choice(range(width))
            col = random.choice(range(width))
            # Kiểm tra xem có phải là ô trống không
            while self.snakeBoard[row][col] != 0:
                row = random.choice(range(width))
                col = random.choice(range(width))

            self.snakeBoard[row][col] = -3
            

    # A star Algorithm
    def calculateManhattanBoard(self):
        foodRow = self.foodPosition['row']
        foodCol = self.foodPosition['col']
        self.manhattanBoard = [[0 for x in range(self.boardSize)] for x in range(self.boardSize)]
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                manDistance = abs(foodRow - row) + abs(foodCol - col)
                self.manhattanBoard[row][col] = manDistance

    def heuristic(self, node):
        """calculates manhattan distance from the node to the food"""
        inf = float('inf') #để đánh dấu các nút k hợp lệ
        for snakePart in self.snakeSegments:
            snakeRow = snakePart['row']
            snakeCol = snakePart['col']
            if node.row == snakeRow and node.col == snakeCol:
                return inf
        headRow = self.snakeHead['row']
        headCol = self.snakeHead['col']
        if node.row == headRow and node.col == headCol:
            return inf
        if self.snakeBoard[node.row][node.col] == -3:
            return inf

        return abs(node.row - self.foodPosition['row']) + abs(node.col - self.foodPosition['col'])

    def setNodeBoard(self):
        self.nodeBoard = [[Node(row, col) for col in range(self.boardSize)] for row in range(self.boardSize)]

    def neighborNodes(self, node):
        surroundNodes = []
        if node.row - 1 >= 0:
            top = self.nodeBoard[node.row - 1][node.col]
            if self.isValidNode(top):
                surroundNodes.append(top)

        if node.col - 1 >= 0:
            left = self.nodeBoard[node.row][node.col - 1]
            if self.isValidNode(left):
                surroundNodes.append(left)

        if node.col + 1 < self.boardSize:
            right = self.nodeBoard[node.row][node.col + 1]
            if self.isValidNode(right):
                surroundNodes.append(right)

        if node.row + 1 < self.boardSize:
            bot = self.nodeBoard[node.row + 1][node.col]
            if self.isValidNode(bot):
                surroundNodes.append(bot)

        return surroundNodes

    def isValidNode(self, node):
        """Kiểm tra cái node hiện tại có thỏa không (không va chạm với thân và chướng ngại vật)"""
        if self.snakeBoard[node.row][node.col] > 0 or self.snakeBoard[node.row][node.col] == -3:
            return False
        return True

    def findMinNode(self, nodes):
        """tìm node với fVal là nhỏ nhất"""
        minNode = nodes[0]
        for node in nodes:
            if node.fVal < minNode.fVal:
                minNode = node
        return minNode
    

    #Hàm lưu trữ đường đi từ đích đến điểm bắt đầu đang xét
    def printPathList(self, end):
        while end.parent is not None:
            self.pathList.append([end.row, end.col])
            end = end.parent
        self.pathList.reverse()

    def calculateAstar(self):
        self.pathList = [] #lưu trữ đường đi tìm đc
        self.setPositions()
        self.setNodeBoard()
        openList = []
        closedList = []
        goal = Node(self.foodPosition['row'], self.foodPosition['col'])
        beginNode = self.nodeBoard[self.snakeHead['row']][self.snakeHead['col']]
        beginNode.gVal = 0
        beginNode.hVal = self.manhattanBoard[beginNode.row][beginNode.col]
        beginNode.fVal = beginNode.gVal + beginNode.hVal
        openList.append(beginNode)
        while openList:
            current = self.findMinNode(openList)  # node in openList with lowest fVal
            if current.row == goal.row and current.col == goal.col:
                self.printPathList(current)
                return self.pathList
            openList.remove(current)
            closedList.append(current)
            neighborsList = self.neighborNodes(current)

            for neighbor in neighborsList:  # for each neighbor of current
                if neighbor in closedList:
                    continue
                if neighbor not in openList:
                    neighbor.gVal = current.gVal + 1
                    neighbor.hVal = self.heuristic(neighbor)
                    neighbor.fVal = neighbor.gVal + neighbor.hVal
                    neighbor.parent = current
                    openList.append(neighbor)
                else:
                    newGval = current.gVal + 1
                    if newGval < neighbor.gVal:
                        neighbor.gVal = newGval
                        neighbor.parent = current

    def setDirection(self):
        if not self.pathList:
            if self.direction == "Left":
                self.moveSnake(0, -1)
            elif self.direction == "Right":
                self.moveSnake(0, 1)
            elif self.direction == "Up":
                self.moveSnake(-1, 0)
            elif self.direction == "Down":
                self.moveSnake(1, 0)
            self.gameOver = True 
            return 
        nextLocation = self.pathList.pop(0)
        nextRow, nextCol = nextLocation
        if self.snakeBoard[nextRow][nextCol] > 0:
            self.stall()
            return
        if nextRow == self.snakeHead['row'] and (nextCol - self.snakeHead['col']) == -1:  # left
            self.moveSnake(0, -1)
        elif nextRow == self.snakeHead['row'] and (nextCol - self.snakeHead['col']) == 1:  # right
            self.moveSnake(0, 1)
        elif (nextRow - self.snakeHead['row']) == -1 and nextCol == self.snakeHead['col']:  # up
            self.moveSnake(-1, 0)
        elif (nextRow - self.snakeHead['row']) == 1 and nextCol == self.snakeHead['col']:  # down
            self.moveSnake(1, 0)

    def stall(self):
        """Kiểm tra tất cả các hướng di chuyển có thể và chọn hướng an toàn nhất.
           Nếu không có hướng đi an toàn thì chọn 1 hướng ngẫu nhiên"""
        safeMoves = []

        if self.snakeHead['col'] - 1 >= 0 and self.snakeBoard[self.snakeHead['row']][self.snakeHead['col'] - 1] <= 0:  # left
            safeMoves.append((0, -1))
        if self.snakeHead['col'] + 1 < self.boardSize and self.snakeBoard[self.snakeHead['row']][self.snakeHead['col'] + 1] <= 0:  # right
            safeMoves.append((0, 1))
        if self.snakeHead['row'] - 1 >= 0 and self.snakeBoard[self.snakeHead['row'] - 1][self.snakeHead['col']] <= 0:  # up
            safeMoves.append((-1, 0))
        if self.snakeHead['row'] + 1 < self.boardSize and self.snakeBoard[self.snakeHead['row'] + 1][self.snakeHead['col']] <= 0:  # down
            safeMoves.append((1, 0))

        if safeMoves:
            # Chọn ngẫu nhiên một hướng đi an toàn
            possibleMoves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            move = random.choice(possibleMoves)
            self.moveSnake(move[0], move[1])
        else:
           self.gameOver = True

# Sử dụng lớp SnakeLogic
game = SnakeLogic()
game.gameStarted = True
while not game.gameOver:
    path = game.calculateAstar()
    if path:
        game.setDirection()
    else:
        game.stall()
