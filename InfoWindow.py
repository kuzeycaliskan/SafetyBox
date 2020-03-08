from PyQt5.QtWidgets import *
import CabinNum_Window


class InfoWindow(QWidget):  # <===
    def __init__(self, info_type, DB_RowValue):
        super().__init__()
        #self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Kullanıcı Bilgileri")


        if info_type == "receiver":
            print("InfoWindowClass", DB_RowValue)
            print(type(DB_RowValue[0][0]))
            print(type(DB_RowValue[0][1]))
            print(type(DB_RowValue[0][2]))
            print(type(DB_RowValue[0][3]))
            print(type(DB_RowValue[0][4]))
            self.receiver_info(DB_RowValue)
        elif info_type == "delivery":
            print("InfoWindowClass", DB_RowValue)
            self.delivery_info(DB_RowValue)

        self.show()


    def receiver_info(self, knowledge):
        vbox = QVBoxLayout()

        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)
        self.nameLabel = QLabel("Ad: " + knowledge[0][0])
        self.surnameLabel = QLabel("Soyad: " + knowledge[0][1])
        self.phoneLabel = QLabel("Telefon: " + str(knowledge[0][2]))
        self.mailLabel = QLabel("Mail: " + knowledge[0][3])
        self.box_no = knowledge[0][4]
        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.surnameLabel)
        vbox.addWidget(self.phoneLabel)
        vbox.addWidget(self.mailLabel)
        vbox.addWidget(confirmbutton)
        vbox.addStretch()

        self.setLayout(vbox)
        print("Label Kontrol")

    def delivery_info(self, knowledge):

        vbox = QVBoxLayout()

        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)
        self.nameLabel = QLabel("Ad: " + knowledge[0][0])
        self.surnameLabel = QLabel("Soyad: " + knowledge[0][1])
        self.phoneLabel = QLabel("Telefon: " + str(knowledge[0][2]))
        self.mailLabel = QLabel("Mail: " + knowledge[0][3])

        vbox.addWidget(self.nameLabel)
        vbox.addWidget(self.surnameLabel)
        vbox.addWidget(self.phoneLabel)
        vbox.addWidget(self.mailLabel)
        vbox.addWidget(confirmbutton)
        vbox.addStretch()

        self.setLayout(vbox)

    def confirmFunction(self):
        self.close()
        self.w = CabinNum_Window.CabinNum_Window(self.box_no)
        self.w.show()


