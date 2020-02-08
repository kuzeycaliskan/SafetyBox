from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.Qt import *
import InfoWindow
import main_DB
import Window_DB
import CreateRow
import DeliveryWindow

#GUI Button Shape
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
'''

class Window(QWidget):
    def __init__(self):
        super().__init__()  # QWidget fonskiyonlarını kullanabilmek icin

        self.setGeometry(0, 0, 1080,732) #window size
        self.setWindowTitle("Safety Box")  #window title
        self.database = main_DB.main_DB()  # calling database class

        # self.database.deleteTable()
        # self.database.createTable()
        # self.database.addRow_default()
        # self.database.getDB_All()


        # self.database.select_DB.execute('SELECT COUNT(*) FROM cargosystem')
        # self.readRowCount = self.database.select_DB.fetchone()
        # print(int(self.readRowCount[0]))

        self.tabs() #initialize tabs
        self.show()


    def cargoRecieve(self): #Kargo Teslim Alma - Step1

        groupBox = QGroupBox("Kargo Teslim Alma")

        vbox = QVBoxLayout()

        deliveringButton = QPushButton("Kargo Teslim\nAlma", objectName="ReceivingButton") #button initialize
        deliveringButton.installEventFilter(self)
        deliveringButton.setFixedSize(deliveringButton.width(),deliveringButton.height()) #button size maximize
        deliveringButton.setFont(QFont("Arial", 50, QFont.Bold)) #button font
        # deliveringButton.setVisible(False)
        deliveringButton.clicked.connect(self.deliveringFunction)
        # unclicked unvisible
        #print(groupBox.width())
        #vbox.setContentsMargins((groupBox.width()-deliveringButton.width()),0,0,0)
        vbox.addWidget(deliveringButton)
        groupBox.setLayout(vbox)

        return groupBox


    def cargoDelivery(self): #Kargo Teslim Etme - Step1
        groupBox = QGroupBox("Kargo Teslim Etme")

        vbox = QVBoxLayout()
        receivingButton = QPushButton("Kargo Teslim\nEtme", objectName="DeliveringButton") #button initialize
        receivingButton.setFixedSize(receivingButton.width(), receivingButton.height()) #button size maximize
        receivingButton.setFont(QFont("Arial", 50, QFont.Bold)) #button font
        receivingButton.clicked.connect(self.receivingFunction)
        vbox.addWidget(receivingButton)
        groupBox.setLayout(vbox)

        return groupBox

    def deliveringFunction(self): #main screen button function
        self.tab.setCurrentWidget(self.tab2) #pass tab-2 when clicked button

    def receivingFunction(self): #main screen button function
        self.tab.setCurrentWidget(self.tab5) #pass tab-5 when clicked button

    def instructions(self): #Talimatlar Group Box - Step2

        groupBox = QGroupBox("Talimatlar") #create groupbox

        info_instructions = QLabel("QR Kodunuzu Aşağıdaki Cihaza Okutunuz")
        info_instructions.setFont(QFont("Arial", 30, QFont.Bold))
        info_instructions.setAlignment(Qt.AlignCenter)

        image1 = QLabel(self) #instruction picture one
        image1.setPixmap(QPixmap("qrkod1.jpg"))

        image2 = QLabel(self) #instruction picture two
        image2.setPixmap(QPixmap("qrkod1.jpg"))

        image3 = QLabel(self) #instruction picture three
        image3.setPixmap(QPixmap("qrkod1.jpg"))


        hbox = QHBoxLayout() #create layout

        hbox.addStretch()
        hbox.addWidget(image1)
        hbox.addWidget(image2)
        hbox.addWidget(image3)
        hbox.addStretch()

        vbox = QVBoxLayout()

        vbox.addWidget(info_instructions)
        vbox.addLayout(hbox)

        groupBox.setLayout(vbox) #hbox is placed in groupbox


        return groupBox

    def cargoPNR(self): #Kargo Teslim Grup Box - Step2

        groupBox = QGroupBox("Kargo Teslim")

        info_PNRDelivery = QLabel("Kargonuzu PNR ile teslim almak için butona basınız.")
        info_PNRDelivery.setFont(QFont("Arial", 30, QFont.Bold))
        info_PNRDelivery.setAlignment(Qt.AlignCenter)

        self.PNRTextEditor = QLineEdit(self)
        self.PNRTextEditor.setPlaceholderText("PNR Kod Giriniz")
        self.PNRTextEditor.setStyleSheet("color : blue")


        PNRbutton = QPushButton("PNR Button")
        PNRbutton.setStyleSheet("background : gray; color: white")
        PNRbutton.clicked.connect(self.PNRFinder)


        self.PNRText = QLabel("") #success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addWidget(self.PNRTextEditor)
        vbox.addWidget(self.PNRText)
        vbox.addWidget(PNRbutton)
        vbox.addStretch()
        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def PNRFinder(self): #find person from PNR Number
        getPNRList = self.database.getPNRList() #calling all PNR list from Database
        # print(int(self.PNRTextEditor.text()))
        i = 0

        for getPNR in getPNRList: #search in database
            if  int(self.PNRTextEditor.text()) == int(getPNR[0]): #if found open info window
                self.PNRText.setText("Success")
                print(int(self.PNRTextEditor.text()) == int(getPNR[0]))
                self.InfoWindow(str(getPNR[0]))
                i = i+1
                break
            else:
                self.PNRText.setText("Failed")
                print(getPNR[0])
                print(int(self.PNRTextEditor.text()) == int(getPNR[0]))

        if i == 0: #if not found give information is provided
            QMessageBox.information(self, "Bilgilendirme", "Aradığınız kişi bulunamamıştır.\n "
                                                           "Kontrol edip tekrar deneyiniz.")

    def InfoWindow(self, PNR_Num): #calling info window class with PNR Number
        list_InfoWindow = self.database.getInfo_IW(PNR_Num)
        self.w = InfoWindow.InfoWindow(list_InfoWindow)
        self.w.show()

    def DatabaseWindow(self): #calling database window class
        # for i in self.read_DB:
        #     print("check")
        #     print(i)
        self.w_DB = Window_DB.Window_DB()
        self.w_DB.show()
        # self.database.getDB_All()

    def Database_CreateRow(self): #calling database CreateRow window class
        self.cr_W = CreateRow.CreateRow()
        self.cr_W.show()

    def Database_Update(self): #Database value uptade
        # self.database.updateRow(column, U_Name, U_T_Value)
        self.tab.setCurrentWidget(self.tab4)
        U_CurrentCombo = self.U_Combo.currentText()
        U_CurrentName = self.U_Name.text()
        U_CurrentValue = self.U_T_Value.text()

        if U_CurrentCombo == "Değiştirmek istediğiniz sütunu seçiniz.":
            QMessageBox.critical(self, "Hata", "Sütun seçimi boş bırakılamaz.")
        else:
            self.database.updateRow(U_CurrentCombo, U_CurrentName, U_CurrentValue)

    def cargoTrack(self): #Kargo teslim verme
        groupBox = QGroupBox("Kargo Teslim Verme ")

        info_PNRDelivery = QLabel("Kargoyu Teslim Vermek İçin Butona Basınız")
        info_PNRDelivery.setFont(QFont("Arial", 15, QFont.Bold))

        self.TrackTextEditor = QLineEdit(self)
        self.TrackTextEditor.setPlaceholderText("Takip Numarasını Giriniz")

        Trackbutton = QPushButton("Takip  Button")
        Trackbutton.clicked.connect(self.TrackingFinder)

        self.TrackText = QLabel("")  # success failed text

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(info_PNRDelivery)
        vbox.addWidget(self.TrackTextEditor)
        vbox.addWidget(self.TrackText)
        vbox.addWidget(Trackbutton)
        vbox.addStretch()
        groupBox.size().setHeight(320)
        groupBox.setLayout(vbox)

        return groupBox

    def TrackingFinder(self):
        getTrackList = self.database.getTrackList()  # calling all Tracking num. list from Database
        # print(getTrackList)
        i = 0

        for getTrack in getTrackList:  # search in database
            if int(self.TrackTextEditor.text()) == int(getTrack[0]):
                self.TrackText.setText("Success")
                print(int(self.TrackTextEditor.text()) == int(getTrack[0]))
                self.DeliveryWindow(str(getTrack[0]))
                i = i + 1
                break
            else:
                self.TrackText.setText("Failed")
                print(getTrack[0])
                print(int(self.TrackTextEditor.text()) == int(getTrack[0]))

        if i == 0:  # if not found give information is provided
            QMessageBox.information(self, "Bilgilendirme", "Girdiğiniz takip numarası bulunamamıştır.\n"
                                                           "Kontrol edip tekrar deneyiniz.")

    def DeliveryWindow(self, Tracking_Num):  # calling Delivery window class with Tracking Number
        list_DeliveryWindow = self.database.getTracking_Num_DW(Tracking_Num)
        self.w = DeliveryWindow.DeliveryWindow(list_DeliveryWindow)
        self.w.show()

    def tabs(self): #tabs function

        mainLayout = QVBoxLayout() #tab's Main Layout

        self.tab = QTabWidget() #create Tab

        self.tab1 = QWidget() #create tab-1 (step-1)
        self.tab2 = QWidget() #create tab-2 (step-2)
        self.tab3 = QWidget() #create tab-3 (step-3)
        self.tab4 = QWidget() #create tab-4 (step-4)
        self.tab5 = QWidget() #create tab-5 (step-5)

        tab1_grid = QGridLayout() #tab-1's layout
        tab2_grid = QGridLayout() #tab-2's layout
        tab3_vbox = QVBoxLayout() #tab-3's layout
        tab4_vbox = QVBoxLayout() #tab-4's layout
        tab5_grid = QGridLayout() #tab-5's layout

        #TAB-3 Widgets
        self.databaseAddRow = QPushButton("Add Row")
        self.databaseAddRow.clicked.connect(self.Database_CreateRow)
        self.databaseButton = QPushButton("DB Table")
        self.databaseButton.clicked.connect(self.DatabaseWindow)
        self.databaseUpdateRow = QPushButton("Update Row")
        self.databaseUpdateRow.clicked.connect(self.Database_Update)
        #TAB-3 Widgets END

        #TAB-4 Widgets
        self.U_TextLabel = QLabel("")

        self.U_Combo = QComboBox(self)
        self.U_Combo.addItems(["Değiştirmek istediğiniz sütunu seçiniz.","Takip_Numarasi","Ad","Soyad","Tel_Num",
                               "Mail_adres","Qrkod","Pnr_Num","Security","Box_Location","Cabin_Num","Cargo_Start_Time",
                               "Cargo_End_Time"])

        self.U_Name = QLineEdit()
        self.U_Name.setPlaceholderText("Verisi değiştirilmek istenin kişinin adını giriniz.")


        self.U_T_Value = QLineEdit()
        self.U_T_Value.setPlaceholderText("Yeni veriyi giriniz.")


        self.U_Button = QPushButton("Kaydet")
        self.U_Button.clicked.connect(self.Database_Update)
        #TAB-4 Widgets END

        #widgets are placed
        tab1_grid.addWidget(self.cargoRecieve(), 0, 0)
        tab1_grid.addWidget(self.cargoDelivery(), 0, 1)
        tab2_grid.addWidget(self.instructions(), 1, 0)
        tab2_grid.addWidget(self.cargoPNR(), 0, 0)
        tab3_vbox.addWidget(self.databaseAddRow)
        tab3_vbox.addWidget(self.databaseUpdateRow)
        tab3_vbox.addWidget(self.databaseButton)
        tab4_vbox.addStretch()
        tab4_vbox.addWidget(self.U_TextLabel)
        tab4_vbox.addWidget(self.U_Combo)
        tab4_vbox.addWidget(self.U_Name)
        tab4_vbox.addWidget(self.U_T_Value)
        tab4_vbox.addWidget(self.U_Button)
        tab4_vbox.addStretch()
        tab5_grid.addWidget(self.cargoTrack())

        #tab's layout setted
        self.tab1.setLayout(tab1_grid)
        self.tab2.setLayout(tab2_grid)
        self.tab3.setLayout(tab3_vbox)
        self.tab4.setLayout(tab4_vbox)
        self.tab5.setLayout(tab5_grid)

        self.tab.addTab(self.tab1, "Ana Sayfa")
        self.tab.addTab(self.tab2, "Kargo Alma Aşaması")
        self.tab.addTab(self.tab3, "DataBase İşlemleri")
        self.tab.addTab(self.tab4, "DB Güncelleme")
        self.tab.addTab(self.tab5, "Kargo Verme Aşaması")




        mainLayout.addWidget(self.tab)

        self.setLayout(mainLayout)



app = QApplication([])
app.setStyleSheet(StyleSheet)
window = Window()
window.show()
app.exec_()