import math

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QWidget



class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("modules/model_haty.ui", self)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        # self.f = self.v_input.getDouble()
        # self.d = self.d_input.getText()
        # self.base = self.hB_input.getText()
        # self.mob = self.hM_input.getText()
        # if self.f != 0:
        #     print(self.f)

        if self.urban_button.isChecked():
            self.mode = 1
        if self.suburban_button.isChecked():
            self.mode = 2
        if self.open_button.isChecked():
            self.mode = 3



    def go_to_clear_data(self):
        self.v_input.setText('')
        self.d_input.setText('')
        self.hB_input.setText('')
        self.hM_input.setText('')


    def exec(self, f, d, base, mob, mode):
        if mode == 1: return self.get_urban(f, d, base, mob, 1)
        if mode == 2: return self.get_suburban(f, d, base, mob)
        if mode == 3: return self.get_open(f, d, base, mob)
        raise ValueError("Hata model: invalid mode")
        return -1


    def get_a(self, f, mob, mode):
        if mode == 1:
            return (1.1 * math.log10(f) - 0.7) * mob - (1.56 * math.log10(f) - 0.8)

        if mode == 2:
            if f < 200:
                return 8.29 * (math.pow(math.log10(1.54 * mob), 2)) - 1.1
            else:
                return 3.2 * (math.pow(math.log10(11.75 * mob), 2)) - 4.97

        return -1


    def get_urban(self, f, d, base, mob, mode=1):
        return 69.55 + 26.16 * math.log10(f) - self.get_a(f, mob, mode) - 13.83 * math.log10(base) + (
                44.9 - 6.55 * math.log10(base)) * math.log10(d)


    def get_suburban(self, f, d, base, mob):
        return self.get_urban(f, d, base, mob, 2) - 2 * math.pow(math.log10(f / 28), 2) - 5.4


    def get_open(self, f, d, base, mob):
        return self.get_urban(f, d, base, mob, 2) - 4.78 * math.pow(math.log10(f), 2) + 18.33 * math.log10(f) - 40.94
