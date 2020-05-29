import datetime

import cv2
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.Qt import *
from pyzbar import pyzbar

import CreateRow
import Finder
import InfoWindow
import Mail
import Database_Window
import Database
import adminPassWindow
import Code_Generator

# GUI Button Shape
StyleSheet = '''  
QPushButton#DeliveringButton {
    background-color: #2FC4B2;
    border-radius: 48px;
    padding: 20px; 
}

QPushButton#DeliveringButton:hover {
    background-color: #80E9DC;
    color: #fff;
}

QPushButton#DeliveringButton:pressed {
    background-color: #A0F3E9;
}

QPushButton#ReceivingButton {
    background-color: #F17808;
    border-radius: 48px;
    padding: 20px; 
}

QPushButton#ReceivingButton:hover {
    background-color: #ECA664;
    color: #fff;
}

QPushButton#ReceivingButton:pressed {
    background-color: #ECBD90;
}

QPushButton#LockerButton {
    background-color: #68BA48;
    border-radius: 48px;
    padding: 20px; 
}

QPushButton#LockerButton:hover {
    background-color: #8FDC72;
    color: #fff;
}

QPushButton#LockerButton:pressed {
    background-color: #C1F3AE;
}

QPushButton#GeneralButton{
    background-color : #48E0FA;
    border-radius: 14px;
    font-size: 12pt;
    padding: 10px; 
}

QPushButton#GeneralButton:hover{
    background-color: #FFDBA0;
}

QPushButton#GeneralButton:pressed {
    background-color: #F9EDC7;
}

QPushButton#BackMainButton{
    background-color : #90D843;
    border-radius: 14px;
    font-size: 12pt;
    padding: 7px; 
}

QPushButton#BackMainButton:hover{
    background-color: #A3DC67;
}

QPushButton#BackMainButton:pressed {
    background-color: #BDE791;
}

QPushButton#SmallButton{
    background-color : #48E0FA;
    border-radius: 14px;
    font-size: 10pt;
}

QPushButton#SmallButton:hover{
    background-color: #FFDBA0;
}

QPushButton#SmallButton:pressed {
    background-color: #F9EDC7;
}

QPushButton#SettingsButton {
    qproperty-icon: url("home/pi/Desktop/SafetyBox/icons/setting.png"); 
    qproperty-iconSize: 35px 35px; 
    background-color: #FFF;
    border-radius: 48px;
}

QPushButton#SettingsButton:hover {
    background-color: #D3D3D3;
    color: #fff;
}

QPushButton#SettingsButton:pressed {
    background-color: #FFF;
}

QLineEdit#GeneralLineEdit {
    color: black; 
    background-color: #AEF3EE; 
    border-radius: 15px; 
    padding: 10px;

}

QLineEdit#LockerLineEdit {
    color: black; 
    background-color: #AEF3EE; 
    border-radius: 15px; 
    padding: 10px;
    margin-left: 30px;

}

QLabel#LockerLabels {
    font: 15pt "Arial";
    font-weight: bold;
    
}

QRadioButton { 
    font: 15pt Arial;
    font-weight: bold;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #96ABEC, stop: 1 #8395CC);
     border-radius: 15px;
     padding: 10px; 

} 

QRadioButton::indicator { 
    width: 10px; 
    height: 10px;    
}

'''


class Window(QWidget):
    Finder = Finder.Finder()
    Tr2Eng = str.maketrans("ÇĞİÖŞÜçğıöşü", "CGIOSUcgiosu")
    safetybox_name = "Üsküdar Vapur İskelesi"
    safetybox_address = "Mimar Sinan Cd. Cami Yanı"
    safetybox_county = "Üsküdar"
    safetybox_city = "İstanbul"

    def __init__(self):
        super().__init__()  # QWidget fonskiyonlarını kullanabilmek icin
        self.setGeometry(0, 0, 800, 640)  # window size
        self.setWindowTitle("Safety Box")  # window title
        background_Color = self.palette()
        background_Color.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(background_Color)

        self.database = Database.main_DB()  # calling database class

        self.tabs()  # initialize tabs
        self.show()

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)

        # messagebox opened, when no cargo is found
        self.info_dialog = QtWidgets.QMessageBox(self)
        self.info_dialog.setIcon(QMessageBox.Information)
        # self.info_dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)  # no title bar
        self.info_dialog.setWindowIcon(QIcon('/home/pi/Desktop/SafetyBox/icons/icon.png'))
        # self.info_dialog.setIconPixmap(QPixmap('icons/icon.png'))
        self.info_dialog.setWindowTitle("Uyarı")
        self.info_dialog.setText("Program Başlamıştır")
        self.button = QPushButton("Tamam", self)
        self.info_dialog.addButton(self.button, QMessageBox.RejectRole)
        self.info_dialog.show()

    def OpenSettingWindow(self):  # Menu Bar Database Güncelleme
        self.admin_W = adminPassWindow.adminPassWindow()
        self.admin_W.setCllback_Admin(self.cllback_AdminPass)
        self.admin_W.show()

    def cllback_AdminPass(self, result):
        if result is True:
            self.tab.addTab(self.tab5, "Ayarlar")
            self.tab.setCurrentWidget(self.tab5)
            self.settingButton.setVisible(False)
            self.admin_W.close()
        else:
            print("Giriş başarısız")

    def GB_cargoReceive(self):  # Kargo Teslim Alma - Step1

        groupBox = QGroupBox("Kargo Teslim Alma")

        vbox = QVBoxLayout()

        self.receivingButton = QPushButton("Kargo Teslim\nAlma", objectName="ReceivingButton")  # button initialize
        self.receivingButton.installEventFilter(self)
        # receivingButton.setFixedSize(receivingButton.width(), receivingButton.height())  # button size maximize
        self.receivingButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.receivingButton.setFont(QFont("Arial", 40, QFont.Bold))  # button font

        self.receivingButton.clicked.connect(self.B_receivingFunction)

        vbox.addWidget(self.receivingButton)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_cargoDelivery(self):  # Kargo Teslim Etme - Step1
        groupBox = QGroupBox("Kargo Teslim Etme")

        vbox = QVBoxLayout()
        self.deliveringButton = QPushButton("Kargo Teslim\nEtme", objectName="DeliveringButton")  # button initialize
        self.deliveringButton.installEventFilter(self)
        # deliveringButton.setFixedSize(deliveringButton.width(), deliveringButton.height())  # button size maximize
        self.deliveringButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.deliveringButton.setFont(QFont("Arial", 40, QFont.Bold))  # button font
        self.deliveringButton.clicked.connect(self.B_deliveringFunction)
        vbox.addWidget(self.deliveringButton)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_LockerSystem(self):  # Emanet Dolabı - Step1

        groupBox = QGroupBox("Emanet Dolabı")

        vbox = QVBoxLayout()

        self.lockerbutton = QPushButton("Emanet Dolabı", objectName="LockerButton")  # button initialize
        self.lockerbutton.installEventFilter(self)
        # receivingButton.setFixedSize(receivingButton.width(), receivingButton.height())  # button size maximize
        self.lockerbutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lockerbutton.setFont(QFont("Arial", 40, QFont.Bold))  # button font

        self.lockerbutton.clicked.connect(self.B_LockerFunction)

        vbox.addWidget(self.lockerbutton)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_cargoPNR(self):  # Kargo Teslim Grup Box - Step2

        self.infoWin = InfoWindow.InfoWindow()  # taking picture after pushing confirm at info window
        self.infoWin.setCllBack_TakePicture(self.cllback_TakePicture)

        self.CameraLabel_R = QLabel(self)
        # self.label.move(280, 120)
        self.CameraLabel_R.resize(640, 480)
        self.th = Thread(self)
        self.th.setCllback(self.cllback)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        groupBox = QGroupBox("Kargo Teslim")

        info_PNRDelivery = QLabel("Kargonuzu Teslim Almak İçin \nQR Kod Okutunuz veya PNR Girip Butona Basınız.")
        info_PNRDelivery.setFont(QFont("Arial", 18, QFont.Bold))
        info_PNRDelivery.setAlignment(Qt.AlignCenter)
        info_PNRDelivery.setMargin(20)

        self.PNRTextEditor = QLineEdit(objectName="GeneralLineEdit")
        self.PNRTextEditor.setPlaceholderText("PNR Kod Giriniz")
        self.PNRTextEditor.setValidator(QIntValidator())


        PNRbutton = QPushButton("Kargo Teslim Al", objectName="GeneralButton")

        # PNRbutton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        PNRbutton.installEventFilter(self)
        PNRbutton.setFont(QFont("Time New Roman", 25))
        PNRbutton.clicked.connect(self.PNRFinder)


        self.PNRText = QLabel("")  # success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addStretch()
        vbox.addWidget(self.PNRTextEditor, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.PNRText)
        vbox.addWidget(PNRbutton, alignment=QtCore.Qt.AlignCenter)
        vbox.addStretch()
        vbox.addWidget(self.CameraLabel_R, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)

        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_cargoTrack(self):  # Kargo teslim verme
        self.CameraLabel_D = QLabel(self)
        # self.label.move(280, 120)
        self.CameraLabel_D.resize(640, 480)

        groupBox = QGroupBox("Kargo Teslim Verme ")

        info_PNRDelivery = QLabel("Kargoyu Teslim Vermek İçin, \n Barkod Okutunuz veya Kodu Girip Butona Basınız")
        info_PNRDelivery.setFont(QFont("Arial", 18, QFont.Bold))
        info_PNRDelivery.setAlignment(Qt.AlignCenter)
        info_PNRDelivery.setMargin(20)

        self.TrackTextEditor = QLineEdit(self, objectName="GeneralLineEdit")
        self.TrackTextEditor.setPlaceholderText("Takip Numarasını Giriniz")
        self.TrackTextEditor.setValidator(QIntValidator())


        Trackbutton = QPushButton("Kargo Teslim Et", objectName="GeneralButton")
        Trackbutton.setFont(QFont("Time New Roman", 25))
        Trackbutton.clicked.connect(self.TrackingFinder)


        self.TrackText = QLabel("")  # success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addWidget(self.TrackTextEditor, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.TrackText)
        vbox.addWidget(Trackbutton, alignment=QtCore.Qt.AlignCenter)
        vbox.addStretch()
        vbox.addWidget(self.CameraLabel_D, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)
        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_Locker_ChoosingMenu(self):
        self.groupBox_Locker_ChoosingMenu = QGroupBox("Seçim Ekranı")

        hbox = QHBoxLayout()

        newIdentity = QPushButton("Yeni \nMüşteriyim", objectName="ReceivingButton")
        newIdentity.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        newIdentity.setFont(QFont("Arial", 40, QFont.Bold))  # button font

        oldIdentity = QPushButton("Müşterinizim", objectName="DeliveringButton")
        oldIdentity.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        oldIdentity.setFont(QFont("Arial", 40, QFont.Bold))  # button font

        hbox.addWidget(newIdentity)
        hbox.addWidget(oldIdentity)

        newIdentity.clicked.connect(self.Open_Locker_NewIdentity)
        oldIdentity.clicked.connect(self.Open_Locker_FindIdentity)
        self.groupBox_Locker_ChoosingMenu.setLayout(hbox)

        return self.groupBox_Locker_ChoosingMenu

    def Open_Locker_FindIdentity(self):
        self.groupBox_Locker_FindItentity.setVisible(True)
        self.groupBox_Locker_ChoosingMenu.setVisible(False)
        self.groupBox_Locker_NewIdentity.setVisible(False)

    def Open_Locker_NewIdentity(self):
        self.groupBox_Locker_NewIdentity.setVisible(True)
        self.groupBox_Locker_ChoosingMenu.setVisible(False)
        self.groupBox_Locker_FindItentity.setVisible(False)

    def GB_Locker_FindIdentity(self):
        self.groupBox_Locker_FindItentity = QGroupBox("Yeni Kişi Emanet Bırakma")
        self.groupBox_Locker_FindItentity.setVisible(False)

        vbox = QVBoxLayout()
        info = QLabel()
        info.setText("SafetyBox Kimlik Numaranızı Giriniz.\nve\nKutu Boyutu Seçiniz.")
        info.setAlignment(QtCore.Qt.AlignCenter)
        info.setFont(QFont("Arial", 18, QFont.Bold))
        info.setMargin(20)

        SB_ID_TextEditor = QLineEdit(objectName="GeneralLineEdit")
        SB_ID_TextEditor.setPlaceholderText("SafetyBox ID")
        SB_ID_TextEditor.setValidator(QIntValidator())


        Locker_Button_GetIdentity = QPushButton("Beni Bul", objectName="GeneralButton")
        Locker_Button_GetIdentity.clicked.connect(lambda: self.Locker_GetIdentity(SB_ID_TextEditor.text()))

        Label_Name = QLabel("Ad", objectName="LockerLabels")
        Label_Surname = QLabel("Soyad", objectName="LockerLabels")
        Label_Phone = QLabel("Telefon", objectName="LockerLabels")
        Label_Mail = QLabel("Mail", objectName="LockerLabels")

        self.LockerIdentity_Name = QLabel(objectName="LockerLabels")
        self.LockerIdentity_Surname = QLabel(objectName="LockerLabels")
        self.LockerIdentity_Phone = QLabel(objectName="LockerLabels")
        self.LockerIdentity_Mail = QLabel(objectName="LockerLabels")
        self.Locker_emptyBoxCount = QLabel()

        self.Locker_box_size = "M"
        self.Locker_SmallSize = QRadioButton("Küçük Boy", self)
        self.Locker_MediumSize = QRadioButton("Orta Boy", self)
        self.Locker_MediumSize.setChecked(True)
        self.Locker_BigSize = QRadioButton("Büyük Boy", self)

        self.Locker_SmallSize.clicked.connect(self.Locker_SearchEmptyBox)
        self.Locker_MediumSize.clicked.connect(self.Locker_SearchEmptyBox)
        self.Locker_BigSize.clicked.connect(self.Locker_SearchEmptyBox)
        self.Locker_SearchEmptyBox()


        hbox_LockerSizeButton = QHBoxLayout()
        hbox_LockerSizeButton.addStretch()
        hbox_LockerSizeButton.addWidget(self.Locker_SmallSize)
        hbox_LockerSizeButton.addWidget(self.Locker_MediumSize)
        hbox_LockerSizeButton.addWidget(self.Locker_BigSize)
        hbox_LockerSizeButton.addStretch()

        Locker_FormLayout = QFormLayout()
        Locker_FormLayout.addRow(Label_Name,  self.LockerIdentity_Name)
        Locker_FormLayout.addRow(Label_Surname, self.LockerIdentity_Surname)
        Locker_FormLayout.addRow(Label_Phone, self.LockerIdentity_Phone)
        Locker_FormLayout.addRow(Label_Mail, self.LockerIdentity_Mail)

        vbox_FromLayout = QVBoxLayout()
        vbox_FromLayout.addLayout(Locker_FormLayout)
        vbox_FromLayout.setAlignment(QtCore.Qt.AlignCenter)


        self.Locker_Button_Confirm = QPushButton("Onayla", objectName="GeneralButton")
        self.Locker_Button_Confirm.setVisible(False)
        self.Locker_Button_Confirm.clicked.connect(self.Locker_CreateLocker)

        vbox.addWidget(info, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(SB_ID_TextEditor, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(Locker_Button_GetIdentity, alignment=QtCore.Qt.AlignCenter)
        vbox.addLayout(vbox_FromLayout)
        vbox.addLayout(hbox_LockerSizeButton)
        vbox.addWidget(self.Locker_emptyBoxCount,alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.Locker_Button_Confirm, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)

        self.groupBox_Locker_FindItentity.setLayout(vbox)

        return self.groupBox_Locker_FindItentity

    def Locker_SearchEmptyBox(self):
        if self.Locker_SmallSize.isChecked():
            self.Locker_box_size = "S"
        elif self.Locker_MediumSize.isChecked():
            self.Locker_box_size = "M"
        elif self.Locker_BigSize.isChecked():
            self.Locker_box_size = "L"
        else:
            print("choose something")

        empty_box = CreateRow.CreateRow().findEmptyBox(self.safetybox_name, self.Locker_box_size)
        print("****", empty_box)

        return empty_box

    def Locker_GetIdentity(self, person_code):
        self.IdentityValues = self.database.getIdentity_withPersonCode(str(person_code))
        print("Locker_GetIdentity Function: ", self.IdentityValues)
        if self.IdentityValues is None:
            print("Person Code ile Kişi Bulunamadı")
            self.info_dialog.setText("Kişi Kayıtlı Değildir. \n"
                                     "Kodunuzu kontrol edin veya kayıt olun.")
            self.button.setText("Tekrar Dene")
            self.info_dialog.setHidden(False)

        else:

            self.Locker_Button_Confirm.setVisible(True)
            self.LockerIdentity_Name.setText(": " + self.IdentityValues[1])
            self.LockerIdentity_Surname.setText(": " + self.IdentityValues[2])
            number = str(self.IdentityValues[3])
            number = number[:5] + "*" + number[6:8] + "**"
            self.LockerIdentity_Phone.setText(": " + number)
            mail = self.IdentityValues[4].split("@")
            mail[0] = mail[0][:-5]+"*****"
            self.LockerIdentity_Mail.setText(": " + mail[0] + "@" + mail[1])
            return

    def Locker_CreateLocker(self):
        emptybox_ID = self.Locker_SearchEmptyBox()

        if len(emptybox_ID) == 0:
            self.info_dialog.setText("Maalesef seçtiğiniz boyuttaki \ndolaplarımız doludur")
            self.button.setText("Tamam")
            self.info_dialog.setHidden(False)

        else:
            identities_ID = self.IdentityValues[0]
            surname = self.IdentityValues[2]
            name = self.IdentityValues[1]
            county = self.safetybox_county
            city = self.safetybox_city
            #generating pnr num, tracking num and qrcode
            PNR, Tracking, QRCode, datetime = Code_Generator.Code_Generator().Generate_AllCodes("L", surname, name, county, city)
            #creating safety locker
            self.database.create_SafetyLocker(PNR, QRCode, str(emptybox_ID[0][0]), identities_ID, datetime, "0")
            #chanhing box's empty state
            self.database.setBoxState_isEmpty("0", str(emptybox_ID[0][0]))
            self.Locker_SearchEmptyBox() #updating emptybox count

            #send mail
            parameters = [name, surname, "", self.IdentityValues[4], "", PNR, self.safetybox_name,
                          self.safetybox_address, self.safetybox_county, self.safetybox_city]
            Mail.SendMail("Creating_SafetyLocker", parameters)


    def GB_Locker_NewIdentity(self):
        self.groupBox_Locker_NewIdentity = QGroupBox("Kişi Kodu ile Emanet Bırakma")
        self.groupBox_Locker_NewIdentity.setVisible(False)


        info = QLabel(objectName="LockerLabels")
        info.setText("Kayıt olmak için bilgilerinizi doldurunuz.")

        Label_Name = QLabel("Ad", objectName="LockerLabels")
        Label_Surname = QLabel("Soyad", objectName="LockerLabels")
        Label_Phone = QLabel("Telefon", objectName="LockerLabels")
        Label_Mail = QLabel("Mail", objectName="LockerLabels")

        Locker_LineEdit_Name = QLineEdit(objectName="LockerLineEdit")
        Locker_LineEdit_Name.setPlaceholderText("Adınızı Girin")
        Locker_LineEdit_Name.setFixedWidth(Locker_LineEdit_Name.sizeHint().width()+50)
        Locker_LineEdit_Surname = QLineEdit(objectName="LockerLineEdit")
        Locker_LineEdit_Surname.setPlaceholderText("Soyadınızı Girin")
        Locker_LineEdit_Surname.setFixedWidth(Locker_LineEdit_Surname.sizeHint().width()+50)
        Locker_LineEdit_Phone = QLineEdit(objectName="LockerLineEdit")
        Locker_LineEdit_Phone.setPlaceholderText("Örn: 5XXXXXXXXX")
        Locker_LineEdit_Phone.setFixedWidth(Locker_LineEdit_Phone.sizeHint().width()+50)
        Locker_LineEdit_Phone.setValidator(QIntValidator())
        Locker_LineEdit_Mail = QLineEdit(objectName="LockerLineEdit")
        Locker_LineEdit_Mail.setPlaceholderText("Mailinizi Girin")
        Locker_LineEdit_Mail.setFixedWidth(Locker_LineEdit_Mail.sizeHint().width()+50)

        Locker_FormLayout = QFormLayout()
        Locker_FormLayout.addRow(Label_Name,  Locker_LineEdit_Name)
        Locker_FormLayout.addRow(Label_Surname, Locker_LineEdit_Surname)
        Locker_FormLayout.addRow(Label_Phone, Locker_LineEdit_Phone)
        Locker_FormLayout.addRow(Label_Mail, Locker_LineEdit_Mail)

        hbox_FromLayout = QHBoxLayout()
        hbox_FromLayout.addStretch()
        hbox_FromLayout.addLayout(Locker_FormLayout)
        hbox_FromLayout.addStretch()

        confirmbutton = QPushButton("Kaydet", objectName="GeneralButton")
        confirmbutton.clicked.connect(lambda: self.Locker_CreatIdentity(Locker_LineEdit_Name.text(),
                                                                        Locker_LineEdit_Surname.text(),
                                                                        Locker_LineEdit_Phone.text(),
                                                                        Locker_LineEdit_Mail.text(),))

        vbox = QVBoxLayout()
        vbox.addWidget(info, alignment=QtCore.Qt.AlignCenter)
        vbox.addLayout(hbox_FromLayout)
        vbox.addWidget(confirmbutton, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)

        self.groupBox_Locker_NewIdentity.setLayout(vbox)

        return self.groupBox_Locker_NewIdentity

    def Locker_CreatIdentity(self, name, surname, phone, mail):
        name = name.translate(self.Tr2Eng)
        surname = surname.translate(self.Tr2Eng)
        mail = mail.translate(self.Tr2Eng)
        result = CreateRow.CreateRow().checkIdenties(name, surname, str(phone), mail)
        print("checking Identity", result)

        if result is True:
            self.info_dialog.setText("Girdiğiniz telefon numarasına kayıtlı\n"
                                     "kullanıcı mevcuttur. SafetyBox ID'niz\n"
                                     "SMS ve Mail olarak tarafınıza iletilmiştir.")
            self.button.setText("Tamam")
            self.info_dialog.setHidden(False)

        else:
            self.Open_Locker_FindIdentity()
            person_code = self.database.getIdentity_withPhone(str(phone))
            self.Locker_GetIdentity(person_code[0][5])


    def B_receivingFunction(self):  # receiving button function
        self.tab.addTab(self.tab2, "Kargo Alma Aşaması")
        self.tab.setCurrentWidget(self.tab2)
        self.settingButton.setVisible(False)

    def B_deliveringFunction(self):  # delivering button function
        self.tab.addTab(self.tab3, "Kargo Verme Aşaması")
        self.tab.setCurrentWidget(self.tab3)  # pass tab-5 when clicked button
        self.settingButton.setVisible(False)

    def B_LockerFunction(self):
        self.groupBox_Locker_ChoosingMenu.setVisible(True)
        self.groupBox_Locker_NewIdentity.setVisible(False)
        self.groupBox_Locker_FindItentity.setVisible(False)

        self.tab.addTab(self.tab4, "Kargo Verme Aşaması")
        self.tab.setCurrentWidget(self.tab4)  # pass tab-6 when clicked button
        self.settingButton.setVisible(False)

    def B_BackMainButton(self):

        self.BackButton = QPushButton("Ana Menüye Dönmek için Tıklayınız", objectName="BackMainButton")
        self.BackButton.setIcon(QIcon("home/pi/Desktop/SafetyBox/icons/Home.png"))
        self.BackButton.setIconSize(QtCore.QSize(30, 30))

        self.BackButton.clicked.connect(self.BackMainFunction)

        self.settingButton.setVisible(True)

        return self.BackButton

    def W_DatabaseWindow(self):  # calling database window class
        self.w_DB = Database_Window.Window_DB("İlçeler")
        self.w_DB.show()

    def W_Database_CreateRow(self):  # calling database CreateRow window class
        self.cr_W = CreateRow.CreateRow()
        self.cr_W.show()

    @pyqtSlot(QImage)
    def setImage(self, image):  # set camera image for thread class
        self.CameraLabel_R.setPixmap(QPixmap.fromImage(image))
        self.CameraLabel_D.setPixmap(QPixmap.fromImage(image))

    def cllback(self, barcodeData):  # take back barcode value from thread class
        self.barcodeData = barcodeData
        values = self.Finder.QRCodeFinder(barcodeData)
        print("Values: ", values)
        # print(cargo_type)
        if values is None:
            print("QR CODE KİŞİSİ BULUNAMADI")
            self.info_dialog.setText("QR Kod sistemde kayıtlı değildir.\n"
                                     "PNR ile teslim alamayı deneyin veya \n"
                                     "bizimle iletişime geçin.")
            self.button.setText("Tekrar Dene")
            self.info_dialog.setHidden(False)
        elif values[0] == "receiver":
            tracking_no = self.database.getTrackingNo_withQRCode(barcodeData)  # taking tracking no with PNR
            self.infoWin.showInfoWindow(values[0], values[1], tracking_no)
            return

        elif values[0] == "Locker":
            pnr_no = self.database.getLockerPNRNo_withQRCode(barcodeData)  # taking tracking no with PNR
            self.infoWin.showInfoWindow(values[0], values[1], pnr_no)
            return

    def cllback_TakePicture(self, receiver_ID, current_time):
        self.th.takePicture(receiver_ID, current_time)

    def PNRFinder(self):
        if self.PNRTextEditor.text() != "":
            currernttext = self.PNRTextEditor.text()
            values = self.Finder.PNRFinder(currernttext)
            if values is None:

                self.info_dialog.setText("PNR Numarası sistemde kayıtlı değildir.\n"
                                         "QR Kod ile teslim alamayı deneyin veya \n"
                                         "bizimle iletişime geçin.")
                self.button.setText("Tekrar Dene")
                self.info_dialog.setHidden(False)
            else:
                tracking_no = self.database.getTrackingNo_withPNRNo(currernttext)  # taking tracking no with PNR
                self.infoWin.showInfoWindow(values[0], values[1], tracking_no)  # showing info window


        else:
            QMessageBox.information(self, "Bilgilendirme", "PNR Numarası Girmediniz\n"
                                                           "Lütfen PNR Numarası Girip Tekrar Deneyiniz")

    def TrackingFinder(self):
        if self.TrackTextEditor.text() != "":
            currernttext = self.TrackTextEditor.text()
            values = self.Finder.TrackFinder(currernttext)
            if values is None:
                self.info_dialog.setText("Takip Numarası sistemde kayıtlı değildir.\n"
                                         "Barkod ile teslim etmeyi deneyin veya \n"
                                         "bizimle iletişime geçin.")
                self.button.setText("Tekrar Dene")
                self.info_dialog.setHidden(False)
            else:
                self.infoWin.showInfoWindow(values[0], values[1], None)
                Mail.SendMail("Delivering_Cargo", values[2])  # Gelen 3.değeri mail dosyasına yolluyor.

        else:
            QMessageBox.information(self, "Bilgilendirme", "Takip Numarası Girmediniz\n"
                                                           "Lütfen Takip Numarası Girip Tekrar Deneyiniz")

    def Database_Update(self):  # Database value uptade
        self.tab.addTab(self.tab6, "DB Güncelleme")
        self.tab.setCurrentWidget(self.tab6)

    def BackMainFunction(self):
        self.settingButton.setVisible(True)
        currenttab = self.tab.indexOf(self.tab.currentWidget())
        self.tab.setCurrentWidget(self.tab1)

        if self.tab.currentWidget() == self.tab1:
            self.tab.removeTab(currenttab)

    def tabs(self):  # tabs function

        mainLayout = QVBoxLayout()  # tab's Main Layout

        self.tab = QTabWidget()  # create Tab

        self.tab1 = QWidget()  # create tab-1 (step-1) main tab
        self.tab2 = QWidget()  # create tab-2 (step-2) receiver tab
        self.tab3 = QWidget()  # create tab-3 (step-3) delivery tab
        self.tab4 = QWidget()  # create tab-4 (step-4) luggage locker
        self.tab5 = QWidget()  # create tab-5 (step-5) update tab
        self.tab6 = QWidget()  # create tab-6 (step-6) settings tab

        tab1_vbox = QVBoxLayout()  # tab-1's main layout
        tab1_hbox = QHBoxLayout()  # tab-1's layout
        tab2_vbox = QVBoxLayout()  # tab-2's layout
        tab3_vbox = QVBoxLayout()  # tab-3's layout
        tab4_hbox = QHBoxLayout()  # tab-4's layout
        tab5_vbox = QVBoxLayout()  # tab-5's layout
        tab6_vbox = QVBoxLayout()  # tab-6's layout

        # Main TAB Settings Button
        self.settingButton = QPushButton(objectName="SettingsButton")
        self.settingButton.clicked.connect(self.OpenSettingWindow)
        # self.settingButton.setIcon(QIcon("icons/setting.png"))
        # self.settingButton.setIconSize(QSize(64,64))
        # self.settingButton.setFixedWidth(60)
        # self.settingButton.setFixedHeight(60)

        # TAB-5 Widgets
        self.databaseAddRow = QPushButton("Add Row", objectName="GeneralButton")
        self.databaseAddRow.clicked.connect(self.W_Database_CreateRow)
        self.databaseButton = QPushButton("DB Table", objectName="GeneralButton")
        self.databaseButton.clicked.connect(self.W_DatabaseWindow)
        self.databaseUpdateRow = QPushButton("Update Row", objectName="GeneralButton")
        self.databaseUpdateRow.clicked.connect(self.Database_Update)

        # TAB-5 Widgets END

        # TAB-6 Widgets
        self.U_TextLabel = QLabel("")

        self.U_Column = QComboBox(self)
        self.U_Column.addItems(["Değiştirmek istediğiniz sütunu seçiniz.", "isim", "soyisim", "mail"])

        self.U_Tel_Num = QLineEdit()
        self.U_Tel_Num.setPlaceholderText("Verisi değiştirilmek istenin kişinin telefon numarasını giriniz.")

        self.U_N_Value = QLineEdit()
        self.U_N_Value.setPlaceholderText("Yeni veriyi giriniz.")

        self.U_Button = QPushButton("Kaydet", objectName="GeneralButton")
        self.U_Button.clicked.connect(self.Database_Update)
        # TAB-6 Widgets END

        # widgets are placed
        tab1_hbox.addWidget(self.GB_cargoReceive())
        tab1_hbox.addWidget(self.GB_cargoDelivery())
        tab1_vbox.addLayout(tab1_hbox, 70)
        tab1_vbox.addWidget(self.GB_LockerSystem(), 30)

        tab2_vbox.addWidget(self.GB_cargoPNR())

        tab3_vbox.addWidget(self.GB_cargoTrack())

        tab4_hbox.addWidget(self.GB_Locker_ChoosingMenu())
        tab4_hbox.addWidget(self.GB_Locker_NewIdentity())
        tab4_hbox.addWidget(self.GB_Locker_FindIdentity())

        tab5_vbox.addWidget(self.databaseAddRow)
        tab5_vbox.addWidget(self.databaseUpdateRow)
        tab5_vbox.addWidget(self.databaseButton)
        tab5_vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)

        tab6_vbox.addStretch()
        tab6_vbox.addWidget(self.U_TextLabel)
        tab6_vbox.addWidget(self.U_Column)
        tab6_vbox.addWidget(self.U_N_Value)
        tab6_vbox.addWidget(self.U_Tel_Num)
        tab6_vbox.addWidget(self.U_Button)
        tab6_vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)
        tab6_vbox.addStretch()

        # tab's layout setted
        self.tab1.setLayout(tab1_vbox)
        self.tab2.setLayout(tab2_vbox)
        self.tab3.setLayout(tab3_vbox)
        self.tab4.setLayout(tab4_hbox)
        self.tab5.setLayout(tab5_vbox)
        self.tab6.setLayout(tab6_vbox)

        self.tab.addTab(self.tab1, "Ana Sayfa")
        # TABS WILL OPEN WHEN YOU CLICK BUTTON
        # self.tab.addTab(self.tab2, "Kargo Alma Aşaması")
        # self.tab.addTab(self.tab3, "Kargo Verme Aşaması")
        # self.tab.addTab(self.tab4, "DataBase İşlemleri")
        # self.tab.addTab(self.tab5, "DB Güncelleme")

        mainLayout.addWidget(self.settingButton, alignment=QtCore.Qt.AlignRight)
        mainLayout.addWidget(self.tab)
        self.tab2.setStyleSheet("QTabBar::tab::disabled {width: 0; height: 0; margin: 0; padding: 0; border: none;} ")

        self.setLayout(mainLayout)


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    mem_barcodeData = ""

    def setCllback(self, cllbck):
        print("thread setcllback func girildi")
        self.cllbck = cllbck

    def run(self):
        counter = 0
        self.cap = cv2.VideoCapture(0)

        self.threadactive = True

        while True:
            ret, self.frame = self.cap.read()
            if self.cap.read() is None:
                break
            barcodes = pyzbar.decode(self.frame)
            found = set()

            for barcode in barcodes:
                counter = counter + 1
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(self.frame, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode   q to disk and update the set
                if barcodeData not in found:
                    if counter % 10 == 0:
                        if barcodeData != self.mem_barcodeData:
                            print(counter, barcodeData)

                            self.mem_barcodeData = barcodeData
                            self.cllbck(barcodeData)

            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def takePicture(self, receiver_ID, saving_name):
        cv2.imwrite("home/pi/Desktop/receiver_Person/" + str(receiver_ID) + "/" + str(saving_name) + ".jpg",
                    self.frame)


app = QApplication([])
app.setStyleSheet(StyleSheet)
mainwindow = Window()
mainwindow.show()
app.exec_()

# if __name__ == "__main__":
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#     palette = QPalette()
#     palette.setColor(QPalette.Window, QColor(53, 53, 53))
#     palette.setColor(QPalette.WindowText, QtCore.Qt.white)
#     palette.setColor(QPalette.Base, QColor(15, 15, 15))
#     palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
#     palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
#     palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
#     palette.setColor(QPalette.Text, QtCore.Qt.white)
#     palette.setColor(QPalette.Button, QColor(53, 53, 53))
#     palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
#     palette.setColor(QPalette.BrightText, QtCore.Qt.red)
#
#     palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
#     palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
#     app.setPalette(palette)
#     app.setStyleSheet(StyleSheet)
#     MainWindow = Window()
#     MainWindow.show()
#     sys.exit(app.exec_())
