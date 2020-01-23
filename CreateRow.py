from PyQt5.QtWidgets import *
import main_DB

class CreateRow(QWidget):  # <===
    def __init__(self):
        super().__init__()
        #self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Yeni Kişi Oluştur")
        self.database = main_DB.main_DB()


        self.createrow()
        self.show()

    def createrow(self):

        self.textbox_tracking = QLineEdit()
        self.textbox_tracking.setPlaceholderText("Takip No Giriniz (max. 12 haneli)")
        self.textbox_name = QLineEdit()
        self.textbox_name.setPlaceholderText("Ad Giriniz")
        self.textbox_surname = QLineEdit()
        self.textbox_surname.setPlaceholderText("Soyad Giriniz")
        self.textbox_tel_no = QLineEdit()
        self.textbox_tel_no.setPlaceholderText("Telefon Numarası Giriniz")
        self.textbox_mail = QLineEdit()
        self.textbox_mail.setPlaceholderText("Mail adresinizi giriniz")
        self.textbox_qrkod = QLineEdit()
        self.textbox_qrkod.setPlaceholderText("30 haneli QRKod giriniz")
        self.textbox_PNR_no = QLineEdit()
        self.textbox_PNR_no.setPlaceholderText("PNR No giriniz")
        self.textbox_securtiy = QLineEdit()
        self.textbox_securtiy.setPlaceholderText("Ek güvenlik istiyor musun? [Evet = 1 / Hayır = 0]")
        self.textbox_cabin_no = QLineEdit()
        self.textbox_cabin_no.setPlaceholderText("Dolap No Giriniz")
        self.textbox_box_loca = QLineEdit()
        self.textbox_box_loca.setPlaceholderText("SefetyBox Lokasyonunu Giriniz")
        self.textbox_cargo_ST = QLineEdit()
        self.textbox_cargo_ST.setPlaceholderText("Kargo bırakıldığı tarihi giriniz. (YYYY-MM-DD HH:MM:SS)")
        self.textbox_cargo_ET = QLineEdit()
        self.textbox_cargo_ET.setPlaceholderText("Kargo alındığı tarihi giriniz. (YYYY-MM-DD HH:MM:SS)")
        self.title_W = QLabel()
        self.title_W.setText("YENİ KİŞİ EKLE")

        savebutton = QPushButton("Kaydet")
        savebutton.clicked.connect(self.saveFunction)

        vbox = QVBoxLayout()
        # vbox.addWidget(self.title_W)
        vbox.addWidget(self.textbox_tracking)
        vbox.addWidget(self.textbox_name)
        vbox.addWidget(self.textbox_surname)
        vbox.addWidget(self.textbox_tel_no)
        vbox.addWidget(self.textbox_mail)
        vbox.addWidget(self.textbox_qrkod)
        vbox.addWidget(self.textbox_PNR_no)
        vbox.addWidget(self.textbox_securtiy)
        vbox.addWidget(self.textbox_box_loca)
        vbox.addWidget(self.textbox_cabin_no)
        vbox.addWidget(self.textbox_cargo_ST)
        vbox.addWidget(self.textbox_cargo_ET)
        vbox.addWidget(savebutton)

        vbox.setContentsMargins(40,25,40,40)
        self.setLayout(vbox)



    def saveFunction(self):
        newrowlist = ["none"] * 12

        newrowlist[0] = self.textbox_tracking.text()
        newrowlist[1] = self.textbox_name.text()
        newrowlist[2] = self.textbox_surname.text()
        newrowlist[3] = self.textbox_tel_no.text()
        newrowlist[4] = self.textbox_mail.text()
        newrowlist[5] = self.textbox_qrkod.text()
        newrowlist[6] = self.textbox_PNR_no.text()
        newrowlist[7] = self.textbox_securtiy.text()
        newrowlist[8] = self.textbox_box_loca.text()
        newrowlist[9] = self.textbox_cabin_no.text()
        newrowlist[10] = self.textbox_cargo_ST.text()
        newrowlist[11] = self.textbox_cargo_ET.text()

        self.database.createRow(newrowlist)

        QMessageBox.information(self, "Bilgilendirme", "Kişiniz başarı ile kaydedilmiştir.")
        self.hide()








