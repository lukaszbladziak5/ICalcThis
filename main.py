from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import sys
import sql
import random
import quotes

import modules.hata
import modules.dB
import modules.friis

class ErrorDialog(QDialog):
    def __init__(self, msg = "Sorry, something went wrong"):
        super().__init__()

        self.setWindowTitle("ERROR")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class Ekran_poczatkowy(QDialog):

    def __init__(self):
        super(Ekran_poczatkowy, self).__init__()
        loadUi("UI/Wielki_poczatek.ui", self)
        self.przycisk_logowania.clicked.connect(self.logowanie)
        self.przycisk_nowe_konto.clicked.connect(self.rejestracja)

    def rejestracja(self):
        przycisk_nowe_konto = Ekran_rejestracji()
        widget.addWidget(przycisk_nowe_konto)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def logowanie(self):
        przycisk_logowania = Ekran_logowania()
        widget.addWidget(przycisk_logowania)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Ekran_logowania(QDialog):

    def __init__(self):
        super(Ekran_logowania, self).__init__()
        loadUi("UI/Logowanie.ui", self)
        self.pole_haslo.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki wpisujac haslo
        self.login.clicked.connect(self.funkcja_logowania)

    def funkcja_logowania(self):
        nazwa_uzytkownika = self.pole_nazwa_uzytkownika.text()
        haslo = self.pole_haslo.text()

        if (len(nazwa_uzytkownika) == 0 or len(haslo) == 0):
            self.blad.setText("Nieprawidłowa nazwa użytkownika lub hasło!")
        else:
            if sql.login(nazwa_uzytkownika, haslo):
                print("Logowanie powiodło się!")
                profil = Menu()
                widget.addWidget(profil)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.blad.setText("Nieprawidłowa nazwa użytkownika lub hasło!")


class Ekran_rejestracji(QDialog):

    def __init__(self):
        super(Ekran_rejestracji, self).__init__()
        loadUi("UI/Rejestracja.ui", self)
        self.pole_haslo2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pole_haslo2_podtwierdzenie.setEchoMode(QtWidgets.QLineEdit.Password)
        self.przycisk_zarejestruj.clicked.connect(self.funkcja_rejestracji)

    def funkcja_rejestracji(self):
        nazwa_uzytkownika_rejestracja = str(self.pole_nazwa_uzytkownika2.text())
        haslo_rejestracja = str(self.pole_haslo2.text())
        haslo2_rejestacja = str(self.pole_haslo2_podtwierdzenie.text())

        if (len(nazwa_uzytkownika_rejestracja) == 0 or len(haslo_rejestracja) == 0 or len(haslo2_rejestacja) == 0):
            self.blad2.setText("Proszę wypełnij puste pola.")
        elif haslo_rejestracja != haslo2_rejestacja:
            self.blad2.setText("Hasła są różne.")
        else:
            try:
                sql.register(nazwa_uzytkownika_rejestracja, haslo_rejestracja)
                profil = Menu()
                widget.addWidget(profil)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            except:
                dlg = ErrorDialog("Błąd - prawdopodobnie taki uzytkownik juz istnieje")
                if dlg.exec(): print("Error dialog prompted")


class Menu(QDialog):

    def __init__(self):
        super(Menu, self).__init__()
        loadUi("UI/Menu.ui", self)
        self.modelHaty_przycisk.clicked.connect(self.model_Haty)  # menu główne, przycisk 1
        self.rachunek_db_przycisk.clicked.connect(self.rachunek_db)  # menu główne, przycisk 2
        self.przycisk3_PrawoOhma.clicked.connect(self.Prawo_Ohma)
        self.operacja4_ONP.clicked.connect(self.ONP)
        self.rownanie_friisa_przycisk.clicked.connect(self.rownanie_friisa)

        quoteID = random.randint(0, quotes.ammount - 1)
        #quoteID = 17
        quote = quotes.quote[quoteID]
        self.menuQuote.setText("\"" + quote[0] + "\"")
        self.menuQuoteAuthor.setText("- " + quote[1])

    def model_Haty(self):
        modelHaty_przycisk = Model_Haty()
        widget.addWidget(modelHaty_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def rachunek_db(self):
        rachunek_db_przycisk = Rachunek_decybelowy()
        widget.addWidget(rachunek_db_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Prawo_Ohma(self):
        przycisk3_PrawoOhma = Prawo_Ohma()
        widget.addWidget(przycisk3_PrawoOhma)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def ONP(self):
        operacja4_ONP = Notacja_Polska()
        widget.addWidget(operacja4_ONP)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def rownanie_friisa(self):
        r_friisa = Rownanie_Friisa()
        widget.addWidget(r_friisa)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Model_Haty(QDialog):

    def __init__(self):
        super(Model_Haty, self).__init__()
        loadUi("UI/model_haty2.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)

    def go_to_clear_data(self):
        self.v_input_2.setValue(0)
        self.d_input_2.setValue(0)
        self.hB_input_2.setValue(0)
        self.hM_input_2.setValue(0)
        self.wynik_hata.setText('')
        self.wynikA.setText('')

    def go_to_save_data(self):
        if self.urban_button_2.isChecked():
            self.mode = 1
        if self.suburban_button_2.isChecked():
            self.mode = 2
        if self.open_button_2.isChecked():
            self.mode = 3
        self.f = self.v_input_2.value()
        self.d = self.d_input_2.value()
        self.base = self.hB_input_2.value()
        self.mob = self.hM_input_2.value()
        wynikAhms = -1
        wynik = -1
        try:
            wynikAhms = modules.hata.get_a(self.f, self.mob, self.mode)
            wynik = modules.hata.exec(self.f, self.d, self.base, self.mob, self.mode)
        except:
            dlg = ErrorDialog("Wprowadzono błędne dane!")
            if dlg.exec(): print("Error dialog prompted")
            wynikAhms = "NaN"
            wynik = "NaN"
        self.wynikA.setText(str(wynikAhms))
        self.wynik_hata.setText(str(wynik))

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Rachunek_decybelowy(QDialog):

    def __init__(self):
        super(Rachunek_decybelowy, self).__init__()
        loadUi("UI/Rachunek_db.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)
        self.wybor_konwersji.currentIndexChanged.connect(self._update_conversion_method)

        self.first_value = self.pierwsza_dana.value()
        self.second_value = self.druga_dana.value()
        self.jednostka_danych1.setText('dBW')
        self.druga_dana.hide()
        self.jednostka_danych2.hide()

    def _update_conversion_method(self):
        if self.wybor_konwersji.currentIndex() == 0:
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.jednostka_danych1.setText('dBW')
        elif self.wybor_konwersji.currentIndex() == 1:
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.jednostka_danych1.setText('dBm')
        elif self.wybor_konwersji.currentIndex() == 2:
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.jednostka_danych1.setText('dBW')
        elif self.wybor_konwersji.currentIndex() == 3:
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.jednostka_danych1.setText('dBm')
        elif self.wybor_konwersji.currentIndex() == 4:
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.jednostka_danych1.setText('W')
        elif self.wybor_konwersji.currentIndex() == 5:
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.jednostka_danych1.setText('dB')
        elif self.wybor_konwersji.currentIndex() == 6:
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.jednostka_danych1.setText('W')
            self.jednostka_danych2.setText('W')
        elif self.wybor_konwersji.currentIndex() == 7:
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.jednostka_danych1.setText('W')
        elif self.wybor_konwersji.currentIndex() == 8:
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.jednostka_danych1.setText('V')
            self.jednostka_danych2.setText('V')
#hhhhhhhhhhhhhhhhhhhhaaaaaaaaaaaaaaaaaaaaa
    def go_to_clear_data(self):
        self.wynik.setText('')
        self.pierwsza_dana.setValue(0)
        self.druga_dana.setValue(0)

    def _choose_mode(self):                             # przepraszam za składnię poniżej # wybaczam
        if self.wybor_konwersji.currentIndex() == 0: return modules.dB.dBWTodBm(self.first_value), "dBm"
        elif self.wybor_konwersji.currentIndex() == 1: return modules.dB.dBmTodBW(self.first_value), "dBW"
        elif self.wybor_konwersji.currentIndex() == 2: return modules.dB.dBWToW(self.first_value), "W"
        elif self.wybor_konwersji.currentIndex() == 3: return modules.dB.dBmToW(self.first_value), "W"
        elif self.wybor_konwersji.currentIndex() == 4: return modules.dB.WTodBm(self.first_value), "dBm"
        elif self.wybor_konwersji.currentIndex() == 5: return modules.dB.dBToRatio(self.first_value), "(ratio)"
        elif self.wybor_konwersji.currentIndex() == 6: return modules.dB.ratioTodB(self.first_value, self.second_value), "dB"
        elif self.wybor_konwersji.currentIndex() == 7: return modules.dB.lossTodB(self.first_value), "dB"
        elif self.wybor_konwersji.currentIndex() == 8: return modules.dB.voltageTodB(self.first_value, self.second_value), "dB"

    def go_to_save_data(self):
        try:
            self.first_value = self.pierwsza_dana.value()
            self.second_value = self.druga_dana.value()
            self.result, self.result_unit = self._choose_mode()
            self.wynik.setText(str(self.result))
            self.jednostka_wyniku.setText(str(self.result_unit))
        except:
            dlg = ErrorDialog()
            if dlg.exec(): print("Error dialog prompted")

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Prawo_Ohma(QDialog):

    def __init__(self):
        super(Prawo_Ohma, self).__init__()
        loadUi("UI/Prawo_Ohma.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Notacja_Polska(QDialog):

    def __init__(self):
        super(Notacja_Polska, self).__init__()
        loadUi("UI/Notacja_Polska.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Rownanie_Friisa(QDialog):

    def __init__(self):
        super(Rownanie_Friisa, self).__init__()
        loadUi("UI/Rownanie_frissa.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)
        self.stosunek_button.clicked.connect(self._button1Clicked)
        self.pr_button.clicked.connect(self._button2Clicked)
        self.pt_button.clicked.connect(self._button3Clicked)
        self.stosunek_button.setChecked(True)
        self._button1Clicked()

    def _button1Clicked(self):
        self.pr_tekst.hide()
        self.pr_input.hide()
        self.dBm_tekst.hide()
        self.pt_tekst.hide()
        self.pt_input.hide()
        self.dBm_tekst_2.hide()

    def _button2Clicked(self):
        self.pr_tekst.hide()
        self.pr_input.hide()
        self.dBm_tekst.hide()
        self.pt_tekst.show()
        self.pt_input.show()
        self.dBm_tekst_2.show()

    def _button3Clicked(self):
        self.pr_tekst.show()
        self.pr_input.show()
        self.dBm_tekst.show()
        self.pt_tekst.hide()
        self.pt_input.hide()
        self.dBm_tekst_2.hide()


    def go_to_clear_data(self):
        self.gt_input.setValue(0)
        self.gr_input.setValue(0)
        self.lambda_input.setValue(0)
        self.d_input.setValue(0)
        self.pr_input.setValue(0)
        self.pt_input.setValue(0)
        self.rownanie_tekst.setText('')
        self.wynik.setText('')
        self.jednostka_tekst.setText('')

    def go_to_save_data(self):
        self.Gt = self.gt_input.value()
        self.Gr = self.gr_input.value()
        self.wavelength = self.lambda_input.value()
        self.d = self.d_input.value()
        result = -1

        if self.stosunek_button.isChecked():
            self.rownanie_tekst.setText('Pr/Pt =')
            try:
                result = modules.friis.exec(self.Gt, self.Gr, self.wavelength, self.d)
            except:
                dlg = ErrorDialog("Wprowadzono błędne dane!")
                if dlg.exec(): print("Error dialog prompted")
                result = "NaN"
        if self.pr_button.isChecked():
            self.rownanie_tekst.setText('Pr =')
            self.jednostka_tekst.setText('[dBm]')
            self.Pt = self.pt_input.value()
            try:
                result = modules.friis.execPr(self.Gt, self.Gr, self.wavelength, self.d, self.Pt)
            except:
                dlg = ErrorDialog("Wprowadzono błędne dane!")
                if dlg.exec(): print("Error dialog prompted")
                result = "NaN"
        if self.pt_button.isChecked():
            self.rownanie_tekst.setText('Pt =')
            self.jednostka_tekst.setText('[dBm]')
            self.Pr = self.pr_input.value()
            try:
                result = modules.friis.execPt(self.Gt, self.Gr, self.wavelength, self.d, self.Pr)
            except:
                dlg = ErrorDialog("Wprowadzono błędne dane!")
                if dlg.exec(): print("Error dialog prompted")
                result = "NaN"
        self.wynik.setText(str(result))

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
welcome = Ekran_poczatkowy()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.setWindowTitle('ICalcThis')
widget.setWindowIcon(QtGui.QIcon('images/calculator_image.png'))
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
