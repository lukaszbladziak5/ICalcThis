from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import sys
import sqlite3
import modules.hata


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
            polaczenie = sqlite3.connect("baza_danych_uzytkownikow.db")
            cur = polaczenie.cursor()
            wiersz = 'SELECT password FROM login_info WHERE username =\'' + nazwa_uzytkownika + "\'"
            cur.execute(wiersz)
            rezultat = cur.fetchone()[0]
            if rezultat == haslo:
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
        nazwa_uzytkownika_rejestracja = self.pole_nazwa_uzytkownika2.text()
        haslo_rejestracja = self.pole_haslo2.text()
        haslo2_rejestacja = self.pole_haslo2_podtwierdzenie.text()

        if (len(nazwa_uzytkownika_rejestracja) == 0 or len(haslo_rejestracja) == 0 or len(haslo2_rejestacja) == 0):
            self.blad2.setText("Proszę wypełnij puste pola.")
        elif haslo_rejestracja != haslo2_rejestacja:
            self.blad2.setText("Hasła są różne.")
        else:
            polaczenie2 = sqlite3.connect("baza_danych_uzytkownikow.db")
            cur2 = polaczenie2.cursor()
            informacja_o_uzytkowniku = [nazwa_uzytkownika_rejestracja, haslo_rejestracja]
            cur2.execute('INSERT INTO login_info (username,password) VALUES (?,?)', informacja_o_uzytkowniku)

            polaczenie2.commit()
            polaczenie2.close()
            profil = Menu()
            widget.addWidget(profil)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class Menu(QDialog):

    def __init__(self):
        super(Menu, self).__init__()
        loadUi("UI/Menu.ui", self)
        self.modelHaty_przycisk.clicked.connect(self.model_Haty)  # menu główne, przycisk 1
        self.rachunek_db_przycisk.clicked.connect(self.rachunek_db)  # menu główne, przycisk 2
        self.operacja_3_przycisk.clicked.connect(self.operacja3)

    def model_Haty(self):
        modelHaty_przycisk = Model_Haty()
        widget.addWidget(modelHaty_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def rachunek_db(self):
        rachunek_db_przycisk = Rachunek_decybelowy()
        widget.addWidget(rachunek_db_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def operacja3(self):
        operacja_3_przycisk = Operacja3()
        widget.addWidget(operacja_3_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Model_Haty(QDialog):

    def __init__(self):
        super(Model_Haty, self).__init__()
        loadUi("UI/model_haty2.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)

        self.f = self.v_input_2.text()
        self.d = self.d_input_2.text()
        self.base = self.hB_input_2.text()
        self.mob = self.hM_input_2.text()

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
        wynikAhms = modules.hata.get_a(self.f, self.mob, self.mode)
        wynik = modules.hata.exec(self.f, self.d, self.base, self.mob, self.mode)
        self.wynikA.setText(str(wynikAhms))
        self.wynik_hata.setText(str(wynik))

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class Rachunek_decybelowy(QDialog):

    def __init__(self):
        super(Rachunek_decybelowy, self).__init__()
        loadUi("UI/Rachunek_db.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)

        self.first_value = self.pierwsza_dana.value()
        self.second_value = self.druga_dana.value()
        # self.result = self.wynik.value()

    def go_to_clear_data(self):
        self.wynik.setText('')
        self.pierwsza_dana.setValue(0)
        self.druga_dana.setValue(0)

    def _choose_mode(self):
        if self.wybor_konwersji.currentIndex() == 0:
            return modules.dB.dBWTodBm(self.first_value)

    def go_to_save_data(self):

        # wynik_obliczen = self._choose_mode()
        # self.wynik.setText(str(self.result))

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class Operacja3(QDialog):

    def __init__(self):
        super(Operacja3, self).__init__()
        loadUi("UI/Operacja3.ui", self)
        self.cofanie_przycisk.clicked.connect(self.cofanie)

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() - 1)


app = QApplication(sys.argv)
welcome = Ekran_poczatkowy()
widget = QtWidgets.QStackedWidget()
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
