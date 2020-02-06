from PyQt5.QtGui import QFont
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import RP4_GPIO

class CabinNum_Window(QWidget):  # <===
    def __init__(self, Cabin_Num):
        super().__init__()
        #self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Kabin Numarası")
        self.Cabin_Num = Cabin_Num

        self.confirmButton()
        self.show()

    def confirmButton(self):

        vbox = QVBoxLayout()

        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)
        Cabin_Num_Text = QLabel(str(self.Cabin_Num), self)
        Cabin_Num_Text.setFont(QFont("Arial",50,QFont.Bold))
        Cabin_Num_Text.setAlignment(Qt.AlignCenter)
        information_Text = QLabel("Numaralı Dolaptan\nKargonuzu Alabilirsiniz.")
        information_Text.setFont(QFont("Arial", 25, QFont.Bold))
        information_Text.setAlignment(Qt.AlignCenter)

        vbox.addWidget(Cabin_Num_Text)
        vbox.addWidget(information_Text)
        vbox.addWidget(confirmbutton)
        vbox.addStretch()

        self.setLayout(vbox)

    def confirmFunction(self):
        self.hide()
        RP4_GPIO.RP4_GPIO(self.Cabin_Num)


