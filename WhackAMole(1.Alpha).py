#FEATURES THAT ARE IN THE WORKS:
#Add in grid options
#Mole Png Icons?
#Moles disappear between 0.5 to 1.5 seconds
#No Qlabel Final Score, instead a txt file to keep record.



#Importing the necessary and needed PyQt5 assets.
import sys
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
        self.score = 0

        self.timerLabel = QLabel('')
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timerLabel, alignment=Qt.AlignCenter)

        self.scoreLabel = QLabel('')
        self.scoreLabel.setAlignment(Qt.AlignCenter)
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
        self.buttons = [[QPushButton(' ') for col in range(3)] for row in range(3)]
        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                button.setFixedSize(100, 100)
                #Sets the buttons in the 3x3 grid.
                button.clicked.connect(lambda ch, row=row, col=col: self.buttonClicked(row, col))
                self.grid.addWidget(button, row, col)

        self.resetButton = QPushButton('Reset Game')
        self.resetButton.clicked.connect(self.resetGame)
        self.layout.addWidget(self.resetButton, alignment=Qt.AlignCenter)

        #Running the Random mole code + showing the window.
        self.placeRandomMole()
        self.show()

    #Places the random mole text on a random row and col.
    def placeRandomMole(self):
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        self.clearMoles()
        self.buttons[row][col].setText('ʕ •ᴥ•ʔ')

    #Replaces the mole button with " " when clicked
    def clearMoles(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].setText(' ')

    #The timer that will move a mole to a different square every 2 seconds.
    def startMoleTimer(self):
        self.mole_timer = QTimer(self)
        self.mole_timer.timeout.connect(self.placeRandomMole)
        self.mole_timer.start(2000)

    #The main code, so when the button is pressed and it has the mole text, it runs the other 2 codes.
    def buttonClicked(self, row, col):
        if self.buttons[row][col].text() == 'ʕ •ᴥ•ʔ':
            #The Score Value and Qlabel
            self.score += 10
            self.scoreLabel.setText(f'Score: {self.score}')
            #Resets the timer when 1 mole is clicked.
            self.mole_timer.start(2000)
            self.placeRandomMole()

    def startTimer(self):
        if not self.timer_set:
            #Input for what time limit should be set, with a minimum and maximum.
            time_limit, ok = QInputDialog.getInt(self, 'Set Timer', 'Enter time limit (seconds 15 to 60):', min=15, max=60)
            if ok:
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.updateTimer)
                self.time_remaining = time_limit
                #Code to update the time remaining.
                self.timerLabel.setText(f"Time remaining: {self.time_remaining} seconds")
                self.timer.start(1000)
                self.timer_set = True
                self.startMoleTimer()
            else:
                self.startTimer()

    def updateTimer(self):
        self.time_remaining -= 1
        self.timerLabel.setText(f"Time remaining: {self.time_remaining} seconds")
        #A loop to check if the timer has hit 0 yet, if it has, it runs the end game function.
        if self.time_remaining <= 0:
            self.timer.stop()
            self.endgame()

    #When the reset game button is pressed, this code runs and resets all the other code back to the start.
    def resetGame(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
        if hasattr(self, 'mole_timer'):
            self.mole_timer.stop()
        self.score = 0
        self.scoreLabel.setText('')
        self.timerLabel.setText('')
        self.timer_set = False
        self.clearMoles()
        self.startTimer()
        self.enable_buttons()
    
    #the end game function
    def endgame(self):
        self.disable_buttons()
        final_score_label = QLabel(f'Game Over! Final Score: {self.score}')
        final_score_label.setAlignment(Qt.AlignCenter)
        final_score_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: red;
                margin-top: 20px;
            }
        """)
        self.layout.addWidget(final_score_label, alignment=Qt.AlignCenter)
    
    #Disables button usage after it has been clicked or when the game is finished.
    def disable_buttons(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].setEnabled(False)

    #Enables the buttons when you want to play again.
    def enable_buttons(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].setEnabled(True)
#Ends the code.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhackAMole()
    sys.exit(app.exec_())
