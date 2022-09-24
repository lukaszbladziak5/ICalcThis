from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

import sys
import sql
import modules.hata
import modules.dB
import modules.friis
import modules.circuits
import modules.mccluskey
import modules.boolean
import modules.radio
import modules.fiber
import modules.binary
import modules.rpn


login = ""
def setLogin(user):
    global login
    login = user
def getLogin(): return login

class ErrorDialog(QDialog):

    def __init__(self, msg="Sorry, something went wrong"):
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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

class Ekran_logowania(QDialog):

    def __init__(self):
        super(Ekran_logowania, self).__init__()
        loadUi("UI/Logowanie.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.pole_haslo.setEchoMode(QtWidgets.QLineEdit.Password)  # kropeczki wpisujac haslo
        self.login.clicked.connect(self.funkcja_logowania)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

    def funkcja_logowania(self):
        nazwa_uzytkownika = self.pole_nazwa_uzytkownika.text()
        haslo = self.pole_haslo.text()
        setLogin(nazwa_uzytkownika)
        try:
            if sql.login(nazwa_uzytkownika, haslo):
                print("Logowanie powiodło się!")
                profil = Menu()
                widget.addWidget(profil)
                widget.setCurrentIndex(widget.currentIndex() + 1)
        except:
            dlg = ErrorDialog("Podano nieprawidłowe dane logowania! Spróbuj ponownie.")
            if dlg.exec(): print("Error dialog prompted")

    def cofanie(self):
        cofanie_przycisk = Ekran_poczatkowy()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Ekran_rejestracji(QDialog):

    def __init__(self):
        super(Ekran_rejestracji, self).__init__()
        loadUi("UI/Rejestracja.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.pole_haslo2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pole_haslo2_podtwierdzenie.setEchoMode(QtWidgets.QLineEdit.Password)
        self.przycisk_zarejestruj.clicked.connect(self.funkcja_rejestracji)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

    def funkcja_rejestracji(self):

        nazwa_uzytkownika_rejestracja = str(self.pole_nazwa_uzytkownika2.text())
        haslo_rejestracja = str(self.pole_haslo2.text())
        haslo2_rejestacja = str(self.pole_haslo2_podtwierdzenie.text())
        setLogin(nazwa_uzytkownika_rejestracja)

        if (len(nazwa_uzytkownika_rejestracja) == 0 or len(haslo_rejestracja) == 0 or len(haslo2_rejestacja) == 0):
            self.blad2.setText("Proszę wypełnij puste pola.")
        elif haslo_rejestracja != haslo2_rejestacja:
            self.blad2.setText("Hasła są różne.")
        else:
            try:
                if(sql.register(nazwa_uzytkownika_rejestracja, haslo_rejestracja) == False): raise SystemError("User already exist!")
                profil = Profil()
                widget.addWidget(profil)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            except:
                dlg = ErrorDialog("Błąd - prawdopodobnie taki użytkownik już istnieje!")
                if dlg.exec(): print("Error dialog prompted")

    def cofanie(self):
        cofanie_przycisk = Ekran_poczatkowy()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Profil(QDialog):

    def __init__(self):
        super(Profil, self).__init__()
        loadUi("UI/Profil.ui", self)

        self.commandLinkButton.clicked.connect(self.cofanie)
        self.przycisk_zaladuj.clicked.connect(self.on_click)
        self.przycisk_kontynuuj.clicked.connect(self.ZapisProfilu)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def on_click(self):
        print('PyQt5 button click')
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)

    def ZapisProfilu(self):
        Specjalizacja_index = self.wybor_specializacji.currentIndex()
        Specializacja = str(self.wybor_specializacji.itemText(Specjalizacja_index))
        Pseudonim = str(self.pole_pseudonim.text())
        Imie = str(self.pole_imie.text())
        Nazwisko = str(self.pole_naziwsko.text())
        if (len(Pseudonim) == 0 or len(Imie) == 0 or len(Nazwisko) == 0):
            self.blad2.setText("Proszę wypełnij puste pola.")
        else:
            sql.updateUserData(login,Pseudonim,Imie,Nazwisko,Specializacja)
        profil = Menu()
        widget.addWidget(profil)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Menu(QDialog):

    def __init__(self):
        super(Menu, self).__init__()
        loadUi("UI/Menu.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.wyborOperacjiTekst.setText( "Witaj " + getLogin() + "! Wybierz operację." )
        self.modelHaty_przycisk.clicked.connect(self.model_Haty)  # menu główne, przycisk 1
        self.rachunek_db_przycisk.clicked.connect(self.rachunek_db)  # menu główne, przycisk 2
        self.obwodyElektryczne_przycisk.clicked.connect(self.obwody_elektryczne)
        self.operacja4_ONP.clicked.connect(self.ONP)
        self.rownanie_friisa_przycisk.clicked.connect(self.rownanie_friisa)
        self.radio_przycisk.clicked.connect(self.radio)
        self.fiber_przycisk.clicked.connect(self.fiber)
        self.binary_button.clicked.connect(self.binary)
        self.mccluskey_przycisk.clicked.connect(self.mccluskey) # button 9

        self.profil_menu.setIcon(QtGui.QIcon('images/profilowe.jpg'))
        self.profil_menu.setIconSize(QtCore.QSize(140, 80))
        self.profil_menu.clicked.connect(self.Profil_edycja)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()
         
    def model_Haty(self):
        modelHaty_przycisk = Model_Haty()
        widget.addWidget(modelHaty_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def rachunek_db(self):
        rachunek_db_przycisk = Rachunek_decybelowy()
        widget.addWidget(rachunek_db_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def obwody_elektryczne(self):
        obwodyElektryczne_przycisk = Obwody_elektryczne()
        widget.addWidget(obwodyElektryczne_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def ONP(self):
        operacja4_ONP = Notacja_Polska()
        widget.addWidget(operacja4_ONP)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def rownanie_friisa(self):
        r_friisa = Rownanie_Friisa()
        widget.addWidget(r_friisa)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def radio(self):
        radio = Radio()
        widget.addWidget(radio)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def fiber(self):
        fiber = Fiber()
        widget.addWidget(fiber)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def binary(self):
        bin = Binary()
        widget.addWidget(bin)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def mccluskey(self):
        mccluskey = McCluskey()
        widget.addWidget(mccluskey)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Profil_edycja(self):
        profil_ed = Profil_edycja()
        widget.addWidget(profil_ed)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def cofanie(self):
        cofanie_przycisk = Ekran_poczatkowy()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Profil_edycja(QDialog):

    def __init__(self):
        super(Profil_edycja, self).__init__()
        loadUi("UI/Edycja_profilu.ui", self)
        user = sql.getUserData(login)
        self.wybor_specializacji.setCurrentIndex( (self.wybor_specializacji.findText(user[0])) )
        self.pole_pseudonim.setText(user[1])
        self.pole_imie.setText(user[2])
        self.pole_naziwsko.setText(user[3])
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.przycisk_zaladuj.clicked.connect(self.on_click)
        self.przycisk_kontynuuj.clicked.connect(self.ZapisProfilu)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def on_click(self):
        print('PyQt5 button click')
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap)

    def ZapisProfilu(self):
        Specjalizacja_index = self.wybor_specializacji.currentIndex()
        Specializacja = str(self.wybor_specializacji.itemText(Specjalizacja_index))
        Pseudonim = str(self.pole_pseudonim.text())
        Imie = str(self.pole_imie.text())
        Nazwisko = str(self.pole_naziwsko.text())
        if (len(Pseudonim) == 0 or len(Imie) == 0 or len(Nazwisko) == 0):
            self.blad2.setText("Proszę wypełnij puste pola.")
        else:
            print(Specializacja)
            sql.updateUserData(login,Pseudonim,Imie,Nazwisko, Specializacja)
        profil = Menu()
        widget.addWidget(profil)
        widget.setCurrentIndex(widget.currentIndex() + 1)
  
class Model_Haty(QDialog):

    def __init__(self):
        super(Model_Haty, self).__init__()
        loadUi("UI/model_haty2.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

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

    def go_to_clear_data(self):
        self.wynik.setText('')
        self.pierwsza_dana.setValue(0)
        self.druga_dana.setValue(0)

    def _choose_mode(self):  # przepraszam za składnię poniżej # wybaczam
        if self.wybor_konwersji.currentIndex() == 0:
            return modules.dB.dBWTodBm(self.first_value), "dBm"
        elif self.wybor_konwersji.currentIndex() == 1:
            return modules.dB.dBmTodBW(self.first_value), "dBW"
        elif self.wybor_konwersji.currentIndex() == 2:
            return modules.dB.dBWToW(self.first_value), "W"
        elif self.wybor_konwersji.currentIndex() == 3:
            return modules.dB.dBmToW(self.first_value), "W"
        elif self.wybor_konwersji.currentIndex() == 4:
            return modules.dB.WTodBm(self.first_value), "dBm"
        elif self.wybor_konwersji.currentIndex() == 5:
            return modules.dB.dBToRatio(self.first_value), "(ratio)"
        elif self.wybor_konwersji.currentIndex() == 6:
            return modules.dB.ratioTodB(self.first_value, self.second_value), "dB"
        elif self.wybor_konwersji.currentIndex() == 7:
            return modules.dB.lossTodB(self.first_value), "dB"
        elif self.wybor_konwersji.currentIndex() == 8:
            return modules.dB.voltageTodB(self.first_value, self.second_value), "dB"

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


class Obwody_elektryczne(QDialog):

    def __init__(self):
        super(Obwody_elektryczne, self).__init__()
        loadUi("UI/Prawo_Ohma.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.reset_button_2.clicked.connect(self.go_to_clear_data2)
        self.oblicz_button.clicked.connect(self.go_to_save_data)
        self.oblicz_button_2.clicked.connect(self.go_to_save_data2)
        self.wybor_polaczenia.currentIndexChanged.connect(self._update_conversion_method)
        self.wybor_polaczenia_2.currentIndexChanged.connect(self._update_conversion_method2)

        self.rezystory.setGeometry(30, 300, 201, 82)
        self.kondensatory.setGeometry(360, 300, 179, 100)
        self.rezystory.setStyleSheet("background-image : url(images/szeregowe1.png)")
        self.kondensatory.setStyleSheet("background-image : url(images/szeregowe_kondensator.png)")
        self.o1_tekst.setText('U =')
        self.o2_tekst.setText('I =')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

    def _update_conversion_method(self):
        if self.wybor_polaczenia.currentIndex() == 0:
            self.rezystory.setGeometry(30, 300, 201, 82)
            self.kondensatory.setGeometry(360, 300, 179, 100)
            self.rezystory.setStyleSheet("background-image : url(images/szeregowe1.png)")
            self.rezystory_tekst.setText("Połączenie szeregowe rezystorów")
            self.kondensatory.setStyleSheet("background-image : url(images/szeregowe_kondensator.png)")
            self.kondensatory_tekst.setText("Połączenie szeregowe kondensatorów")
        elif self.wybor_polaczenia.currentIndex() == 1:
            self.rezystory.setGeometry(30, 300, 138, 112)
            self.kondensatory.setGeometry(360, 300, 211, 150)
            self.rezystory.setStyleSheet("background-image : url(images/rownolegle1.png)")
            self.rezystory_tekst.setText("Połączenie równoległe rezystorów")
            self.kondensatory.setStyleSheet("background-image : url(images/rownolegle_kondensator.png)")
            self.kondensatory_tekst.setText("Połączenie równoległe kondensatorów")

    def _update_conversion_method2(self):
        if self.wybor_polaczenia_2.currentIndex() == 0:
            self.o2_tekst.show()
            self.o2_input.show()
            self.o1_tekst.setText('U =')
            self.o2_tekst.setText('I =')
        elif self.wybor_polaczenia_2.currentIndex() == 1:
            self.o2_tekst.show()
            self.o2_input.show()
            self.o1_tekst.setText('R =')
            self.o2_tekst.setText('I =')
        elif self.wybor_polaczenia_2.currentIndex() == 2:
            self.o2_tekst.show()
            self.o2_input.show()
            self.o1_tekst.setText('R =')
            self.o2_tekst.setText('U =')
        elif self.wybor_polaczenia_2.currentIndex() == 3:
            self.o2_tekst.show()
            self.o2_input.show()
            self.o1_tekst.setText('U =')
            self.o2_tekst.setText('I =')
        elif self.wybor_polaczenia_2.currentIndex() == 4:
            self.o2_tekst.show()
            self.o2_input.show()
            self.o1_tekst.setText('I =')
            self.o2_tekst.setText('R =')
        elif self.wybor_polaczenia_2.currentIndex() == 5:
            self.o2_tekst.hide()
            self.o2_input.hide()
            self.o1_tekst.setText('MAX =')

    def go_to_clear_data(self):
        self.wynik.setText('')
        self.jednostka_wyniku.setText('')
        self.wynik_2.setText('')
        self.jednostka_wyniku_2.setText('')
        self.r1_input.setValue(0)
        self.r2_input.setValue(0)
        self.c1_input.setValue(0)
        self.c2_input.setValue(0)

    def go_to_clear_data2(self):
        self.wynik_3.setText('')
        self.jednostka_wyniku_3.setText('')
        self.o1_input.setValue(0)
        self.o2_input.setValue(0)

    def _choose_mode(self):
        if self.wybor_polaczenia.currentIndex() == 0:
            return modules.circuits.resistorSeries(self.r_first_value, self.r_second_value), "Ω", modules.circuits.capacitorSeries(self.c_first_value, self.c_second_value), "F"
        elif self.wybor_polaczenia.currentIndex() == 1:
            return modules.circuits.resistorParallel(self.r_first_value, self.r_second_value), "Ω", modules.circuits.capacitorParallel(self.c_first_value, self.c_second_value), "F"

    def _choose_mode2(self):
        if self.wybor_polaczenia_2.currentIndex() == 0:
            return modules.circuits.ohmLawR(self.o_first_value, self.o_second_value), "Ω"
        elif self.wybor_polaczenia_2.currentIndex() == 1:
            return modules.circuits.ohmLawU(self.o_first_value, self.o_second_value), "V"
        elif self.wybor_polaczenia_2.currentIndex() == 2:
            return modules.circuits.ohmLawI(self.o_first_value, self.o_second_value), "A"
        elif self.wybor_polaczenia_2.currentIndex() == 3:
            return modules.circuits.powerUI(self.o_first_value, self.o_second_value), "W"
        elif self.wybor_polaczenia_2.currentIndex() == 4:
            return modules.circuits.powerIR(self.o_first_value, self.o_second_value), "W"
        elif self.wybor_polaczenia_2.currentIndex() == 5:
            return modules.circuits.RMS(self.o_first_value), "(RMS)"

    def go_to_save_data(self):
        try:
            self.r_first_value = self.r1_input.value()
            self.r_second_value = self.r2_input.value()
            self.c_first_value = self.c1_input.value()
            self.c_second_value = self.c2_input.value()
            self.r_result, self.r_result_unit, self.c_result, self.c_result_unit = self._choose_mode()
            self.wynik.setText("R = " + str(self.r_result))
            self.jednostka_wyniku.setText(str(self.r_result_unit))
            self.wynik_2.setText("C = " + str(self.c_result))
            self.jednostka_wyniku_2.setText(str(self.c_result_unit))
        except:
            dlg = ErrorDialog()
            if dlg.exec(): print("Error dialog prompted")

    def go_to_save_data2(self):
        try:
            self.o_first_value = self.o1_input.value()
            self.o_second_value = self.o2_input.value()
            self.o_result, self.o_result_unit = self._choose_mode2()
            self.wynik_3.setText(str(self.o_result))
            self.jednostka_wyniku_3.setText(str(self.o_result_unit))
        except:
            dlg = ErrorDialog()
            if dlg.exec(): print("Error dialog prompted")

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Notacja_Polska(QDialog):

    mode = 2

    def __init__(self):
        super(Notacja_Polska, self).__init__()
        loadUi("UI/Notacja_Polska.ui", self)
        self.wynik.setText("")
        self.wybor_notacji.setCurrentIndex(2)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.oblicz_button.clicked.connect(self.go_to_save_data)
        self.reset_button.clicked.connect(self.go_to_clear_data)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_save_data(self):
        input = self.ONP_wejscie.toPlainText()
        result = ""
        try:
            mode = self.wybor_notacji.currentIndex()
            if(mode == 0):
                #Zwykła
                echo(mode)
            elif(mode == 1):
                #NP
                echo(mode)
            elif(mode == 2):
                #ONP
                result = modules.rpn.evaluate(input)
            else: raise ValueError("RPN: invalid operation mode")
            self.wynik.setText(str(result))
        except:
            dlg = ErrorDialog("Błąd danych")
            if dlg.exec(): print("Error dialog prompted")

    def go_to_clear_data(self):
        self.ONP_wejscie.setText("")
        self.wynik.setText("")


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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

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

class Binary(QDialog):

    def __init__(self):
        super(Binary, self).__init__()
        loadUi("UI/Binary.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.binButton.clicked.connect(self.save_data_bin)
        self.octButton.clicked.connect(self.save_data_oct)
        self.decButton.clicked.connect(self.save_data_dec)
        self.hexButton.clicked.connect(self.save_data_hex)

    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_clear_data(self):
        self.Bin.setText("")
        self.Oct.setText("")
        self.Dec.setText("")
        self.Hex.setText("")
        self.ZM.setText("")
        self.U1.setText("")
        self.U2.setText("")
        self.bitLength.setText("")

    def save_data_bin(self):
        try:
            length = self.bitLength.toPlainText()
            if(length == ""): length = 32
            else: length = int(length)
            bin = self.Bin.toPlainText()
            dec = modules.binary.exec(bin, 2, 10)
            oct = modules.binary.exec(dec, 10, 8)
            hex = modules.binary.exec(dec, 10, 16)
            zm = modules.binary.decToZM(dec, length)
            u1 = modules.binary.decToU1(dec, length)
            u2 = modules.binary.decToU2(dec, length)

            self.Oct.setText(oct)
            self.Dec.setText(str(dec))
            self.Hex.setText(hex)
            self.ZM.setText(zm)
            self.U1.setText(u1)
            self.U2.setText(u2)
        except:
            dlg = ErrorDialog("Błąd danych")
            if dlg.exec(): print("Error dialog prompted")

    def save_data_oct(self):
        try:
            length = self.bitLength.toPlainText()
            if(length == ""): length = 32
            else: length = int(length)
            oct = self.Oct.toPlainText()
            dec = modules.binary.exec(oct, 8, 10)
            bin = modules.binary.exec(dec, 10, 2)
            hex = modules.binary.exec(dec, 10, 16)
            zm = modules.binary.decToZM(dec, length)
            u1 = modules.binary.decToU1(dec, length)
            u2 = modules.binary.decToU2(dec, length)

            self.Bin.setText(bin)
            self.Dec.setText(str(dec))
            self.Hex.setText(hex)
            self.ZM.setText(zm)
            self.U1.setText(u1)
            self.U2.setText(u2)
        except:
            dlg = ErrorDialog("Błąd danych")
            if dlg.exec(): print("Error dialog prompted")

    def save_data_dec(self):
        try:
            length = self.bitLength.toPlainText()
            if(length == ""): length = 32
            else: length = int(length)
            dec = int(self.Dec.toPlainText())
            bin = modules.binary.exec(dec, 10, 2)
            oct = modules.binary.exec(dec, 10, 8)
            hex = modules.binary.exec(dec, 10, 16)
            zm = modules.binary.decToZM(dec, length)
            u1 = modules.binary.decToU1(dec, length)
            u2 = modules.binary.decToU2(dec, length)

            self.Oct.setText(oct)
            self.Bin.setText(bin)
            self.Hex.setText(hex)
            self.ZM.setText(zm)
            self.U1.setText(u1)
            self.U2.setText(u2)
        except:
            dlg = ErrorDialog("Błąd danych")
            if dlg.exec(): print("Error dialog prompted")

    def save_data_hex(self):
        try:
            length = self.bitLength.toPlainText()
            if(length == ""): length = 32
            else: length = int(length)
            hex = self.Hex.toPlainText()
            dec = modules.binary.exec(hex, 16, 10)
            bin = modules.binary.exec(dec, 10, 2)
            oct = modules.binary.exec(dec, 10, 8)
            zm = modules.binary.decToZM(dec, length)
            u1 = modules.binary.decToU1(dec, length)
            u2 = modules.binary.decToU2(dec, length)

            self.Oct.setText(oct)
            self.Bin.setText(bin)
            self.Dec.setText(str(dec))
            self.ZM.setText(zm)
            self.U1.setText(u1)
            self.U2.setText(u2)
        except:
            dlg = ErrorDialog("Błąd danych")
            if dlg.exec(): print("Error dialog prompted")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

class Radio(QDialog):

    def __init__(self):
        super(Radio, self).__init__()
        loadUi("UI/Radio.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)
        self.wybor_konwersji.currentIndexChanged.connect(self._update_conversion_method)
        self._hide_buttons()

        self.first_value = self.pierwsza_dana.value()
        self.second_value = self.druga_dana.value()
        self.third_value = self.trzecia_dana.value()
        self.fourth_value = self.czwarta_dana.value()
        self.fifth_value = self.piata_dana.value()
        self.sixth_value = self.szosta_dana.value()
        self.seventh_value = self.siodma_dana.value()

        self.dana1.setText('λ =')
        self.jednostka_danych1.setText('m')

    def _hide_buttons(self):

        self.dana2.hide()
        self.druga_dana.hide()
        self.jednostka_danych2.hide()
        self.dana3.hide()
        self.trzecia_dana.hide()
        self.jednostka_danych3.hide()
        self.dana4.hide()
        self.czwarta_dana.hide()
        self.jednostka_danych4.hide()
        self.dana5.hide()
        self.piata_dana.hide()
        self.jednostka_danych5.hide()
        self.dana6.hide()
        self.szosta_dana.hide()
        self.jednostka_danych6.hide()
        self.dana7.hide()
        self.siodma_dana.hide()
        self.jednostka_danych7.hide()

    def _update_conversion_method(self):
        if self.wybor_konwersji.currentIndex() == 0:
            self._hide_buttons()
            self.dana1.setText('λ =')
            self.jednostka_danych1.setText('m')
        elif self.wybor_konwersji.currentIndex() == 1:
            self._hide_buttons()
            self.dana1.setText('f =')
            self.jednostka_danych1.setText('kHz')
        elif self.wybor_konwersji.currentIndex() == 2:
            self._hide_buttons()
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana3.show()
            self.trzecia_dana.show()
            self.jednostka_danych3.show()
            self.dana1.setText('P =')
            self.dana2.setText('L =')
            self.dana3.setText('G =')
            self.jednostka_danych1.setText('dBm')
            self.jednostka_danych2.setText('dB')
            self.jednostka_danych3.setText('dBi')
        elif self.wybor_konwersji.currentIndex() == 3:
            self._hide_buttons()
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana1.setText('d =')
            self.dana2.setText('f =')
            self.jednostka_danych1.setText('km')
            self.jednostka_danych2.setText('GHz')
        elif self.wybor_konwersji.currentIndex() == 4:
            self._hide_buttons()
            self.dana1.setText('f =')
            self.jednostka_danych1.setText('kHz')
        elif self.wybor_konwersji.currentIndex() == 5:
            self._hide_buttons()
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana1.setText('λ =')
            self.dana2.setText('G =')
            self.jednostka_danych1.setText('km')
            self.jednostka_danych2.setText('dBi')
        elif self.wybor_konwersji.currentIndex() == 6:
            self._hide_buttons()
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana1.setText('e =')
            self.dana2.setText('u =')
            self.jednostka_danych1.setText('')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 7:
            self._hide_buttons()
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana1.setText('e =')
            self.dana2.setText('u =')
            self.jednostka_danych1.setText('')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 8:
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana3.show()
            self.trzecia_dana.show()
            self.jednostka_danych3.show()
            self.dana4.show()
            self.czwarta_dana.show()
            self.jednostka_danych4.show()
            self.dana5.show()
            self.piata_dana.show()
            self.jednostka_danych5.show()
            self.dana6.show()
            self.szosta_dana.show()
            self.jednostka_danych6.show()
            self.dana7.show()
            self.siodma_dana.show()
            self.jednostka_danych7.show()
            self.dana1.setText('Ptx =')
            self.dana2.setText('LTx =')
            self.dana3.setText('LRx =')
            self.dana4.setText('LFS =')
            self.dana5.setText('LM =')
            self.dana6.setText('GTx =')
            self.dana7.setText('GRx =')
            self.jednostka_danych1.setText('dB')
            self.jednostka_danych2.setText('dB')
            self.jednostka_danych3.setText('dB')
            self.jednostka_danych4.setText('dB')
            self.jednostka_danych5.setText('dB')
            self.jednostka_danych6.setText('dB')
            self.jednostka_danych7.setText('dB')
        elif self.wybor_konwersji.currentIndex() == 9:
            self._hide_buttons()
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana3.show()
            self.trzecia_dana.show()
            self.jednostka_danych3.show()
            self.dana1.setText('E =')
            self.dana2.setText('m =')
            self.dana3.setText('c =')
            self.jednostka_danych1.setText('V/m')
            self.jednostka_danych2.setText('Kg/m^3')
            self.jednostka_danych3.setText('S/m')
        elif self.wybor_konwersji.currentIndex() == 10:
            self._hide_buttons()
            self.dana1.setText('valency =')
            self.jednostka_danych1.setText('')
        elif self.wybor_konwersji.currentIndex() == 11:
            self._hide_buttons()
            self.dana2.show()
            self.druga_dana.show()
            self.jednostka_danych2.show()
            self.dana1.setText('V =')
            self.dana2.setText('n =')
            self.jednostka_danych1.setText('Bd')
            self.jednostka_danych2.setText('')

    def go_to_clear_data(self):
        self.wynik.setText('')
        self.jednostka_wyniku.setText('')
        self.pierwsza_dana.setValue(0)
        self.druga_dana.setValue(0)
        self.trzecia_dana.setValue(0)
        self.czwarta_dana.setValue(0)
        self.piata_dana.setValue(0)
        self.szosta_dana.setValue(0)
        self.siodma_dana.setValue(0)

    def _choose_mode(self):
        if self.wybor_konwersji.currentIndex() == 0:
            return modules.radio.waveToFreq(self.first_value), "kHz"
        elif self.wybor_konwersji.currentIndex() == 1:
            return modules.radio.freqToWave(self.first_value), "m"
        elif self.wybor_konwersji.currentIndex() == 2:
            return modules.radio.eirp(self.first_value, self.second_value, self.third_value), ""
        elif self.wybor_konwersji.currentIndex() == 3:
            return modules.radio.fresnel(self.first_value, self.second_value), "m"
        elif self.wybor_konwersji.currentIndex() == 4:
            return modules.radio.dipoleLength(self.first_value), "km"
        elif self.wybor_konwersji.currentIndex() == 5:
            return modules.radio.effectiveAperture(self.first_value, self.second_value), "m^2"
        elif self.wybor_konwersji.currentIndex() == 6:
            return modules.radio.plainWaveVelocity(self.first_value, self.second_value), "m/s"
        elif self.wybor_konwersji.currentIndex() == 7:
            return modules.radio.plainWaveImpedance(self.first_value, self.second_value), "Ω"
        elif self.wybor_konwersji.currentIndex() == 8:
            return modules.radio.powerBudget(self.first_value, self.second_value, self.third_value, self.fourth_value, self.fifth_value, self.sixth_value, self.seventh_value), "dB"
        elif self.wybor_konwersji.currentIndex() == 9:
            return modules.radio.SAR(self.first_value, self.second_value, self.third_value), ""
        elif self.wybor_konwersji.currentIndex() == 10:
            return modules.radio.bitsQAM(self.first_value), ""
        elif self.wybor_konwersji.currentIndex() == 11:
            return modules.radio.bitrate(self.first_value, self.second_value), ""

    def go_to_save_data(self):
        try:
            self.first_value = self.pierwsza_dana.value()
            self.second_value = self.druga_dana.value()
            self.third_value = self.trzecia_dana.value()
            self.fourth_value = self.czwarta_dana.value()
            self.fifth_value = self.piata_dana.value()
            self.sixth_value = self.szosta_dana.value()
            self.seventh_value = self.siodma_dana.value()
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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()


class McCluskey(QDialog):

    def __init__(self):
        super(McCluskey, self).__init__()
        loadUi("UI/mccluskey.ui", self)
        self.oblicz_button.clicked.connect(self.go_to_save_data)
        self.oblicz_button_2.clicked.connect(self.go_to_save_data2)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.reset_button_2.clicked.connect(self.go_to_clear_data2)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.ilosc_zmiennych.currentIndexChanged.connect(self._update_conversion_method)
        self._update_conversion_method()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

    def _set_two_variables(self):
        self.a60.setText("1")
        self.a61.setText("1")
        self.a62.setText("0")
        self.a63.setText("1")
        self.a64.setText("1")

    def _set_three_variables(self):
        self.zmienna3.setText("C")
        self.a51.setText("1")
        self.a60.setText("0")
        self.a62.setText("1")
        self.a53.setText("0")
        self.a61.setText("0")
        self.a55.setText("1")
        self.a64.setText("1")
        self.a63.setText("0")
        self.a1.setText("1")
        self.a2.setText("0")
        self.a6.setText("0")
        self.a7.setText("1")
        self.a5.setText("1")
        self.a10.setText("1")
        self.a11.setText("0")
        self.a9.setText("1")
        self.a13.setText("1")

    def _set_four_variables(self):
        self.zmienna3.setText("C")
        self.zmienna4.setText("D")
        self.a51.setText("0")
        self.a60.setText("0")
        self.a62.setText("0")
        self.a53.setText("1")
        self.a61.setText("0")
        self.a55.setText("1")
        self.a64.setText("0")
        self.a63.setText("0")
        self.a1.setText("0")
        self.a2.setText("1")
        self.a6.setText("1")
        self.a7.setText("0")
        self.a5.setText("0")
        self.a10.setText("1")
        self.a11.setText("1")
        self.a9.setText("0")
        self.a13.setText("0")

    def _hide_labels(self):
        self.line_4.hide()
        self.line_5.hide()
        self.line_10.hide()
        self.line_11.hide()
        self.line_12.hide()
        self.line_13.hide()
        self.line_14.hide()
        self.line_15.hide()
        self.line_16.hide()
        self.line_17.hide()
        self.line_18.hide()
        self.line_19.hide()
        self.line_20.hide()
        self.line_21.hide()
        self.l4.hide()
        self.l5.hide()
        self.l6.hide()
        self.l7.hide()
        self.l8.hide()
        self.l9.hide()
        self.l10.hide()
        self.l11.hide()
        self.l12.hide()
        self.l13.hide()
        self.l14.hide()
        self.l15.hide()
        self.a1.hide()
        self.a2.hide()
        self.a3.hide()
        self.a4.hide()
        self.a5.hide()
        self.a6.hide()
        self.a7.hide()
        self.a8.hide()
        self.a9.hide()
        self.a10.hide()
        self.a11.hide()
        self.a12.hide()
        self.a13.hide()
        self.a14.hide()
        self.a15.hide()
        self.a16.hide()
        self.a17.hide()
        self.a18.hide()
        self.a19.hide()
        self.a20.hide()
        self.a21.hide()
        self.a22.hide()
        self.a23.hide()
        self.a24.hide()
        self.a25.hide()
        self.a26.hide()
        self.a27.hide()
        self.a28.hide()
        self.a29.hide()
        self.a30.hide()
        self.a31.hide()
        self.a32.hide()
        self.a33.hide()
        self.a34.hide()
        self.a35.hide()
        self.a36.hide()
        self.a37.hide()
        self.a38.hide()
        self.a39.hide()
        self.a40.hide()
        self.a41.hide()
        self.a42.hide()
        self.a43.hide()
        self.a44.hide()
        self.a45.hide()
        self.a46.hide()
        self.a47.hide()
        self.a48.hide()
        self.a49.hide()
        self.a50.hide()
        self.a51.hide()
        self.a52.hide()
        self.a53.hide()
        self.a54.hide()
        self.a55.hide()
        self.a56.hide()
        self.zmienna4.hide()
        self.zmienna3.hide()

    def _show_labels(self):
        self.line_4.show()
        self.line_5.show()
        self.line_10.show()
        self.line_11.show()
        self.line_12.show()
        self.line_13.show()
        self.line_14.show()
        self.line_15.show()
        self.line_16.show()
        self.line_17.show()
        self.line_18.show()
        self.line_19.show()
        self.line_20.show()
        self.line_21.show()
        self.l4.show()
        self.l5.show()
        self.l6.show()
        self.l7.show()
        self.l8.show()
        self.l9.show()
        self.l10.show()
        self.l11.show()
        self.l12.show()
        self.l13.show()
        self.l14.show()
        self.l15.show()
        self.a1.show()
        self.a2.show()
        self.a3.show()
        self.a4.show()
        self.a5.show()
        self.a6.show()
        self.a7.show()
        self.a8.show()
        self.a9.show()
        self.a10.show()
        self.a11.show()
        self.a12.show()
        self.a13.show()
        self.a14.show()
        self.a15.show()
        self.a16.show()
        self.a17.show()
        self.a18.show()
        self.a19.show()
        self.a20.show()
        self.a21.show()
        self.a22.show()
        self.a23.show()
        self.a24.show()
        self.a25.show()
        self.a26.show()
        self.a27.show()
        self.a28.show()
        self.a29.show()
        self.a30.show()
        self.a31.show()
        self.a32.show()
        self.a33.show()
        self.a34.show()
        self.a35.show()
        self.a36.show()
        self.a37.show()
        self.a38.show()
        self.a39.show()
        self.a40.show()
        self.a41.show()
        self.a42.show()
        self.a43.show()
        self.a44.show()
        self.a45.show()
        self.a46.show()
        self.a47.show()
        self.a48.show()
        self.a49.show()
        self.a50.show()
        self.a51.show()
        self.a52.show()
        self.a53.show()
        self.a54.show()
        self.a55.show()
        self.a56.show()
        self.zmienna3.show()
        self.zmienna4.show()
        self.zmienna5.show()

    def _update_conversion_method(self):
        if self.ilosc_zmiennych.currentIndex() == 0:
            self.go_to_clear_data2()
            self._hide_labels()
            self._set_two_variables()
        elif self.ilosc_zmiennych.currentIndex() == 1:
            self.go_to_clear_data2()
            self._hide_labels()
            self.line_4.show()
            self.line_10.show()
            self.line_11.show()
            self.line_12.show()
            self.line_13.show()
            self.l4.show()
            self.l5.show()
            self.l6.show()
            self.l7.show()
            self.a1.show()
            self.a2.show()
            self.a3.show()
            self.a5.show()
            self.a6.show()
            self.a7.show()
            self.a9.show()
            self.a10.show()
            self.a11.show()
            self.a13.show()
            self.a14.show()
            self.a15.show()
            self.a49.show()
            self.a51.show()
            self.a53.show()
            self.a55.show()
            self.zmienna3.show()
            self._set_three_variables()

        elif self.ilosc_zmiennych.currentIndex() == 2:
            self.go_to_clear_data2()
            self._show_labels()
            self._set_four_variables()


    def go_to_clear_data(self):
        self.karnough0.setCurrentIndex(0)
        self.karnough1.setCurrentIndex(0)
        self.karnough2.setCurrentIndex(0)
        self.karnough3.setCurrentIndex(0)
        self.karnough4.setCurrentIndex(0)
        self.karnough5.setCurrentIndex(0)
        self.karnough6.setCurrentIndex(0)
        self.karnough7.setCurrentIndex(0)
        self.karnough8.setCurrentIndex(0)
        self.karnough9.setCurrentIndex(0)
        self.karnough10.setCurrentIndex(0)
        self.karnough11.setCurrentIndex(0)
        self.karnough12.setCurrentIndex(0)
        self.karnough13.setCurrentIndex(0)
        self.karnough14.setCurrentIndex(0)
        self.karnough15.setCurrentIndex(0)
        self.wynik.setText("")

    def go_to_clear_data2(self):
        self.x0.setText("")
        self.x1.setText("")
        self.x2.setText("")
        self.x3.setText("")
        self.x4.setText("")
        self.x5.setText("")
        self.x6.setText("")
        self.x7.setText("")
        self.x8.setText("")
        self.x9.setText("")
        self.x10.setText("")
        self.x11.setText("")
        self.x12.setText("")
        self.x13.setText("")
        self.x14.setText("")
        self.x15.setText("")

    def go_to_save_data(self):
        karnough = []
        karnough.append( self.karnough0.currentIndex() )
        karnough.append( self.karnough1.currentIndex() )
        karnough.append( self.karnough2.currentIndex() )
        karnough.append( self.karnough3.currentIndex() )
        karnough.append( self.karnough4.currentIndex() )
        karnough.append( self.karnough5.currentIndex() )
        karnough.append( self.karnough6.currentIndex() )
        karnough.append( self.karnough7.currentIndex() )
        karnough.append( self.karnough8.currentIndex() )
        karnough.append( self.karnough9.currentIndex() )
        karnough.append( self.karnough10.currentIndex() )
        karnough.append( self.karnough11.currentIndex() )
        karnough.append( self.karnough12.currentIndex() )
        karnough.append( self.karnough13.currentIndex() )
        karnough.append( self.karnough14.currentIndex() )
        karnough.append( self.karnough15.currentIndex() )
        print(karnough)

        minterns = []
        dontcares = []
        for i in range(0, 15):
            if(karnough[i] == 1): minterns.append(i)
            if(karnough[i] == 2): dontcares.append(i)
        if(minterns.__len__() == 0 and dontcares.__len__() == 0): result = "F = 0"
        else: result = modules.mccluskey.exec(minterns, dontcares)
        print(result)
        self.wynik.setText(result)

    def go_to_save_data2(self):
        input_data = self.funkcja_Tekst.text()
        try:
            array = modules.boolean.truthTable(input_data, self.ilosc_zmiennych.currentIndex() + 2)
            if self.ilosc_zmiennych.currentIndex() == 0:
                self.x0.setText(str(array[0]))
                self.x1.setText(str(array[1]))
                self.x2.setText(str(array[2]))
                self.x3.setText(str(array[3]))
            if self.ilosc_zmiennych.currentIndex() == 1:
                self.x0.setText(str(array[0]))
                self.x1.setText(str(array[1]))
                self.x2.setText(str(array[2]))
                self.x3.setText(str(array[3]))
                self.x4.setText(str(array[4]))
                self.x5.setText(str(array[5]))
                self.x6.setText(str(array[6]))
                self.x7.setText(str(array[7]))
            if self.ilosc_zmiennych.currentIndex() == 2:
                self.x0.setText(str(array[0]))
                self.x1.setText(str(array[1]))
                self.x2.setText(str(array[2]))
                self.x3.setText(str(array[3]))
                self.x4.setText(str(array[4]))
                self.x5.setText(str(array[5]))
                self.x6.setText(str(array[6]))
                self.x7.setText(str(array[7]))
                self.x8.setText(str(array[8]))
                self.x9.setText(str(array[9]))
                self.x10.setText(str(array[10]))
                self.x11.setText(str(array[11]))
                self.x12.setText(str(array[12]))
                self.x13.setText(str(array[13]))
                self.x14.setText(str(array[14]))
                self.x15.setText(str(array[15]))
        except:
            dlg = ErrorDialog("Błąd danych")
            if dlg.exec(): print("Error dialog prompted")
    
    def cofanie(self):
        cofanie_przycisk = Menu()
        widget.addWidget(cofanie_przycisk)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Fiber(QDialog):

    def __init__(self):
        super(Fiber, self).__init__()
        loadUi("UI/Fiber.ui", self)
        self.commandLinkButton.clicked.connect(self.cofanie)
        self.reset_button.clicked.connect(self.go_to_clear_data)
        self.oblicz_button.clicked.connect(self.go_to_save_data)
        self.wybor_konwersji.currentIndexChanged.connect(self._update_conversion_method)

        self.first_value = self.pierwsza_dana.value()
        self.second_value = self.druga_dana.value()
        self.third_value = self.trzecia_dana.value()

        self.dana1.setText('n0 =')
        self.jednostka_danych1.setText('')
        self.dana2.setText('n1 =')
        self.jednostka_danych2.setText('')
        self.dana3.setText('n2 =')
        self.jednostka_danych3.setText('')

    def _show_buttons(self):

        self.dana2.show()
        self.druga_dana.show()
        self.jednostka_danych2.show()
        self.dana3.show()
        self.trzecia_dana.show()
        self.jednostka_danych3.show()

    def _update_conversion_method(self):
        if self.wybor_konwersji.currentIndex() == 0:
            self._show_buttons()
            self.dana1.setText('n0 =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('n1 =')
            self.jednostka_danych2.setText('')
            self.dana3.setText('n2 =')
            self.jednostka_danych3.setText('')
        elif self.wybor_konwersji.currentIndex() == 1:
            self._show_buttons()
            self.dana1.setText('NA =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('n =')
            self.jednostka_danych2.setText('')
            self.dana3.setText('L =')
            self.jednostka_danych3.setText('km')
        elif self.wybor_konwersji.currentIndex() == 2:
            self._show_buttons()
            self.dana1.setText('a =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('λ =')
            self.jednostka_danych2.setText('')
            self.dana3.setText('NA =')
            self.jednostka_danych3.setText('')
        elif self.wybor_konwersji.currentIndex() == 3:
            self._show_buttons()
            self.dana3.hide()
            self.trzecia_dana.hide()
            self.jednostka_danych3.hide()
            self.dana1.setText('P0 =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('P1 =')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 4:
            self._show_buttons()
            self.dana3.hide()
            self.trzecia_dana.hide()
            self.jednostka_danych3.hide()
            self.dana1.setText('Pr =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('Pi =')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 5:
            self._show_buttons()
            self.dana3.hide()
            self.trzecia_dana.hide()
            self.jednostka_danych3.hide()
            self.dana1.setText('D1 =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('D2 =')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 6:
            self._show_buttons()
            self.dana3.hide()
            self.trzecia_dana.hide()
            self.jednostka_danych3.hide()
            self.dana1.setText('NA1 =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('NA2 =')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 7:
            self._show_buttons()
            self.dana3.hide()
            self.trzecia_dana.hide()
            self.jednostka_danych3.hide()
            self.dana1.setText('g1 =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('g2 =')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 8:
            self._show_buttons()
            self.dana1.setText('R =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('x =')
            self.jednostka_danych2.setText('')
            self.dana3.setText('a =')
            self.jednostka_danych3.setText('')
        elif self.wybor_konwersji.currentIndex() == 9:
            self._show_buttons()
            self.dana3.hide()
            self.trzecia_dana.hide()
            self.jednostka_danych3.hide()
            self.dana1.setText('R =')
            self.jednostka_danych1.setText('')
            self.dana2.setText('y =')
            self.jednostka_danych2.setText('')
        elif self.wybor_konwersji.currentIndex() == 10:
            self._show_buttons()
            self.dana2.hide()
            self.druga_dana.hide()
            self.jednostka_danych2.hide()
            self.dana3.hide()
            self.trzecia_dana.hide()
            self.jednostka_danych3.hide()
            self.dana1.setText('R =')
            self.jednostka_danych1.setText('')

    def go_to_clear_data(self):
        self.wynik.setText('')
        self.jednostka_wyniku.setText('')
        self.pierwsza_dana.setValue(0)
        self.druga_dana.setValue(0)
        self.trzecia_dana.setValue(0)

    def _choose_mode(self):
        if self.wybor_konwersji.currentIndex() == 0:
            return modules.fiber.numericAperture(self.first_value, self.second_value, self.third_value), ""
        elif self.wybor_konwersji.currentIndex() == 1:
            return modules.fiber.opticalBandwidth(self.first_value, self.second_value, self.third_value), ""
        elif self.wybor_konwersji.currentIndex() == 2:
            return modules.fiber.modLatency(self.first_value, self.second_value, self.third_value), ""
        elif self.wybor_konwersji.currentIndex() == 3:
            return modules.fiber.insertionLoss(self.first_value, self.second_value), ""
        elif self.wybor_konwersji.currentIndex() == 4:
            return modules.fiber.reflectionLoss(self.first_value, self.second_value), ""
        elif self.wybor_konwersji.currentIndex() == 5:
            return modules.fiber.diameterLoss(self.first_value, self.second_value), ""
        elif self.wybor_konwersji.currentIndex() == 6:
            return modules.fiber.NALoss(self.first_value, self.second_value), ""
        elif self.wybor_konwersji.currentIndex() == 7:
            return modules.fiber.profileLoss(self.first_value, self.second_value), ""
        elif self.wybor_konwersji.currentIndex() == 8:
            return modules.fiber.axisShift(self.first_value, self.second_value, self.third_value), ""
        elif self.wybor_konwersji.currentIndex() == 9:
            return modules.fiber.radialShift(self.first_value, self.second_value), ""
        elif self.wybor_konwersji.currentIndex() == 10:
            return modules.fiber.fresnelReflection(self.first_value), ""

    def go_to_save_data(self):
        try:
            self.first_value = self.pierwsza_dana.value()
            self.second_value = self.druga_dana.value()
            self.third_value = self.trzecia_dana.value()
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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
         app.quit()

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
