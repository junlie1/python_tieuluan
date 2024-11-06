from tkinter import *
from tkinter import messagebox
from snakeLogic import SnakeLogic
from PIL import Image, ImageTk  # type: ignore # Pillow
import random
import os


class SnakeGUI(object):
    def __init__(self):
        self.boardSize = 10
        self.board = []
        self.root = Tk()
        self.root.title("Snake Game - group 3")

        # Thiết lập kích thước cửa sổ
        self.root.geometry("1060x800")  # Bạn có thể thay đổi kích thước này tùy ý

        # Đường dẫn đến ảnh nền
        bg_image_path = "background.png"  # Sử dụng đường dẫn tương đối nếu ảnh nằm trong cùng thư mục
        if os.path.exists(bg_image_path):
            try:
                self.bg_image = Image.open(bg_image_path)
                self.bg_image = self.bg_image.resize((1060, 800), Image.Resampling.LANCZOS)  # Đảm bảo ảnh vừa với cửa sổ
                self.bg_image = ImageTk.PhotoImage(self.bg_image)
            except Exception as e:
                print(f"Error loading image: {e}")
                messagebox.showerror("Error", f"Error loading image: {e}")
        else:
            self.bg_image = None
            messagebox.showerror("Error", f"Background image not found at {bg_image_path}")

        # Tạo giao diện chào mừng
        self.welcomeFrame = Frame(self.root, bg="lightblue")
        self.welcomeFrame.pack(fill=BOTH, expand=True)

        if self.bg_image:
            self.welcomeCanvas = Canvas(self.welcomeFrame, width=1088, height=800)
            self.welcomeCanvas.pack(fill=BOTH, expand=True)
            self.welcomeCanvas.create_image(0, 0, anchor=NW, image=self.bg_image)

            self.welcomeLabel = Label(self.welcomeCanvas, text="Welcome to Snake Game - Group 3!", font=("Helvetica", 24), bg="lightblue")
            self.welcomeCanvas.create_window(512, 100, window=self.welcomeLabel)  # Centered at top

            self.startButton = Button(self.welcomeCanvas, text="Start Game", command=self.showGame, font=("Helvetica", 14), bg="darkgreen", fg="white")
            self.welcomeCanvas.create_window(512, 200, window=self.startButton)  # Centered below label

            self.instructionsLabel = Label(self.welcomeCanvas, text="Use any keys to move!\nPress New Game to Restart your game!\nPress A* Run and then press any arrow key to watch the A* Algorithm Snake Player!", font=("Helvetica", 12), bg="lightblue", justify=LEFT)
            self.welcomeCanvas.create_window(512, 500, window=self.instructionsLabel)  # Centered below button
            
            self.instructionsLabel = Label (self.welcomeCanvas, text= "SNAKE GAME - GROUP 3", font=("Helvetica", 12), bg="lightblue")
            self.welcomeCanvas.create_window(512, 300, window=self.welcomeLabel)
            

        # Tạo giao diện game nhưng chưa hiển thị
        self.gameFrame = Frame(self.root)
        self.canvas = Canvas(self.gameFrame, width=(self.boardSize * 31), height=(self.boardSize * 31), bg="lightblue")
        self.canvas.pack(pady=20)

        if self.bg_image:
            self.canvas.create_image(0, 0, anchor=NW, image=self.bg_image)


        # Các thành phần điều khiển game
        button_font = ("Helvetica", 12, "bold")

        self.boardSizeEntryLabel = Label(self.gameFrame, text="Board Size:", font=("Helvetica", 14))
        self.boardSizeEntryLabel.pack(pady=5)
        self.boardSizeEntry = Entry(self.gameFrame, font=("Helvetica", 14))
        self.boardSizeEntry.pack()
        self.boardSizeEntry.insert(0, "10")  # Default value

        # self.obstacleLabel = Label(self.gameFrame, text="Number of Obstacles:", font=("Helvetica", 14))
        # self.obstacleLabel.pack(pady=5)
        # self.obstacleEntry = Entry(self.gameFrame, font=("Helvetica", 14))
        # self.obstacleEntry.pack(pady=5)
        # self.obstacleEntry.insert(0, "3")  # Default value

        self.newGameButton = Button(self.gameFrame, command=self.resetBoardSize, text='RESET', bg="green", fg="white", font=button_font)
        self.newGameButton.pack(pady=5)

        # Create a frame for the mode buttons
        self.modeButtonFrame = Frame(self.gameFrame)
        self.modeButtonFrame.pack(pady=5)

        self.playerModeButton = Button(self.modeButtonFrame, text="Người chơi", command=self.init, bg="pink", fg="white", font=button_font)
        self.playerModeButton.pack(side=LEFT, padx=10)

        self.CPUGameButton = Button(self.modeButtonFrame, text='A* Run', command=self.initA_Star, bg="pink", fg="white", font=button_font)
        self.CPUGameButton.pack(side=RIGHT, padx=10)

        # Frame chứa thông tin về thành phần game
        self.infoFrame = Frame(self.root, bg="lightgrey", width=192)
        self.infoFrame.pack(side=RIGHT, fill=Y)

        self.infoTitleLabel = Label(self.infoFrame, text="GHI CHÚ", font=("Helvetica", 16, "bold"), bg="lightgrey")
        self.infoTitleLabel.pack(pady=10)

        self.yellowLabel = Label(self.infoFrame, text="- Màu vàng là thức ăn", font=("Helvetica", 12), bg="lightgrey", fg="yellow")
        self.yellowLabel.pack(pady=5, anchor='w')

        self.redLabel = Label(self.infoFrame, text="- Màu đỏ là chướng ngại vật", font=("Helvetica", 12), bg="lightgrey", fg="red")
        self.redLabel.pack(pady=5, anchor='w')

        self.greenLabel = Label(self.infoFrame, text="- Màu xanh lá là con rắn", font=("Helvetica", 12), bg="lightgrey", fg="green")
        self.greenLabel.pack(pady=5, anchor='w')

        self.infoContentLabel = Label(self.infoFrame, text="- Reset: Điều chỉnh kích thước bảng\n\n- A* Run: Chọn chế độ chơi bằng thuật toán A*\n\n- Người chơi: Chọn chế độ người chơi", font=("Helvetica", 12), bg="lightgrey", justify=LEFT)
        self.infoContentLabel.pack(pady=10)
         
        # Tạo sự kiện & trạng thái ban đầu
        self.root.bind("<Key>", self.keyPressed)
        self.gameStarted = False
        self.isA_StarGameClicked = False
        self.isNewGameClicked = False
        self.printInstructions()
        self.computerPlay = False
        
        
        # Tạo logic cho game
        self.logic = SnakeLogic()

    def showGame(self):
        self.welcomeFrame.pack_forget()  # Ẩn giao diện chào mừng
        self.gameFrame.pack(fill=BOTH, expand=True)  # Hiển thị giao diện game

    def resetBoardSize(self):
        try:
            size = int(self.boardSizeEntry.get())
            if (10 <= size <= 14):
                self.boardSize = size
                self.canvas.config(width=(self.boardSize * 31), height=(self.boardSize * 31))
                self.isNewGameClicked = True
                self.logic.canMove = False
                self.newGame()
            else:
                messagebox.showerror("Error", "Vui lòng nhập giá trị kích thước bảng từ 10 đến 14")
        except ValueError:
            messagebox.showerror("Error", "Dữ liệu nhập không hợp lệ. Vui lòng nhập giá trị số.")

    
    def init(self):
        try:
            size = int(self.boardSizeEntry.get())
            if (10 <= size <= 14):
                self.boardSize = size
                self.canvas.config(width=(self.boardSize * 31), height=(self.boardSize * 31))
                self.isNewGameClicked = True
                self.logic.canMove = True
                self.newGame()
            else:
                messagebox.showerror("Please enter a value of Size Board between 10 and 14")
        except ValueError:
            messagebox.showerror("Invalid input. Please enter a value of Size Board between 10 and 14")

    def initA_Star(self):
        self.isA_StarGameClicked = True

    def newGame(self):
        self.gameOver = False
        self.gameStarted = False
        self.computerPlay = False
        self.printInstructions()
        self.score = 0
        self.board = [[0] * self.boardSize for _ in range(self.boardSize)]  # Tạo 1 bảng với kích thước mới
        self.redrawAll()

    def updateBoard(self, board):
        self.canvas.delete(ALL)
        self.board = board
        self.drawSnakeBoard()

    def gameOverScreen(self, score):
        """Outputs the Game Over screen in the GUI"""
        canvas_id = self.canvas.create_text(100, 50, anchor="nw")
        endText = "Game Over!\nYour score is:" + str(score)
        self.canvas.itemconfig(canvas_id, text=endText, fill='red')

    def timerFired(self, logic):
        """Delays the game by the tick time amount"""
        delay = 80 
        if self.isNewGameClicked:
            self.isNewGameClicked = False
            self.computerPlay = False
            logic.gameOver = False
            logic.loadSnakeBoard(self.boardSize)
            self.updateBoard(logic.getBoard())
            self.gameStarted = False
            logic.score = 0

        if self.isA_StarGameClicked:
            self.isA_StarGameClicked = False
            logic.gameOver = False
            logic.loadSnakeBoard(self.boardSize)
            self.gameStarted = False
            self.updateBoard(logic.getBoard())
            self.computerPlay = True
            logic.score = 0

        if self.gameStarted and not logic.gameOver:
            if self.computerPlay:
                logic.calculateAstar()
                logic.setDirection()
                self.updateBoard(logic.getBoard())
                self.redrawAll()
            else:
                if self.logic.canMove:  # Kiểm tra nếu rắn có thể di chuyển
                    logic.makeMove(self.direction)
                    self.updateBoard(logic.getBoard())
                    self.redrawAll()
                else:
                    self.updateBoard(logic.getBoard())
                    self.redrawAll()
            
        elif logic.gameOver:
            self.gameOver = True
            self.gameOverScreen(logic.getScore())
        else:
            self.redrawAll()

        self.canvas.after(delay, self.timerFired, logic)

    def drawSnakeBoard(self):
        """Take the 2D list board, and visualizes it into the GUI"""
        for row in range(self.boardSize):
            for col in range(self.boardSize):
                self.drawSnakeCell(row, col)

    def drawSnakeCell(self, row, col):
        """Helper function for drawSnakeBoard
           Draws the cell, which is represented as a rectangle, in the GUI
           if cell is where the snake is at, it has blue oval
           if cell is where the food is at, it has yellow oval"""
        margin = 5
        cellSize = 30
        left = margin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        board = self.board
        self.canvas.create_rectangle(left, top, right, bottom, fill="lightblue")
        
        if board[row][col] > 0:
            # draw part of the snake body
            self.canvas.create_oval(left, top, right, bottom, fill="green")
            if board[row][col] == self.logic.snakeLength():
                self.canvas.create_text(left + cellSize * 0.5, top + cellSize * 0.5, text="đuôi", font=("Helvetica", 10), fill="black")
                # # Mắt trái
                # self.canvas.create_oval(left + cellSize * 0.25, top + cellSize * 0.25,
                #                         left + cellSize * 0.4, top + cellSize * 0.4, fill="black")
                # # Mắt phải
                # self.canvas.create_oval(left + cellSize * 0.6, top + cellSize * 0.25,
                #                         left + cellSize * 0.75, top + cellSize * 0.4, fill="black")
        elif board[row][col] == -1:
            self.canvas.create_oval(left, top, right, bottom, fill="yellow")
        elif board[row][col] == -3:
            self.canvas.create_oval(left, top, right, bottom, fill="red")


    # def makeObstacle(self):
    #     width = self.boardSize
    #     row = random.choice(range(width-1))
    #     col = random.choice(range(width-1))
    #     # if we are at a location where snake already exists, keep looking for random blank space
    #     while self.snakeBoard[row][col] != 0:
    #         row = random.choice(range(width-1))
    #         col = random.choice(range(width-1))

    #     self.snakeBoard[row][col] = -3

    def redrawAll(self):
        """Deletes the current snakeBoard, and redraws a new snakeBoard with changed values"""
        self.canvas.delete(ALL)
        self.drawSnakeBoard()

    def keyPressed(self, event):
        """Input: Keyboard event
        1) Sets the direction data member given corresponding arrow-key event
        2) game starts from the moment key is pressed also"""
        self.direction = event.keysym
        self.gameStarted = True
        self.logic.makeMove(self.direction)

    def getDirection(self):
        return self.direction

    def printInstructions(self):
        """Print the instructions of the game in the Console"""
        print("Welcome to Snake Game!")
        print("Use the Arrow keys to move!")
        print("Press New Game to Restart your game!")
        print("Press A* Game and then press any arrow key to watch the A* Algorithm Snake Player!")


if __name__ == '__main__':
    SnakeGUI()