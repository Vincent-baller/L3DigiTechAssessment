#Importing the necessary and needed PyQt5 assets.
import sys
import os
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class WhackAMole(QWidget):


    def __init__(self):
        super().__init__()
        self.initUI()
        self.startTimer()


       
    #Setting the Geometry and Name for the window.
    def initUI(self):
        self.setWindowTitle('Whack-A-Mole')
        self.setGeometry(250, 250, 350, 450)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
       
        #Setting the Variable's states at the start of the code.
        self.timer_set = False
        self.selectGridSize()
        self.score = 0
        #Number to limit and track the moles. Which is used to make sure there is no overflow of them.
        self.active_moles = 0
        self.max_moles = 3
       
        self.timerLabel = QLabel('')
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timerLabel, alignment=Qt.AlignCenter)
 
        self.scoreLabel = QLabel('')
        self.scoreLabel.setAlignment(Qt.AlignCenter)
        #Creates a Qlabel with custom font sizing and a bordered box with a white backdrop.
        self.scoreLabel.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid black;
                padding: 10px;
                margin-top: 20px;
                font-size: 16px;
            }
        """)
        self.layout.addWidget(self.scoreLabel, alignment=Qt.AlignCenter)
       
        #Placing the Push buttons in columns and rows throughout the grid, their size and position.
        self.buttons = [[QPushButton(' ') for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = self.buttons[row][col]
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda ch, row=row, col=col: self.buttonClicked(row, col))
                self.grid.addWidget(button, row, col)


        #A Button to reset the game through multiple functions.
        self.resetButton = QPushButton('Reset Game')
        self.resetButton.clicked.connect(self.resetGame)
        self.layout.addWidget(self.resetButton, alignment=Qt.AlignCenter)


        #Running the Random mole code + showing the window.
        self.mole_timers = []
        self.placeRandomMole()
        self.show()


    def selectGridSize(self):
        #User selects the grid size of the game with a minimum of 3 and maximum of 5.
        self.grid_size, ok = QInputDialog.getInt(self, 'Grid Size', 'Enter grid size (3 for 3x3, 4 for 4x4, 5 for 5x5):', min=3, max=5)
        #will default to 4x4 if the choice is invalid.
        if not ok:
            self.grid_size = 4




    #Place the random mole text on a random row and col.
    def placeRandomMole(self):
        if self.active_moles >= self.max_moles:
            return 
        #This code makes it so that there is a limit of moles by keeping track of the current ones and making sure it doesn't exceed the set max value.   
        num_moles = random.randint(1, self.max_moles - self.active_moles)
        #Allows it so that the moles are able to appear on any of the grid sizes.
        positions = random.sample([(r, c) for r in range(self.grid_size) for c in range(self.grid_size)], num_moles)
        #Moles are now separated and won't disappear if a different one is clicked.
        for row, col in positions:
            if self.buttons[row][col].text() == ' ':
                self.buttons[row][col].setText('ʕ •ᴥ•ʔ')
                self.active_moles += 1
                self.startMoleTimer(row, col)


    #Replaces the mole button with " " when clicked
    def clearAllMoles(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.clearMole(row, col)


    def clearMole(self, row, col):
        if self.buttons[row][col].text() == 'ʕ •ᴥ•ʔ':
            self.buttons[row][col].setText(' ')
            self.active_moles -= 1


    #Starts an interval between moles appearing.
    def startMoleTimer(self, row, col):
        mole_timer = QTimer(self)
        mole_timer.setSingleShot(True)
        mole_timer.timeout.connect(lambda: self.onMoleTimeout(row, col))
        #Moles now have separate spawn rates and can appear in multiple instances.
        mole_timer.start(random.randint(1000, 3000))
        self.mole_timers.append(mole_timer)


    #A function that when the mole has overstayed the random time, it will run clear mole and placerandommole so it moves to a different button.
    def onMoleTimeout(self, row, col):
        self.clearMole(row, col)
        self.placeRandomMole()


    #The main code, so when the button is pressed and it has the mole text, it runs the other 2 codes.
    def buttonClicked(self, row, col):
         if self.buttons[row][col].text() == 'ʕ •ᴥ•ʔ':
             self.score += 10
             self.scoreLabel.setText(f'Score: {self.score}')
             self.clearMole(row, col)
     
    def startTimer(self):
        if not self.timer_set:
            #Input for what time limit should be set, with a minimum and maximum.
            time_limit, ok = QInputDialog.getInt(self, 'Set Timer', 'Enter time limit (seconds 15 to 60):', min=15, max=60)
            if ok:
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.updateTimer)
                self.time_remaining = time_limit
                self.timerLabel.setText(f"Time remaining: {self.time_remaining} seconds")
                self.timer.start(1000)
                self.timer_set = True
                self.placeRandomMole()
            else:
                self.startTimer()


    def updateTimer(self):
        self.time_remaining -= 1
        self.timerLabel.setText(f"Time remaining: {self.time_remaining} seconds")
        #A loop to check if the timer has hit 0 yet, if it has, it runs the end game function.
        if self.time_remaining <= 0:
            self.timer.stop()
            self.endgame()


    def resetGame(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
        #Stops all the independant Mole timers so that the moles freeze without spawning or despawning.
        for timer in self.mole_timers:
            timer.stop()
        self.mole_timers.clear()
        self.score = 0
        self.active_moles = 0
        self.scoreLabel.setText('')
        self.timerLabel.setText('')
        self.timer_set = False


        self.selectGridSize()


        #Clears the old grid, and redoes the buttons.
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
   
        self.buttons = [[QPushButton(' ') for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = self.buttons[row][col]
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda ch, row=row, col=col: self.buttonClicked(row, col))
                self.grid.addWidget(button, row, col)
   
        self.clearAllMoles()
        self.startTimer()
        self.enable_buttons()
   
    #the end game function, disables the mole buttons, stops timer, states score.
    def endgame(self):
        self.disable_buttons()
        for timer in self.mole_timers:
            timer.stop()
        self.mole_timers.clear()
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(f"Times up! Your Score: {self.score}")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.SaveScoreToFile()
  
    def SaveScoreToFile(self):
        try:
            #Finding the current Directory of the script to download the txt file there.
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "score.txt")
           
            #Opens/Creates the file and places the score in there.
            with open(file_path, "a") as file:
                file.write(f"Score: {self.score}\n")
        except Exception as e:
            print(f"An error occurred while saving the score: {e}")


    #Disables button usage when the game is finished.
    def disable_buttons(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.buttons[row][col].setEnabled(False)
    #Enables buttons when the function is used.
    def enable_buttons(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.buttons[row][col].setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhackAMole()
    sys.exit(app.exec_())
