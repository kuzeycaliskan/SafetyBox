from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
import main_DB


# Inheriting from QMainWindow
class Window_TWDB(QMainWindow):
    # Overriding the class constructor
    def __init__(self, table_name):
        # Be sure to call the super class method
        QMainWindow.__init__(self)

        self.setGeometry(0, 0, 1080, 732)  # window size
        self.setWindowTitle("Database Table")
        self.database = main_DB.main_DB()
        self.table_DB(table_name)

        self.show()

    def table_DB(self, table_name):
        self.table = QTableWidget(self)  # Create a table

        if table_name == "İlçeler":
            read_db = self.database.getCounties()

            rowCount = self.database.getRowCount_Counties()
            self.table.setRowCount(rowCount)  # database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(3)  # database sutun sayisi duzenleme
            self.table.setHorizontalHeaderLabels(["ID", "İlçe Adı", "İl Adı"])

            row = 0

            for get_DB in read_db:
                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2])


        elif table_name == "SafetyBox's":
            read_db = self.database.getSafetyBoxs()

            rowCount = self.database.getRowCount_SafetyBoxs()
            self.table.setRowCount(rowCount)  # database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(4)  # database sutun sayisi duzenleme
            self.table.setHorizontalHeaderLabels(["ID", "SafetyBox İsmi", "SafetyBox Adres", "Kayıtlı İlçe ID"])

            row = 0
            for get_DB in read_db:
                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(get_DB[3])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3])


        elif table_name == "Dolaplar":
            print("Checked for Access Dolaplar Case")
            read_db = self.database.getAllBoxs()

            rowCount = self.database.getRowCount_AllBoxs()
            self.table.setRowCount(rowCount)  # database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(5)  # database sutun sayisi duzenleme
            self.table.setHorizontalHeaderLabels(["ID", "Dolap No", "Boyut", "Boş Mu?", "Kayıtlı SafetyBox ID"])

            row = 0
            for get_DB in read_db:
                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(get_DB[3])))
                self.table.setItem(row, 4, QTableWidgetItem(str(get_DB[4])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4])


        elif table_name == "Kargolar":
            read_db = self.database.getCargoes()

            rowCount = self.database.getRowCount_Cargoes()
            self.table.setRowCount(rowCount)  # database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(10)  # database sutun sayisi duzenleme
            self.table.setHorizontalHeaderLabels(["ID", "Takip No", "QR Kod", "PNR No", "Ek Güvenlik",
                                                  "Kayıtlı Dolap ID", "Kayıtlı Kimlik ID", "Kargo Oluşturma Tarihi",
                                                  "Kargo Teslim Tarihi", "Teslim edildi mi?"])

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
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4], get_DB[5], get_DB[6], get_DB[7], get_DB[8],
                      get_DB[9])


        elif table_name == "Kimlikler":
            read_db = self.database.getIdentities()

            rowCount = self.database.getRowCount_Identities()


            self.table.setRowCount(rowCount)  # database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(5)  # database sutun sayisi duzenleme
            self.table.setHorizontalHeaderLabels(["ID", "İsim", "Soyisim", "Telefon No", "Mail Adresi"])

            row = 0
            for get_DB in read_db:
                self.table.setItem(row, 0, QTableWidgetItem(str(get_DB[0])))
                self.table.setItem(row, 1, QTableWidgetItem(str(get_DB[1])))
                self.table.setItem(row, 2, QTableWidgetItem(str(get_DB[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(get_DB[3])))
                self.table.setItem(row, 4, QTableWidgetItem(str(get_DB[4])))
                row = row + 1
                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4])

        elif table_name == "Detaylı Tablo":
            read_db = self.database.getDB_All()

            rowCount = self.database.getRowCount_Cargoes()

            self.table.setRowCount(rowCount)  # database satir sayisi duzenleme / DBRowCount function will create
            self.table.setColumnCount(21)  # database sutun sayisi duzenleme
            self.table.setHorizontalHeaderLabels(["Kimlik ID", "İsim", "Soyisim", "Telefon No", "Mail Adresi",
                                                  "Kargo ID", "Takip No", "QR Kod", "PNR No", "Ek Güvenlik",
                                                  "Kargo Oluşturma Tarihi", "Kargo Teslim Tarihi", "Teslim Edildi mi?",
                                                  "Dolap ID", "Yerel Dolap No", "Boyut", "Boş mu?",
                                                  "SafetyBox's İsmi", "SafetyBox's Adres", "İlçe", "İl"])

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
                self.table.setItem(row, 10, QTableWidgetItem(str(get_DB[12])))
                self.table.setItem(row, 11, QTableWidgetItem(str(get_DB[13])))
                self.table.setItem(row, 12, QTableWidgetItem(str(get_DB[14])))
                self.table.setItem(row, 13, QTableWidgetItem(str(get_DB[15])))
                self.table.setItem(row, 14, QTableWidgetItem(str(get_DB[16])))
                self.table.setItem(row, 15, QTableWidgetItem(str(get_DB[17])))
                self.table.setItem(row, 16, QTableWidgetItem(str(get_DB[18])))
                self.table.setItem(row, 17, QTableWidgetItem(str(get_DB[21])))
                self.table.setItem(row, 18, QTableWidgetItem(str(get_DB[22])))
                self.table.setItem(row, 19, QTableWidgetItem(str(get_DB[25])))
                self.table.setItem(row, 20, QTableWidgetItem(str(get_DB[26])))
                row = row + 1


        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Install the central widget

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        central_widget.setLayout(hbox)  # Install this placement in the central widget

        self.table.resizeColumnsToContents()
        hbox.addLayout(vbox)
        hbox.addWidget(self.table)

        self.combobox = QComboBox(self)
        self.combobox.addItems(["İlçeler", "SafetyBox's", "Dolaplar", "Kargolar", "Kimlikler", "Detaylı Tablo"])
        button = QPushButton("button")
        vbox.addWidget(self.combobox)
        vbox.addWidget(button)
        button.clicked.connect(self.update_Table)

    def update_Table(self):
        table_name = self.combobox.currentText()
        print(table_name)
        self.table_DB(table_name)



