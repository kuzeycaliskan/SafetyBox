from PyQt5.QtWidgets import *
import main_DB

class Window_DB(QWidget):

    def __init__(self):
        super().__init__()


        self.setGeometry(100, 100, 1080, 640)  # 50,50 parametresi pencerede nerede baslayacigini belirler
        self.setWindowTitle("PyQt5 App")
        self.database = main_DB.main_DB()


        # print("window_DB Class Test")
        self.layout_DB()
        self.show()

    def table_DB(self,table_name):

        self.table = QTableWidget()

        if table_name == "İlçeler":
            read_db = self.database.getCounties()

            rowCount = self.database.getRowCount_Counties()
            self.table.setRowCount(rowCount) #database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(3) #database sutun sayisi duzenleme
            self.table.setHorizontalHeaderItem(0,QTableWidgetItem("ID"))
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("İlçe Adı"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("İl Adı"))
            row = 0

            for get_DB in read_db:

                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                row = row + 1
                print(get_DB[0],get_DB[1], get_DB[2])

            return self.table

        elif table_name == "SafetyBox's":
            read_db = self.database.getSafetyBoxs()

            rowCount = self.database.getRowCount_SafetyBoxs()
            self.table.setRowCount(rowCount) #database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(4) #database sutun sayisi duzenleme
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("SafetyBox İsmi"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("SafetyBox Adres"))
            self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Kayıtlı İlçe ID"))
            row = 0
            for get_DB in read_db:

                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(get_DB[3])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3])

            return self.table

        elif table_name == "Dolaplar":
            print("Checked for Access Dolaplar Case")
            read_db = self.database.getAllBoxs()

            rowCount = self.database.getRowCount_AllBoxs()
            self.table.setRowCount(rowCount) #database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(5) #database sutun sayisi duzenleme
            self.table.setHorizontalHeaderItem(0,QTableWidgetItem("ID"))
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Dolap No"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Boyut"))
            self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Boş Mu?"))
            self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Kayıtlı SafetyBox ID"))
            row = 0
            for get_DB in read_db:

                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(get_DB[3])))
                self.table.setItem(row, 4, QTableWidgetItem(str(get_DB[4])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4])

            return self.table

        elif table_name == "Kargolar":
            read_db = self.database.getCargoes()

            rowCount = self.database.getRowCount_Cargoes()
            self.table.setRowCount(rowCount) #database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(5) #database sutun sayisi duzenleme
            self.table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Takip No"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("QR Kod"))
            self.table.setHorizontalHeaderItem(3, QTableWidgetItem("PNR No"))
            self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Ek Güvenlik"))
            self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Kayıtlı Dolap ID"))
            self.table.setHorizontalHeaderItem(6, QTableWidgetItem("Kayıtlı Kimlik ID"))
            self.table.setHorizontalHeaderItem(7, QTableWidgetItem("Kargo Oluşturma Tarihi"))
            self.table.setHorizontalHeaderItem(8, QTableWidgetItem("Kargo Teslim Tarihi"))
            self.table.setHorizontalHeaderItem(9, QTableWidgetItem("Teslim edildi mi?"))
            row = 0
            for get_DB in read_db:

                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(get_DB[3])))
                self.table.setItem(row, 4, QTableWidgetItem(str(get_DB[4])))
                self.table.setItem(row, 5, QTableWidgetItem(str(get_DB[5])))
                self.table.setItem(row, 6, QTableWidgetItem(str(get_DB[6])))
                self.table.setItem(row, 7, QTableWidgetItem(str(get_DB[7])))
                self.table.setItem(row, 8, QTableWidgetItem(str(get_DB[8])))
                self.table.setItem(row, 9, QTableWidgetItem(str(get_DB[9])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4], get_DB[5], get_DB[6], get_DB[7], get_DB[8], get_DB[9])

            return self.table

        elif table_name == "Kimlikler":
            read_db = self.database.getIdentities()

            rowCount = self.database.getRowCount_Identities()
            print("Kimlikler satır sayısı: ",rowCount)

            self.table.setRowCount(rowCount) #database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(5) #database sutun sayisi duzenleme
            self.table.setHorizontalHeaderLabels(["ID", "İsim", "Soyadı", "Telefon No", "Mail Adresi"])
            self.table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
            self.table.setHorizontalHeaderItem(1, QTableWidgetItem("İsim"))
            self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Soyadı"))
            self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Telefon No"))
            self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Mail Adresi"))
            row = 0
            for get_DB in read_db:

                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(get_DB[3])))
                self.table.setItem(row, 4, QTableWidgetItem(str(get_DB[4])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4])

            return self.table


    def layout_DB(self):
        self.gridlayout = QGridLayout()

        vbox = QVBoxLayout()

        self.combobox = QComboBox(self, )
        self.combobox.addItems(["İlçeler", "SafetyBox's", "Dolaplar", "Kargolar", "Kimlikler"])
        self.combobox.setCurrentText("SafetyBox")
        print("HOW MANY TIMES HAVE I USED THIS FUNCTION?")
        self.button = QPushButton("Table")
        self.button.clicked.connect(self.update_Table)

        vbox.addWidget(self.combobox)
        vbox.addWidget(self.button)

        self.gridlayout.addLayout(vbox, 0, 0)
        self.gridlayout.addWidget(self.table_DB(self.combobox.currentText()), 0, 1)
        self.setLayout(self.gridlayout)


    def update_Table(self):
        table_name = self.combobox.currentText()
        print(table_name)
        self.gridlayout.addWidget(self.table_DB(table_name), 0, 1)

        self.setLayout(self.gridlayout)







