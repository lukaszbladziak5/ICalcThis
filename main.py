from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import sys
import sql
import modules.hata
import modules.dB
import modules.friis
import modules.circuits
import modules.radio
import modules.fiber


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
        self.obwodyElektryczne_przycisk.clicked.connect(self.obwody_elektryczne)
        self.operacja4_ONP.clicked.connect(self.ONP)
        self.rownanie_friisa_przycisk.clicked.connect(self.rownanie_friisa)
        self.radio_przycisk.clicked.connect(self.radio)
        self.fiber_przycisk.clicked.connect(self.fiber)

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

# Zrobione:

# circuits.py
# dB.py
# friis.py
# hata.py

# Do zrobienia:

# binary.py
# boolean.py
# fiber.py
# lineCodes.py
# mccluskey.py
# media.py
# plot.py
# radio.py
# rpn.py

