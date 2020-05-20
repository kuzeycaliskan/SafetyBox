from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class adminPassWindow(QWidget):  # <===
    def __init__(self):
        super().__init__()
        #self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Admin")

        with open("home/pi/Desktop/SafetyBox/admin.txt", "r") as DB_pm:
            data_admin = DB_pm.read().splitlines()

        self.username_txt = data_admin[0]
        self.password_txt = data_admin[1]

        print(data_admin)



        self.mainWindow()
        self.show()


    def mainWindow(self):

        text = QLabel("Ayarlar Menüsü Şifre Ekranı")
        # text.setFont(QFont("Arial", 12, QFont.Black))
        text.setStyleSheet("font: 12pt;")
        username_text = QLabel("Username: ")
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Kullancı adı")

        username_hbox = QHBoxLayout()
        username_hbox.addWidget(username_text)
        username_hbox.addStretch(1)
        username_hbox.addWidget(self.username)

        password_text = QLabel("Password: ")
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Şifre")
        self.password.setEchoMode(QLineEdit.Password)

        password_hbox = QHBoxLayout()
        password_hbox.addWidget(password_text)
        password_hbox.addStretch(1)
        password_hbox.addWidget(self.password)

        self.confirm = QPushButton("Ok", objectName="SmallButton")
        self.confirm.setFixedSize(60, 30)
        self.confirm.clicked.connect(self.result)


        vbox = QVBoxLayout()
        vbox.addWidget(text)
        vbox.addStretch(1)
        vbox.addLayout(username_hbox)
        vbox.addLayout(password_hbox)
        vbox.addStretch(1)
        vbox.addWidget(self.confirm, alignment=QtCore.Qt.AlignHCenter)
        vbox.setContentsMargins(20, 10, 20, 10)


        self.setLayout(vbox)

        self.setHidden(False)

    def setCllback_Admin(self, cllback):
        self.cllback = cllback

    def result(self):
        if self.username.text() == self.username_txt and self.password.text() == self.password_txt:
            print("access confirmed")
            self.cllback(True)

        else:
            print("access denied")
            self.cllback(False)
