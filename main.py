from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.Qt import *
from PyQt5 import QtCore
import InfoWindow
import main_DB
import Window_FilterDB
import Window_DB
import CreateRow
import DeliveryWindow
import QRCode_RPCam
import time
import cv2
import Finder
from pyzbar import pyzbar

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
background-color : #FF9E00 
}

QPushButton#GeneralButton:hover{
 background-color: #FFDBA0 
}
'''


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, 1080, 732)  # window size
        self.window_widget = Window()
        self.setCentralWidget(self.window_widget)  # Ana Widget olarak Window classını çağırıyoruz
        self.menubar()
        self.show()

    def menubar(self):  # Menu Bar oluşturma
        bar = self.menuBar()
        file = bar.addMenu("Ayarlar")

        dbu = QAction("DataBase Güncelleme", self)
        file.addAction(dbu)

        dbt = QAction("DataBase İşlemleri", self)
        file.addAction(dbt)

        dbt.triggered.connect(self.window_widget.DBTool)
        dbu.triggered.connect(self.window_widget.DBU)
        # file.triggered[QAction].connect(self.window_widget.DBTool)


class Window(QWidget):
    Finder = Finder.Finder()

    def __init__(self):
        super().__init__()  # QWidget fonskiyonlarını kullanabilmek icin

        self.setGeometry(0, 0, 1080, 732)  # window size
        self.setWindowTitle("Safety Box")  # window title
        self.database = main_DB.main_DB()  # calling database class
        self.tabs()  # initialize tabs
        self.show()

    def cargoReceive(self):  # Kargo Teslim Alma - Step1

        groupBox = QGroupBox("Kargo Teslim Alma")

        vbox = QVBoxLayout()

        receivingButton = QPushButton("Kargo Teslim\nAlma", objectName="ReceivingButton")  # button initialize
        receivingButton.installEventFilter(self)
        receivingButton.setFixedSize(receivingButton.width(), receivingButton.height())  # button size maximize
        receivingButton.setFont(QFont("Arial", 50, QFont.Bold))  # button font
        # deliveringButton.setVisible(False)
        receivingButton.clicked.connect(self.receivingFunction)
        # unclicked unvisible
        # print(groupBox.width())
        # vbox.setContentsMargins((groupBox.width()-deliveringButton.width()),0,0,0)
        vbox.addWidget(receivingButton)
        groupBox.setLayout(vbox)

        return groupBox

    def cargoDelivery(self):  # Kargo Teslim Etme - Step1
        groupBox = QGroupBox("Kargo Teslim Etme")

        vbox = QVBoxLayout()
        deliveringButton = QPushButton("Kargo Teslim\nEtme", objectName="DeliveringButton")  # button initialize
        deliveringButton.installEventFilter(self)
        deliveringButton.setFixedSize(deliveringButton.width(), deliveringButton.height())  # button size maximize
        deliveringButton.setFont(QFont("Arial", 50, QFont.Bold))  # button font
        deliveringButton.clicked.connect(self.deliveringFunction)
        vbox.addWidget(deliveringButton)
        groupBox.setLayout(vbox)

        return groupBox

    def receivingFunction(self): #receiving button function
        self.tab.addTab(self.tab2, "Kargo Alma Aşaması")
        self.tab.setCurrentWidget(self.tab2)



    def deliveringFunction(self): #delivering button function
        self.tab.addTab(self.tab3, "Kargo Verme Aşaması")
        self.tab.setCurrentWidget(self.tab3)  # pass tab-5 when clicked button
        self.QRWindow = QRCode_RPCam.QRWindow()
        self.QRWindow.show()

    def DBTool(self):  # Menu Bar Database İslemleri
        self.tab.addTab(self.tab4, "DataBase İşlemleri")
        self.tab.setCurrentWidget(self.tab4)
        # self.tab.setCurrentIndex(0) İndex numarasına gidiyor

    def DBU(self):  # Menu Bar Database Güncelleme
        self.tab.addTab(self.tab5, "DB Güncelleme")
        self.tab.setCurrentWidget(self.tab5)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.CameraLabel.setPixmap(QPixmap.fromImage(image))

    def cllback(self, barcodeData):
        self.barcodeData = barcodeData
        cargo_type, infoList = self.Finder.QRCodeFinder(barcodeData)
        # print(cargo_type)
        self.infoWin.showInfoWindow(cargo_type, infoList)
        return

    def instructions(self):  # Talimatlar Group Box - Step2
        self.infoWin = InfoWindow.InfoWindow()

        self.CameraLabel = QLabel(self)
        # self.label.move(280, 120)
        self.CameraLabel.resize(640, 480)
        self.th = Thread(self)
        self.th.setCllback(self.cllback)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()


        groupBox = QGroupBox("Talimatlar")  # create groupbox

        info_instructions = QLabel("QR Kodunuzu Aşağıdaki Cihaza Okutunuz")
        info_instructions.setFont(QFont("Arial", 30, QFont.Bold))
        info_instructions.setAlignment(Qt.AlignCenter)

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

        vbox.addWidget(info_instructions)
        vbox.addLayout(hbox)

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(hbox)
        main_hbox.addLayout(vbox)
        main_hbox.addWidget(self.CameraLabel)


        groupBox.setLayout(main_hbox)  # hbox is placed in groupbox

        return groupBox

    def cargoPNR(self):  # Kargo Teslim Grup Box - Step2

        groupBox = QGroupBox("Kargo Teslim")

        info_PNRDelivery = QLabel("Kargonuzu PNR ile teslim almak için butona basınız.")
        info_PNRDelivery.setFont(QFont("Arial", 30, QFont.Bold))
        info_PNRDelivery.setAlignment(Qt.AlignCenter)

        self.PNRTextEditor = QLineEdit(self)
        self.PNRTextEditor.setPlaceholderText("PNR Kod Giriniz")
        self.PNRTextEditor.setStyleSheet("color : blue")

        PNRbutton = QPushButton("PNR Buttonu", objectName="GeneralButton")
        PNRbutton.installEventFilter(self)
        PNRbutton.setFont(QFont("Time New Roman", 20))
        PNRbutton.clicked.connect(self.PNRFinder)

        self.PNRText = QLabel("")  # success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addWidget(self.PNRTextEditor)
        vbox.addWidget(self.PNRText)
        vbox.addWidget(PNRbutton)
        vbox.addWidget(self.BackMainButton())
        vbox.addStretch()
        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def PNRFinder(self):
        if self.PNRTextEditor.text() != "":
            currernttext = self.PNRTextEditor.text()
            values = self.Finder.PNRFinder(currernttext)
            self.infoWin.showInfoWindow(values[0], values[1])
        else:
            QMessageBox.information(self, "Bilgilendirme", "PNR Numarası Girmediniz\n"
                                                           "Lütfen PNR Numarası Girip Tekrar Deneyiniz")

    def DatabaseWindow(self):  # calling database window class
        self.w_DB = Window_DB.Window_DB("İlçeler")
        self.w_DB.show()

    def DatabaseFilterWindow(self):  # calling database window class
        self.w_FDB = Window_FilterDB.Window_FilterDB()
        self.w_FDB.show()

    def Database_CreateRow(self):  # calling database CreateRow window class
        self.cr_W = CreateRow.CreateRow()
        self.cr_W.show()

    def Database_Update(self):  # Database value uptade
        # self.database.updateRow(column, U_Name, U_T_Value)
        self.tab.setCurrentWidget(self.tab4)
        U_CurrentCombo = self.U_Combo.currentText()
        U_CurrentName = self.U_Name.text()
        U_CurrentValue = self.U_T_Value.text()

        if U_CurrentCombo == "Değiştirmek istediğiniz sütunu seçiniz.":
            QMessageBox.critical(self, "Hata", "Sütun seçimi boş bırakılamaz.")
        else:
            self.database.updateRow(U_CurrentCombo, U_CurrentName, U_CurrentValue)

    def cargoTrack(self):  # Kargo teslim verme
        groupBox = QGroupBox("Kargo Teslim Verme ")

        info_PNRDelivery = QLabel("Kargoyu Teslim Vermek İçin Butona Basınız")
        info_PNRDelivery.setFont(QFont("Arial", 15, QFont.Bold))

        self.TrackTextEditor = QLineEdit(self)
        self.TrackTextEditor.setPlaceholderText("Takip Numarasını Giriniz")

        Trackbutton = QPushButton("Takip  Button", objectName="GeneralButton")
        Trackbutton.setFont(QFont("Time New Roman", 20))
        Trackbutton.clicked.connect(self.TrackingFinder)

        self.TrackText = QLabel("")  # success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addWidget(self.TrackTextEditor)
        vbox.addWidget(self.TrackText)
        vbox.addWidget(Trackbutton)
        vbox.addWidget(self.BackMainButton())
        vbox.addStretch()
        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def TrackingFinder(self):
        getTrackList = self.database.getTrackList()  # calling all Tracking num. list from Database
        # print(getTrackList)
        i = 0

        if self.TrackTextEditor.text() != "":
            for getTrack in getTrackList:  # search in database
                if int(self.TrackTextEditor.text()) == int(getTrack[0]):
                    self.TrackText.setText("Success")
                    print(int(self.TrackTextEditor.text()) == int(getTrack[0]))
                    self.InfoWindowFunc("delivery", "PNR", str(getTrack[0]))
                    i = i + 1
                    break
                else:
                    self.TrackText.setText("Failed")
                    print(getTrack[0])
                    print(int(self.TrackTextEditor.text()) == int(getTrack[0]))

            if i == 0:  # if not found give information is provided
                QMessageBox.information(self, "Bilgilendirme", "Girdiğiniz takip numarası bulunamamıştır.\n"
                                                               "Kontrol edip tekrar deneyiniz.")

        else:
            QMessageBox.information(self, "Bilgilendirme", "Takip Numarası Girmediniz.\n"
                                                           "Lütfen Bir Takip Numarası Giriniz.")

    def DeliveryWindow(self, Tracking_Num):  # calling Delivery window class with Tracking Number
        list_DeliveryWindow = self.database.getPerson_withTrackingNo(Tracking_Num)
        self.w = DeliveryWindow.DeliveryWindow(list_DeliveryWindow)
        self.w.show()

    def BarCode(self):
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

        grupbox.setLayout(vbox)
        return grupbox

    def BackMainFunction(self):
        a = self.tab.indexOf(self.tab.currentWidget())
        self.tab.setCurrentWidget(self.tab1)

        if self.tab.currentWidget() == self.tab1:
            self.tab.removeTab(a)

    def BackMainButton(self):

        self.BackButton = QPushButton("Ana Menüye Dönmek için Tıklayınız", objectName="GeneralButton")
        self.BackButton.setFont(QFont("Arial", 20))
        self.BackButton.setIcon(QIcon("Home.png"))
        self.BackButton.setIconSize(QtCore.QSize(45, 45))
        self.BackButton.clicked.connect(self.BackMainFunction)

        return self.BackButton

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

        # TAB-4 Widgets
        self.databaseAddRow = QPushButton("Add Row", objectName="GeneralButton")
        self.databaseAddRow.clicked.connect(self.Database_CreateRow)
        self.databaseButton = QPushButton("DB Table", objectName="GeneralButton")
        self.databaseButton.clicked.connect(self.DatabaseWindow)
        self.databaseUpdateRow = QPushButton("Update Row", objectName="GeneralButton")
        self.databaseUpdateRow.clicked.connect(self.Database_Update)
        self.databasefilter = QPushButton("Database Filter Window", objectName="GeneralButton")
        self.databasefilter.clicked.connect(self.DatabaseFilterWindow)

        # TAB-4 Widgets END

        # TAB-5 Widgets
        self.U_TextLabel = QLabel("")

        self.U_Combo = QComboBox(self)
        self.U_Combo.addItems(["Değiştirmek istediğiniz sütunu seçiniz.", "Takip_Numarasi", "Ad", "Soyad", "Tel_Num",
                               "Mail_adres", "Qrkod", "Pnr_Num", "Security", "Box_Location", "Cabin_Num",
                               "Cargo_Start_Time",
                               "Cargo_End_Time"])

        self.U_Name = QLineEdit()
        self.U_Name.setPlaceholderText("Verisi değiştirilmek istenin kişinin adını giriniz.")

        self.U_T_Value = QLineEdit()
        self.U_T_Value.setPlaceholderText("Yeni veriyi giriniz.")

        self.U_Button = QPushButton("Kaydet", objectName="GeneralButton")
        self.U_Button.clicked.connect(self.Database_Update)
        # TAB-5 Widgets END

        # widgets are placed
        tab1_grid.addWidget(self.cargoReceive(), 0, 0)
        tab1_grid.addWidget(self.cargoDelivery(), 0, 1)
        tab2_grid.addWidget(self.instructions(), 1, 0)
        tab2_grid.addWidget(self.cargoPNR(), 0, 0)
        tab3_grid.addWidget(self.cargoTrack(), 0, 0)
        tab3_grid.addWidget(self.BarCode(), 1, 0)
        tab4_vbox.addWidget(self.databaseAddRow)
        tab4_vbox.addWidget(self.databaseUpdateRow)
        tab4_vbox.addWidget(self.databaseButton)
        tab4_vbox.addWidget(self.databasefilter)
        tab4_vbox.addWidget(self.BackMainButton())
        tab5_vbox.addStretch()
        tab5_vbox.addWidget(self.U_TextLabel)
        tab5_vbox.addWidget(self.U_Combo)
        tab5_vbox.addWidget(self.U_Name)
        tab5_vbox.addWidget(self.U_T_Value)
        tab5_vbox.addWidget(self.U_Button)
        tab5_vbox.addWidget(self.BackMainButton())
        tab5_vbox.addStretch()

        # tab's layout setted
        self.tab1.setLayout(tab1_grid)
        self.tab2.setLayout(tab2_grid)
        self.tab3.setLayout(tab3_grid)
        self.tab4.setLayout(tab4_vbox)
        self.tab5.setLayout(tab5_vbox)

        self.tab.addTab(self.tab1, "Ana Sayfa")
        # self.tab.addTab(self.tab2, "Kargo Alma Aşaması")
        # self.tab.addTab(self.tab3, "Kargo Verme Aşaması")
        # self.tab.addTab(self.tab4, "DataBase İşlemleri")
        # self.tab.addTab(self.tab5, "DB Güncelleme")

        mainLayout.addWidget(self.tab)

        self.setLayout(mainLayout)

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    oldBarcode = 0

    def setCllback(self, cllbck):
        print("thread setcllback func girildi")
        self.cllbck = cllbck

    def run(self):
        counter = 0
        self.cap = cv2.VideoCapture(0)
        self.threadactive = True

        while (True):
            ret, frame = self.cap.read()
            if self.cap.read() is None:
                break
            barcodes = pyzbar.decode(frame)
            found = set()

            for barcode in barcodes:
                counter = counter + 1
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                print(counter, barcodeData)
                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode   q to disk and update the set
                if barcodeData not in found:
                    if counter % 10 == 0 :
                        self.cllbck(barcodeData)


            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)




app = QApplication([])
app.setStyleSheet(StyleSheet)
mainwindow = MainWindow()
mainwindow.show()
app.exec_()
