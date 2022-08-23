import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import sqlite3


class Ekran_poczatkowy(QDialog):
    def __init__(self):
        super(Ekran_poczatkowy, self).__init__()
        loadUi("Wielki_poczatek.ui",self)
        self.Przycisk_logowania.clicked.connect(self.logowanie)
        self.Przycisk_nowe_konto.clicked.connect(self.Rejestracja)

    def Rejestracja(self):
        Przycisk_nowe_konto = Ekran_rejestracji()
        widget.addWidget(Przycisk_nowe_konto)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def logowanie(self):
        Przycisk_logowania = ekran_logowania()
        widget.addWidget(Przycisk_logowania)
        widget.setCurrentIndex(widget.currentIndex()+1)

class ekran_logowania(QDialog):
    def __init__(self):
        super(ekran_logowania,self).__init__()
        loadUi("Logowanie.ui",self)
        self.pole_haslo.setEchoMode(QtWidgets.QLineEdit.Password) #kropeczki wpisujac haslo

        self.login.clicked.connect(self.funkcja_logowania)

    def funkcja_logowania(self):
        nazwa_uzytkownika = self.pole_nazwa_uzytkownika.text()
        haslo = self.pole_haslo.text()

        if(len(nazwa_uzytkownika)== 0 or len(haslo)==0):
            self.blad.setText("Nieprawidłowa nazwa użytkownika, bądź hasło")
        else:
            polaczenie = sqlite3.connect("baza_danych_uzytkownikow.db")
            cur = polaczenie.cursor()
            wiersz = 'SELECT password FROM login_info WHERE username =\''+nazwa_uzytkownika+"\'"
            cur.execute(wiersz)
            rezultat= cur.fetchone()[0]
            if rezultat == haslo:
                print("Logowanie powiodło się!")
                profil = Menu()
                widget.addWidget(profil)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.blad.setText("Nieprawodłowa nazwa użytkownika bądz hasło")

class Ekran_rejestracji(QDialog):
    def __init__(self):
        super(Ekran_rejestracji, self).__init__()
        loadUi("Rejestracja.ui", self)
        self.pole_haslo2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pole_haslo2_podtwierdzenie.setEchoMode(QtWidgets.QLineEdit.Password)
        self.przycisk_zarejestruj.clicked.connect(self.funkcja_rejestracji)

    def funkcja_rejestracji(self):
        nazwa_uzytkownika_rejestracja = self.pole_nazwa_uzytkownika2.text()
        haslo_rejestracja= self.pole_haslo2.text()
        haslo2_rejestacja= self.pole_haslo2_podtwierdzenie.text()

        if(len(nazwa_uzytkownika_rejestracja)==0 or len(haslo_rejestracja)==0 or len(haslo2_rejestacja)==0):
            self.blad2.setText("Prosze wypełnij puste pola.")
        elif haslo_rejestracja!=haslo2_rejestacja:
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
        loadUi("Menu.ui", self)
        self.Operacja_1_przycisk.clicked.connect(self.Operacja1)                                   # menu główne, przycisk 1
        self.Operacja_2_przycisk.clicked.connect(self.Operacja2)                                    # menu główne, przycisk 2ss222
        self.Operacja_3_przycisk.clicked.connect(self.Operacja3)
    def Operacja1(self):
        Operacja_1_przycisk = Operacja1()
        widget.addWidget(Operacja_1_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def Operacja2(self):
        Operacja_2_przycisk = Operacja2()
        widget.addWidget(Operacja_2_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def Operacja3(self):
        Operacja_3_przycisk = Operacja3()
        widget.addWidget(Operacja_3_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)





class Operacja1(QDialog):
    def __init__(self):
        super(Operacja1, self).__init__()
        loadUi("Operacja1.ui", self)
        self.cofanie_przycisk.clicked.connect(self.cofanie)

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() - 1)



class Operacja2(QDialog):
    def __init__(self):
        super(Operacja2, self).__init__()
        loadUi("Operacja2.ui", self)
        self.cofanie_przycisk.clicked.connect(self.cofanie)

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() - 1)

class Operacja3(QDialog):
    def __init__(self):
        super(Operacja3, self).__init__()
        loadUi("Operacja3.ui", self)
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
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")