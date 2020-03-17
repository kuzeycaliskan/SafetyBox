from PyQt5.QtWidgets import *
import Code_Generator
import main_DB


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
        # Widgets definition end

        for city in self.database.getCounties():
            if self.CB_Cities.findText(city[2]) == -1:
                self.CB_Cities.addItem(str(city[2]))
        self.setCounties()
        self.setSafetyBoxs()

        self.CB_Cities.currentIndexChanged.connect(self.setCounties)
        self.CB_Counties.currentIndexChanged.connect(self.setSafetyBoxs)

        vbox = QVBoxLayout()
        vbox.addWidget(self.name)
        vbox.addWidget(self.surname)
        vbox.addWidget(self.phone)
        vbox.addWidget(self.email)
        vbox.addLayout(security_FormL)
        vbox.addWidget(self.CB_Cities)
        vbox.addWidget(self.CB_Counties)
        vbox.addWidget(self.CB_SafetyBoxs)
        vbox.addWidget(confirmbutton)
        self.setLayout(vbox)

    def setCounties(self):
        self.CB_Counties.clear()
        for county in self.database.getCounties_withCities(self.CB_Cities.currentText()):
            if self.CB_Counties.findText(county[0]) == -1:
                self.CB_Counties.addItem(county[0])

    def setSafetyBoxs(self):
        self.CB_SafetyBoxs.clear()
        for safetybox in self.database.getSafetyBoxs_withCounties(self.CB_Counties.currentText()):
            item = safetybox[0] + "-" + safetybox[1]
            self.CB_SafetyBoxs.addItem(item)

    def confirmFunction(self):
        print("111111")
        self.checkIdenties()
        print("222222")
        name = self.name.text().upper()
        surname = self.surname.text().upper()
        phone = self.phone.text()
        email = self.email.text()
        security = 0
        if self.security.isChecked() is True:
            security = 1
        else:
            security = 0

        safetybox = self.CB_SafetyBoxs.currentText()
        county = self.CB_Counties.currentText()
        city = self.CB_Cities.currentText()
        print("333333")
        identities_ID = self.database.getIdentity_ID(phone)
        print("444444")

        PNR, Tracking, QRCode, datetime = self.Code_Generator.create_QRCode(surname, name, county, city)
        print(QRCode)
        print(security)
        print(datetime)

        print("555555")
        self.database.create_Cargo(Tracking, QRCode, PNR, security, 25, identities_ID, datetime, datetime, 0)
        print("666666")

    def checkIdenties(self):
        name = self.name.text().upper()
        surname = self.surname.text().upper()
        phone = self.phone.text()
        email = self.email.text()

        for identity in self.database.getIdentities():
            if (str(phone) == str(identity[3])) or (str(email) == str(identity[4])):
                return

        self.database.create_Identity(name, surname, phone, email)
        return
