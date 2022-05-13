import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication

class ICT(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('ICalcThis')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ICT()
    sys.exit(app.exec_())
