from PyQt5.QtWidgets import *
import Code_Generator
import Database
import Mail
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.Qt import *

class CreateRow(QWidget):  # <===
    Code_Generator = Code_Generator.Code_Generator()

    def __init__(self):
        super().__init__()
        # self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Yeni Kişi Oluştur")
        self.database = Database.main_DB()

        self.createrow()

    def createrow(self):
        # Widgets
        name = QLineEdit()
        name.setPlaceholderText("Adınızı yazınız")
        surname = QLineEdit()
        surname.setPlaceholderText("Soyadınızı yazınız")
        phone = QLineEdit()
        phone.setPlaceholderText("Telefon numaranızı yazınız")
        email = QLineEdit()
        email.setPlaceholderText("Mailinizi yazınız")
        self.securtiyLabel = QLabel("Ek güvenlik istiyor musunuz?")
        self.security = QCheckBox()
        security_FormL = QFormLayout()
        security_FormL.addRow(self.securtiyLabel, self.security)

        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(lambda: self.confirmFunction(name.text(), surname.text(), phone.text(), email.text()))

        self.CB_Cities = QComboBox()
        self.CB_Counties = QComboBox()
        self.CB_SafetyBoxs = QComboBox()
        self.emptyBoxCount = QLabel()
        # Widgets definition end

        for city in self.database.getCounties():
            if self.CB_Cities.findText(city[2]) == -1:
                self.CB_Cities.addItem(str(city[2]))
        self.setCounties()
        self.setSafetyBoxs()
        self.getSafetyName()

        self.CB_Cities.currentIndexChanged.connect(self.setCounties)
        self.CB_Counties.currentIndexChanged.connect(self.setSafetyBoxs)
        self.CB_SafetyBoxs.currentIndexChanged.connect(self.getSafetyName)

        vbox = QVBoxLayout()
        vbox.addWidget(name)
        vbox.addWidget(surname)
        vbox.addWidget(phone)
        vbox.addWidget(email)
        vbox.addLayout(security_FormL)
        vbox.addWidget(self.CB_Cities)
        vbox.addWidget(self.CB_Counties)
        vbox.addWidget(self.CB_SafetyBoxs)
        vbox.addWidget(self.emptyBoxCount)
        vbox.addWidget(confirmbutton)
        self.setLayout(vbox)

    def getSafetyName(self):
        value = self.CB_SafetyBoxs.currentText()
        value = value.split(" - ")
        if not value[0]:
            pass
        else:
            if not self.findEmptyBox(value[0]):
                self.box_no = "0"
                print("dolapların tamamı dolu")
            else:
                self.box_no = self.findEmptyBox(value[0])[0][0]

    def setCounties(self):  # set county's combobox widget
        self.CB_Counties.clear()
        for county in self.database.getCounties_withCities(self.CB_Cities.currentText()):
            if self.CB_Counties.findText(county[0]) == -1:
                self.CB_Counties.addItem(county[0])

    def setSafetyBoxs(self):  # set safetybox's combobox widget
        self.CB_SafetyBoxs.clear()
        for safetybox in self.database.getSafetyBoxs_withCounties(self.CB_Counties.currentText()):
            item = safetybox[0] + " - " + safetybox[1]
            self.CB_SafetyBoxs.addItem(item)

    def confirmFunction(self, name, surname, phone, email):  # run function when confirmbutton clicked
        self.checkIdenties(name, surname, phone, email)  # Checking if ID is registered
        name = name.upper()
        surname = surname.upper()

        receiver_Person_ID = email.split("@")

        if self.security.isChecked() is True:
            security = 1
        else:
            security = 0

        safetybox = self.CB_SafetyBoxs.currentText()
        county = self.CB_Counties.currentText()
        city = self.CB_Cities.currentText()
        identities_ID = self.database.getIdentity_withPhone(phone)


        if self.box_no == "0":
            info_dialog = QtWidgets.QMessageBox(self)
            info_dialog.setIcon(QMessageBox.Warning)
            info_dialog.setWindowIcon(QIcon('/home/pi/Desktop/SafetyBox/icons/info.png'))
            info_dialog.setWindowTitle("Uyarı")
            info_dialog.setText("Maalesef seçtiğiniz boyuttaki \ndolaplarımız doludur")
            button = QPushButton("Tamam", self)
            info_dialog.addButton(button, QMessageBox.RejectRole)
            info_dialog.show()

        else:
            PNR, Tracking, QRCode, datetime = self.Code_Generator.Generate_AllCodes("R", surname, name, county, city)

            self.database.create_Cargo(Tracking, QRCode, PNR, security, self.box_no, identities_ID[0][0], datetime, 0)
            self.database.setBoxState_isEmpty("0", str(self.box_no))
            self.getSafetyName()

            SB_Split = self.CB_SafetyBoxs.currentText().split(" - ")

            value = [name, surname, "", email.lower(), Tracking, PNR, SB_Split[0], SB_Split[1], county, city]
            Mail.SendMail("Creating_Cargo", value)

            Path("/home/pi/Desktop/receiver_Person/" + receiver_Person_ID[0]).mkdir(parents=True,
                                                                   exist_ok=True)  # create folder if not exist

    def checkIdenties(self, name, surname, phone, email):  # Checking if ID is registered
        name = name.upper()
        surname = surname.upper()

        for identity in self.database.getIdentities():
            if (str(phone) == str(identity[3])) or (str(email) == str(identity[4])):  # returning if ID found
                return True
        person_code = int(self.database.getLastPersonCode_Identities()) + 1
        self.database.create_Identity(name, surname, phone, email, person_code)
        return False

    def findEmptyBox(self, text, size="M"):
        available_box = self.database.getBoxs_WhichAvailable_WithSize(text, size)

        if not available_box:
            print("Boş kutu kalmamıştır")

        if len(available_box) > 0:
            self.emptyBoxCount.setText("Seçtiğiniz SafetyBox'ta Boş Kutu Sayısı: " + str(len(available_box)))
            self.emptyBoxCount.setStyleSheet('font-weight: bold; color: green')
        else:
            self.emptyBoxCount.setText("Seçtiğiniz SafetyBox'ta Boş Kutu Sayısı: " + str(len(available_box)))
            self.emptyBoxCount.setStyleSheet('font-weight: bold; color: red')

        return available_box
