from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import RP4_GPIO

class CabinNum_Window(QWidget):  # <===
    def __init__(self, info_type, Cabin_Num):
        super().__init__()
        #self.setGeometry(0, 0, 500, 250)
        self.setWindowTitle("Kabin Numarası")
        self.Cabin_Num = Cabin_Num
        self.info_type = info_type

        self.confirmButton()
        self.show()

    def confirmButton(self):

        vbox = QVBoxLayout()

        confirmbutton = QPushButton("Onayla")
        confirmbutton.clicked.connect(self.confirmFunction)
        Cabin_Num_Text = QLabel(str(self.Cabin_Num), self)
        Cabin_Num_Text.setFont(QFont("Arial", 50, QFont.Bold))
        Cabin_Num_Text.setAlignment(Qt.AlignCenter)
        self.information_Text = QLabel()
        if self.info_type == "receiver":
            self.information_Text.setText("Numaralı Dolaptan\nKargonuzu Alabilirsiniz.")
        elif self.info_type == "delivery":
            self.information_Text.setText("Numaralı Dolaba\nKargoyu Bırakınız.")
        self.information_Text.setFont(QFont("Arial", 25, QFont.Bold))
        self.information_Text.setAlignment(Qt.AlignCenter)

        vbox.addWidget(Cabin_Num_Text)
        vbox.addWidget(self.information_Text)
        vbox.addWidget(confirmbutton)
        vbox.addStretch()

        self.setLayout(vbox)

    def confirmFunction(self):
        self.close()
        print("cabin_num test", self.Cabin_Num)
        # RP4_GPIO.RP4_GPIO(self.Cabin_Num)
