from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import CabinNum_Window


class InfoWindow(QWidget):  # <===
    def __init__(self):
        super().__init__()

        vbox = QVBoxLayout()
        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)
        # self.nameLabel = QLabel("Ad: " + knowledge[0][0])
        # self.surnameLabel = QLabel("Soyad: " + knowledge[0][1])
        # self.phoneLabel = QLabel("Telefon: " + str(knowledge[0][2]))
        # self.mailLabel = QLabel("Mail: " + knowledge[0][3])
        # self.box_no = knowledge[0][4]
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

        self.setWindowFlag(Qt.WindowStaysOnTopHint)#pencerenin önde kalmasını sağlıyor
        self.show()
        self.setHidden(True)



    def receiver_info(self, knowledge):
        self.nameLabel.setText("Ad: " + knowledge[0][0])
        self.surnameLabel.setText("Soyad: " + knowledge[0][1])
        self.phoneLabel.setText("Telefon: " + str(knowledge[0][2]))
        self.mailLabel.setText("Mail: " + knowledge[0][3])
        self.box_no = knowledge[0][4]

    def delivery_info(self, knowledge):
        self.nameLabel.setText("Ad: " + knowledge[0][0])
        self.surnameLabel.setText("Soyad: " + knowledge[0][1])
        self.phoneLabel.setText("Telefon: " + str(knowledge[0][2]))
        self.mailLabel.setText("Mail: " + knowledge[0][3])
        print('PRINTED INFO')

    def showInfoWindow(self, info_type, DB_RowValue):
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
            self.delivery_info(DB_RowValue)

        self.setHidden(False)

    def closeInfoWindow(self):
        self.setHidden(True)

    def confirmFunction(self):
        self.closeInfoWindow()
        # self.w = CabinNum_Window.CabinNum_Window(self.box_no)
        # self.w.show()


