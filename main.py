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
import Window_DB
import main_DB
import adminPassWindow

# GUI Button Shape
StyleSheet = '''  
QPushButton#DeliveringButton {
    background-color: #0000ff;
    border-radius: 48px;
}

QPushButton#DeliveringButton:hover {
    background-color: #64b5f6;
    color: #fff;
}

QPushButton#DeliveringButton:pressed {
    background-color: #bbdefb;
}

QPushButton#ReceivingButton {
    background-color: #ff0000;
    border-radius: 48px;
}

QPushButton#ReceivingButton:hover {
    background-color: #FC937C;
    color: #fff;
}

QPushButton#ReceivingButton:pressed {
    background-color: #FABCAF;
}

QPushButton#GeneralButton{
    background-color : #48E0FA;
    border-radius: 14px;
    font-size: 15pt;
}

QPushButton#GeneralButton:hover{
    background-color: #FFDBA0;
}

QPushButton#GeneralButton:pressed {
    background-color: #F9EDC7;
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
    qproperty-icon: url("icons/setting.png"); 
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

'''

class Window(QWidget):
    Finder = Finder.Finder()

    def __init__(self):
        super().__init__()  # QWidget fonskiyonlarını kullanabilmek icin
        self.setGeometry(0, 0, 800, 640)  # window size
        self.setWindowTitle("Safety Box")  # window title
        background_Color = self.palette()
        background_Color.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(background_Color)


        self.database = main_DB.main_DB()  # calling database class


        self.tabs()  # initialize tabs
        self.show()

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)

        # messagebox opened, when no cargo is found
        self.info_dialog = QtWidgets.QMessageBox(self)
        self.info_dialog.setIcon(QMessageBox.Information)
        self.info_dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTitleHint)  # no title bar
        self.info_dialog.setWindowIcon(QIcon('icons/icon.png'))
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
            self.tab.addTab(self.tab4, "Ayarlar")
            self.tab.setCurrentWidget(self.tab4)
            self.settingButton.setVisible(False)
            self.admin_W.close()
        else:
            print("Giriş başarısız")

    def GB_cargoReceive(self):  # Kargo Teslim Alma - Step1

        groupBox = QGroupBox("Kargo Teslim Alma")

        vbox = QVBoxLayout()

        receivingButton = QPushButton("Kargo Teslim\nAlma", objectName="ReceivingButton")  # button initialize
        receivingButton.installEventFilter(self)
        # receivingButton.setFixedSize(receivingButton.width(), receivingButton.height())  # button size maximize
        receivingButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        receivingButton.setFont(QFont("Arial", 50, QFont.Bold))  # button font

        receivingButton.clicked.connect(self.B_receivingFunction)

        vbox.addWidget(receivingButton)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_cargoDelivery(self):  # Kargo Teslim Etme - Step1
        groupBox = QGroupBox("Kargo Teslim Etme")

        vbox = QVBoxLayout()
        deliveringButton = QPushButton("Kargo Teslim\nEtme", objectName="DeliveringButton")  # button initialize
        deliveringButton.installEventFilter(self)
        # deliveringButton.setFixedSize(deliveringButton.width(), deliveringButton.height())  # button size maximize
        deliveringButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        deliveringButton.setFont(QFont("Arial", 50, QFont.Bold))  # button font
        deliveringButton.clicked.connect(self.B_deliveringFunction)
        vbox.addWidget(deliveringButton)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_cargoPNR(self):  # Kargo Teslim Grup Box - Step2

        groupBox = QGroupBox("Kargo Teslim")

        info_PNRDelivery = QLabel("Kargonuzu PNR ile teslim almak için butona basınız.")
        info_PNRDelivery.setFont(QFont("Arial", 30, QFont.Bold))
        info_PNRDelivery.setAlignment(Qt.AlignCenter)

        self.PNRTextEditor = QLineEdit()
        self.PNRTextEditor.setPlaceholderText("PNR Kod Giriniz")
        self.PNRTextEditor.setValidator(QIntValidator())
        self.PNRTextEditor.setStyleSheet("color : blue")

        PNRbutton = QPushButton("Kargo Teslim Al", objectName="GeneralButton")

        # PNRbutton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        PNRbutton.installEventFilter(self)
        PNRbutton.setFont(QFont("Time New Roman", 20))
        PNRbutton.clicked.connect(self.PNRFinder)
        PNRbutton.setFixedSize(int(PNRbutton.sizeHint().width())+50, PNRbutton.sizeHint().height()+10)

        self.PNRText = QLabel("")  # success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addWidget(self.PNRTextEditor)
        vbox.addWidget(self.PNRText)
        vbox.addWidget(PNRbutton, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)
        vbox.addStretch()
        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_instructions(self):  # Talimatlar Group Box - Step2
        self.infoWin = InfoWindow.InfoWindow()
        self.infoWin.setCllBack_TakePicture(self.cllback_TakePicture)

        self.CameraLabel_R = QLabel(self)
        # self.label.move(280, 120)
        self.CameraLabel_R.resize(640, 480)
        self.th = Thread(self)
        self.th.setCllback(self.cllback)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        groupBox = QGroupBox("Talimatlar")  # create groupbox

        info_instructions = QLabel("QR Kodunuzu Aşağıdaki Cihaza Okutunuz")
        info_instructions.setFont(QFont("Arial", 30, QFont.Bold))

        image1 = QLabel(self)  # instruction picture one
        image1.setPixmap(QPixmap("qrkod1.jpg"))

        image2 = QLabel(self)  # instruction picture two
        image2.setPixmap(QPixmap("qrkod1.jpg"))

        image3 = QLabel(self)  # instruction picture three
        image3.setPixmap(QPixmap("qrkod1.jpg"))

        hbox = QHBoxLayout()  # create layout

        hbox.addStretch()
        hbox.addWidget(image1)
        hbox.addWidget(image2)
        hbox.addWidget(image3)
        hbox.addStretch()

        vbox = QVBoxLayout()

        vbox.addWidget(info_instructions, alignment=QtCore.Qt.AlignCenter)
        vbox.addLayout(hbox)

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(hbox)
        main_hbox.addLayout(vbox)
        main_hbox.addWidget(self.CameraLabel_R)

        groupBox.setLayout(main_hbox)  # hbox is placed in groupbox

        return groupBox

    def GB_cargoTrack(self):  # Kargo teslim verme
        groupBox = QGroupBox("Kargo Teslim Verme ")

        info_PNRDelivery = QLabel("Kargoyu Teslim Vermek İçin Butona Basınız")
        info_PNRDelivery.setFont(QFont("Arial", 15, QFont.Bold))

        self.TrackTextEditor = QLineEdit(self)
        self.TrackTextEditor.setPlaceholderText("Takip Numarasını Giriniz")
        self.TrackTextEditor.setValidator(QIntValidator())

        Trackbutton = QPushButton("Kargo Teslim Et", objectName="GeneralButton")
        Trackbutton.setFont(QFont("Time New Roman", 20))
        Trackbutton.clicked.connect(self.TrackingFinder)
        Trackbutton.setFixedSize(int(Trackbutton.sizeHint().width()) + 50, Trackbutton.sizeHint().height() + 10)

        self.TrackText = QLabel("")  # success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addWidget(self.TrackTextEditor)
        vbox.addWidget(self.TrackText)
        vbox.addWidget(Trackbutton, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.B_BackMainButton(), alignment=QtCore.Qt.AlignCenter)
        vbox.addStretch()
        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def GB_BarCode(self):
        self.CameraLabel_D = QLabel(self)
        # self.label.move(280, 120)
        self.CameraLabel_D.resize(640, 480)
        grupbox = QGroupBox("Barkod Okuyucu")

        title = QLabel("Kargonuzun barkodunu Aşağıya Okutunuz")
        title.setFont(QFont("Arial", 30, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)

        image = QLabel()
        png = QPixmap("barcode.png")
        png.scaled(64, 64)
        image.setPixmap(png)
        image.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(title)
        vbox.addWidget(image)

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(vbox)
        main_hbox.addWidget(self.CameraLabel_D)

        grupbox.setLayout(main_hbox)
        return grupbox

    def B_receivingFunction(self):  # receiving button function
        self.tab.addTab(self.tab2, "Kargo Alma Aşaması")
        self.tab.setCurrentWidget(self.tab2)

    def B_deliveringFunction(self):  # delivering button function
        self.tab.addTab(self.tab3, "Kargo Verme Aşaması")
        self.tab.setCurrentWidget(self.tab3)  # pass tab-5 when clicked button

    def B_BackMainButton(self):

        self.BackButton = QPushButton("Ana Menüye Dönmek için Tıklayınız", objectName="GeneralButton")
        self.BackButton.setFont(QFont("Arial", 20))
        self.BackButton.setIcon(QIcon("Home.png"))
        self.BackButton.setIconSize(QtCore.QSize(45, 45))
        self.BackButton.setFixedSize(int(self.BackButton.sizeHint().width())+50, self.BackButton.sizeHint().height()+10)
        self.BackButton.clicked.connect(self.BackMainFunction)

        return self.BackButton

    def W_DatabaseWindow(self):  # calling database window class
        self.w_DB = Window_DB.Window_DB("İlçeler")
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
            self.info_dialog.setText("Aradığınız kişi bulunamamıştır.\n "
                                     "Kontrol edip tekrar deneyiniz.")
            self.button.setText("Tekrar Dene")
            self.info_dialog.setHidden(False)
        else:
            tracking_no = self.database.getTrackingNo_withQRCode(barcodeData)  # taking tracking no with PNR
            self.infoWin.showInfoWindow(values[0], values[1], tracking_no)
            return

    def cllback_TakePicture(self, receiver_ID, current_time):
        self.th.takePicture(receiver_ID, current_time)

    def PNRFinder(self):
        if self.PNRTextEditor.text() != "":
            currernttext = self.PNRTextEditor.text()
            values = self.Finder.PNRFinder(currernttext)
            if values is None:

                self.info_dialog.setText("Aradığınız kişi bulunamamıştır.\n "
                                         "Kontrol edip tekrar deneyiniz.")
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
                self.info_dialog.setText("Aradığınız kişi bulunamamıştır.\n "
                                         "Kontrol edip tekrar deneyiniz.")
                self.button.setText("Tekrar Dene")
                self.info_dialog.setHidden(False)
            else:
                self.infoWin.showInfoWindow(values[0], values[1], None)
                Mail.SendMail("Delivering_Cargo", values[2])  # Gelen 3.değeri mail dosyasına yolluyor.

        else:
            QMessageBox.information(self, "Bilgilendirme", "Takip Numarası Girmediniz\n"
                                                           "Lütfen Takip Numarası Girip Tekrar Deneyiniz")

    def Database_Update(self):  # Database value uptade
        self.tab.addTab(self.tab5, "DB Güncelleme")
        self.tab.setCurrentWidget(self.tab5)

    def BackMainFunction(self):
        self.settingButton.setVisible(True)
        currenttab = self.tab.indexOf(self.tab.currentWidget())
        self.tab.setCurrentWidget(self.tab1)

        if self.tab.currentWidget() == self.tab1:
            self.tab.removeTab(currenttab)

    def tabs(self):  # tabs function

        mainLayout = QVBoxLayout()  # tab's Main Layout

        self.tab = QTabWidget()  # create Tab

        self.tab1 = QWidget()  # create tab-1 (step-1)
        self.tab2 = QWidget()  # create tab-2 (step-2)
        self.tab3 = QWidget()  # create tab-3 (step-3)
        self.tab4 = QWidget()  # create tab-4 (step-4)
        self.tab5 = QWidget()  # create tab-5 (step-5)

        tab1_grid = QGridLayout()  # tab-1's layout
        tab2_grid = QGridLayout()  # tab-2's layout
        tab5_vbox = QVBoxLayout()  # tab-3's layout
        tab4_vbox = QVBoxLayout()  # tab-4's layout
        tab3_grid = QGridLayout()  # tab-5's layout

        #Main TAB Settings Button
        self.settingButton = QPushButton(objectName="SettingsButton")
        self.settingButton.clicked.connect(self.OpenSettingWindow)
        # self.settingButton.setIcon(QIcon("icons/setting.png"))
        # self.settingButton.setIconSize(QSize(64,64))
        # self.settingButton.setFixedWidth(60)
        # self.settingButton.setFixedHeight(60)

        # TAB-4 Widgets
        self.databaseAddRow = QPushButton("Add Row", objectName="GeneralButton")
        self.databaseAddRow.clicked.connect(self.W_Database_CreateRow)
        self.databaseButton = QPushButton("DB Table", objectName="GeneralButton")
        self.databaseButton.clicked.connect(self.W_DatabaseWindow)
        self.databaseUpdateRow = QPushButton("Update Row", objectName="GeneralButton")
        self.databaseUpdateRow.clicked.connect(self.Database_Update)

        # TAB-4 Widgets END

        # TAB-5 Widgets
        self.U_TextLabel = QLabel("")

        self.U_Column = QComboBox(self)
        self.U_Column.addItems(["Değiştirmek istediğiniz sütunu seçiniz.", "isim", "soyisim", "mail"])

        self.U_Tel_Num = QLineEdit()
        self.U_Tel_Num.setPlaceholderText("Verisi değiştirilmek istenin kişinin telefon numarasını giriniz.")

        self.U_N_Value = QLineEdit()
        self.U_N_Value.setPlaceholderText("Yeni veriyi giriniz.")

        self.U_Button = QPushButton("Kaydet", objectName="GeneralButton")
        self.U_Button.clicked.connect(self.Database_Update)
        # TAB-5 Widgets END

        # widgets are placed
        tab1_grid.addWidget(self.GB_cargoReceive(), 0, 0)
        tab1_grid.addWidget(self.GB_cargoDelivery(), 0, 1)
        tab2_grid.addWidget(self.GB_cargoPNR(), 0, 0)
        tab2_grid.addWidget(self.GB_instructions(), 1, 0)
        tab3_grid.addWidget(self.GB_cargoTrack(), 0, 0)
        tab3_grid.addWidget(self.GB_BarCode(), 1, 0)
        tab4_vbox.addWidget(self.databaseAddRow)
        tab4_vbox.addWidget(self.databaseUpdateRow)
        tab4_vbox.addWidget(self.databaseButton)
        tab4_vbox.addWidget(self.B_BackMainButton())
        tab5_vbox.addStretch()
        tab5_vbox.addWidget(self.U_TextLabel)
        tab5_vbox.addWidget(self.U_Column)
        tab5_vbox.addWidget(self.U_N_Value)
        tab5_vbox.addWidget(self.U_Tel_Num)
        tab5_vbox.addWidget(self.U_Button)
        tab5_vbox.addWidget(self.B_BackMainButton())
        tab5_vbox.addStretch()

        # tab's layout setted
        self.tab1.setLayout(tab1_grid)
        self.tab2.setLayout(tab2_grid)
        self.tab3.setLayout(tab3_grid)
        self.tab4.setLayout(tab4_vbox)
        self.tab5.setLayout(tab5_vbox)

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
                p = convertToQtFormat.scaled(360, 270, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def takePicture(self, receiver_ID, saving_name):
        cv2.imwrite("/home/pi/Desktop/receiver_Person/" + str(receiver_ID) + "/" + str(saving_name) + ".jpg",
                    self.frame)


app = QApplication([])
app.setStyleSheet(StyleSheet)
mainwindow = Window()
mainwindow.show()
app.exec_()
