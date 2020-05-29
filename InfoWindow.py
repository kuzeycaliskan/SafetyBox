from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import CabinNum_Window
import Mail
import time


class InfoWindow(QWidget):  # <===
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)
        self.nameLabel = QLabel()
        self.surnameLabel = QLabel()
        self.phoneLabel = QLabel()
        self.mailLabel = QLabel()
        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.surnameLabel)
        vbox.addWidget(self.phoneLabel)
        vbox.addWidget(self.mailLabel)
        vbox.addWidget(confirmbutton)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # pencerenin önde kalmasını sağlıyor
        self.show()
        self.setHidden(True)

    def receiver_info(self, knowledge):
        self.nameLabel.setText("Ad: " + knowledge[0][0])
        self.surnameLabel.setText("Soyad: " + knowledge[0][1])
        self.phoneLabel.setText("Telefon: " + str(knowledge[0][2]))
        self.mailLabel.setText("Mail: " + knowledge[0][3])
        self.box_no = knowledge[0][4]

        self.receiver_ID = knowledge[0][3]

    def delivery_info(self, knowledge):
        self.nameLabel.setText("Ad: " + knowledge[0][0])
        self.surnameLabel.setText("Soyad: " + knowledge[0][1])
        self.phoneLabel.setText("Telefon: " + str(knowledge[0][2]))
        self.mailLabel.setText("Mail: " + knowledge[0][3])
        self.box_no = knowledge[0][4]
        print('PRINTED INFO')
        self.receiver_ID = knowledge[0][3]

    def setInfoLabels(self, knowledge):
        self.nameLabel.setText("Ad: " + knowledge[0][0])
        self.surnameLabel.setText("Soyad: " + knowledge[0][1])
        self.phoneLabel.setText("Telefon: " + str(knowledge[0][2]))
        self.mailLabel.setText("Mail: " + knowledge[0][3])
        self.box_no = knowledge[0][4]
        print('PRINTED INFO')
        self.receiver_ID = knowledge[0][3]

    def showInfoWindow(self, info_type, DB_RowValue, pnr_or_tracking):
        self.pnr_or_tracking = pnr_or_tracking
        self.DB_RowValue = DB_RowValue
        self.info_type = info_type
        if info_type == "receiver":
            print("InfoWindowClass", DB_RowValue)
            print(DB_RowValue[0][0])
            print(DB_RowValue[0][1])
            print(DB_RowValue[0][2])
            print(DB_RowValue[0][3])
            print(DB_RowValue[0][4])
            self.receiver_info(DB_RowValue)
        elif info_type == "delivery":
            print("Shouldn't write this sentence", DB_RowValue)
            print(DB_RowValue[0][0])
            print(DB_RowValue[0][1])
            print(DB_RowValue[0][2])
            print(DB_RowValue[0][3])
            self.delivery_info(DB_RowValue)

        elif info_type == "Locker":
            print("Locker showInfoWindow", DB_RowValue)
            print(DB_RowValue[0][0])
            print(DB_RowValue[0][1])
            print(DB_RowValue[0][2])
            print(DB_RowValue[0][3])
            self.setInfoLabels(DB_RowValue)

        self.setHidden(False)

    def closeInfoWindow(self):
        self.setHidden(True)

    def setCllBack_TakePicture(self, cllback):  # callback function for take picture from main.py
        self.cllback = cllback

    def confirmFunction(self):
        self.closeInfoWindow()

        if self.info_type == "receiver":
            # send mail and take picture process
            current_time = time.strftime("%d_%m_%Y_%H.%M.%S")  # creating current time value
            receiver_ID = self.receiver_ID.split("@")
            self.cllback(receiver_ID[0], current_time)
            values_PNR = [self.DB_RowValue[0][3], self.DB_RowValue[0][0], self.DB_RowValue[0][1],
                          self.pnr_or_tracking, current_time]  # creating values for mail
            Mail.SendMail("Receiving_Cargo", values_PNR)

        elif self.info_type == "Locker":
            # send mail and take picture process
            current_time = time.strftime("%d_%m_%Y_%H.%M.%S")  # creating current time value
            receiver_ID = self.receiver_ID.split("@")
            self.cllback(receiver_ID[0], current_time)
            values_PNR = [self.DB_RowValue[0][3], self.DB_RowValue[0][0], self.DB_RowValue[0][1],
                          self.pnr_or_tracking, current_time]  # creating values for mail
            Mail.SendMail("Receiving_Locker", values_PNR)

        self.w = CabinNum_Window.CabinNum_Window(self.info_type, self.box_no)
        self.w.show()
