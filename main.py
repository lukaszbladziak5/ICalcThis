from operator import mod
from turtle import position
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import sys
from PyQt5 import QtCore, QtWidgets

#Modules
import modules.binary
import modules.circuits
import modules.dB
import modules.friis
import modules.hata
import modules.mccluskey
import modules.radio
import modules.rpn

# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # set the title
#         self.setWindowTitle("Okno1")
#
#         # setting  the geometry of window
#         self.setGeometry(0, 100, 400, 300)
#
#         # creating a label widget
#         # by default label will display at top left corner
#         self.label_1 = QLabel("Witaj", self)
#         self.label_1.setStyleSheet("border: 1px solid black;")
#         self.label_1.resize(140, 40)
#         self.label_1.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_1.setFont(QFont('Arial', 20))
#         self.label_1.move(170, 100)
#         # moving position
#         self.closeButton = QPushButton(self)
#         self.closeButton.setText("Close")  # text
#         self.closeButton.setIcon(QIcon("close.png"))  # icon
#         self.closeButton.setShortcut('Q')  # shortcut key
#         self.closeButton.clicked.connect(self.close)
#         self.closeButton.setToolTip("Close the widget")  # Tool tip
#         self.closeButton.move(100, 100)
#
#         # setting font and size
#
#
#         self.show()


# class PushButton(QWidget):
#     def __init__(self):
#         super(PushButton,self).__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle("PushButton")
#         self.setGeometry(400,400,300,260)
#         self.closeButton = QPushButton(self)
#         self.closeButton.setText("Close")          #text
#         self.closeButton.setIcon(QIcon("close.png")) #icon
#         self.closeButton.setShortcut('Q')  #shortcut key
#         self.closeButton.clicked.connect(self.close)
#         self.closeButton.setToolTip("Close the widget") #Tool tip
#         self.closeButton.move(100,100)

  
if __name__ == '__main__':

    # # create pyqt5 app
    # App = QApplication(sys.argv)
    #
    # # create the instance of our Window
    # window = Window()
    # ex = PushButton()
    #
    # # start the app
    # sys.exit(App.exec())
    app = QApplication(sys.argv)
    welcome = modules.hata.WelcomeScreen()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(welcome)
    widget.setFixedHeight(600)
    widget.setFixedWidth(800)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")