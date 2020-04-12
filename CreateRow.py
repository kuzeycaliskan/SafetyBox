from PyQt5.QtWidgets import *
import Code_Generator
import main_DB
import Mail
from pathlib import Path

class CreateRow(QWidget):  # <===
    Code_Generator = Code_Generator.Code_Generator()

    def __init__(self):
        super().__init__()
        # self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Yeni Kişi Oluştur")
        self.database = main_DB.main_DB()

        self.createrow()
        self.show()

    def createrow(self):
        # Widgets
        self.name = QLineEdit()
        self.name.setPlaceholderText("Adınızı yazınız")
        self.surname = QLineEdit()
        self.surname.setPlaceholderText("Soyadınızı yazınız")
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Telefon numaranızı yazınız")
        self.email = QLineEdit()
        self.email.setPlaceholderText("Mailinizi yazınız")
        self.securtiyLabel = QLabel("Ek güvenlik istiyor musunuz?")
        self.security = QCheckBox()
        security_FormL = QFormLayout()
        security_FormL.addRow(self.securtiyLabel, self.security)

        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)

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

        vbox.addWidget(self.name)
        vbox.addWidget(self.surname)
        vbox.addWidget(self.phone)
        vbox.addWidget(self.email)
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
            self.box_no = self.findEmptyBox(value[0])

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

    def confirmFunction(self):  # run function when confirmbutton clicked
        self.checkIdenties()  # Checking if ID is registered
        name = self.name.text().upper()
        surname = self.surname.text().upper()
        phone = self.phone.text()
        email = self.email.text()

        receiver_Person_ID = email.split("@")

        if self.security.isChecked() is True:
            security = 1
        else:
            security = 0

        safetybox = self.CB_SafetyBoxs.currentText()
        county = self.CB_Counties.currentText()
        city = self.CB_Cities.currentText()
        identities_ID = self.database.getIdentity_ID(phone)

        PNR, Tracking, QRCode, datetime = self.Code_Generator.create_QRCode(surname, name, county, city)

        self.database.create_Cargo(Tracking, QRCode, PNR, security, self.box_no, identities_ID, datetime, 0)
        self.database.setBoxState_isEmpty("0", str(self.box_no))
        self.getSafetyName()

        SB_Split = self.CB_SafetyBoxs.currentText().split(" - ")

        value = [name, surname, "", email.lower(), Tracking, PNR, SB_Split[0], SB_Split[1], county, city]
        Mail.SendMail("Creating_Cargo", value)

        Path("receiver_Person/" + receiver_Person_ID[0]).mkdir(parents=True,
                                                               exist_ok=True)  # create folder if not exist

    def checkIdenties(self):  # Checking if ID is registered
        name = self.name.text().upper()
        surname = self.surname.text().upper()
        phone = self.phone.text()
        email = self.email.text()

        for identity in self.database.getIdentities():
            if (str(phone) == str(identity[3])) or (str(email) == str(identity[4])):  # returning if ID found
                return

        self.database.create_Identity(name, surname, phone, email)
        return

    def findEmptyBox(self, text):
        available_box = self.database.getBoxs_WhichAvailable_WithSize(text, "M")
        if len(available_box) > 0:
            self.emptyBoxCount.setText("Seçtiğiniz SafetyBox'ta Boş Kutu Sayısı: " + str(len(available_box)))
            self.emptyBoxCount.setStyleSheet('font-weight: bold; color: green')
        else:
            self.emptyBoxCount.setText("Seçtiğiniz SafetyBox'ta Boş Kutu Sayısı: " + str(len(available_box)))
            self.emptyBoxCount.setStyleSheet('font-weight: bold; color: red')
        if not available_box:
            print("Boş kutu kalmamıştır")
            return

        return available_box[0][0]
