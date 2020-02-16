from PyQt5.QtWidgets import *

class DeliveryWindow(QWidget):  # <===
    def __init__(self, DB_RowValue):
        super().__init__()
        #self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Kargo Teslim Etme")
        self.DBRowValue = DB_RowValue
        print(self.DBRowValue)

        self.delivery_info()
        self.show()

    def delivery_info(self):

        vbox = QVBoxLayout()

        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)
        self.nameLabel = QLabel("Ad: " + self.DBRowValue[0][0])
        self.surnameLabel = QLabel("Soyad: " + self.DBRowValue[0][1])
        self.phoneLabel = QLabel("Telefon: " + str(self.DBRowValue[0][2]))
        self.mailLabel = QLabel("Mail: " + self.DBRowValue[0][3])

        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.surnameLabel)
        vbox.addWidget(self.phoneLabel)
        vbox.addWidget(self.mailLabel)
        vbox.addWidget(confirmbutton)
        vbox.addStretch()

        self.setLayout(vbox)

    def confirmFunction(self):
        self.hide()

