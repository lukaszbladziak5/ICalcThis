from operator import mod
from turtle import position
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys
from PyQt5 import QtCore

#Modules
import modules.hata
import modules.binary
  
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
  
        # set the title
        self.setWindowTitle("Label")
  
        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)
  
        # creating a label widget
        # by default label will display at top left corner
        self.label_1 = QLabel("Arial font", self)
        self.label_1.setStyleSheet("border: 1px solid black;")
        self.label_1.resize(140, 40)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setFont(QFont('Arial', 20))
        self.label_1.move(170, 100)
        # moving position
       
  
        # setting font and size
       
  
        self.show()
  
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())