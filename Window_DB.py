from PyQt5.QtWidgets import *
import main_DB

class Window_DB(QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1080, 640)  # 50,50 parametresi pencerede nerede baslayacigini belirler
        self.setWindowTitle("PyQt5 App")
        self.database = main_DB.main_DB()
        self.rowCount = self.database.getRowCount()
        read_DB = self.database.getDB_All()



        # print("window_DB Class Test")
        self.table_DB(read_DB)
        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)
        self.show()

    def table_DB(self, read_db):

        vbox = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(self.rowCount) #database satir sayisi duzenleme / DBRowCount function will create
        self.table.setColumnCount(13) #database sutun sayisi duzenleme
        self.table.setHorizontalHeaderItem(0,QTableWidgetItem("No"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("Takip Numarası"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Ad"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("Soyad"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("Telefon No"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("Mail"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("QR Kod"))
        self.table.setHorizontalHeaderItem(7, QTableWidgetItem("PNR No"))
        self.table.setHorizontalHeaderItem(8, QTableWidgetItem("Güvenlik"))
        self.table.setHorizontalHeaderItem(9, QTableWidgetItem("Lokasyon"))
        self.table.setHorizontalHeaderItem(10, QTableWidgetItem("Dolap No"))
        self.table.setHorizontalHeaderItem(11, QTableWidgetItem("Kargo Baş.Trh."))
        self.table.setHorizontalHeaderItem(12, QTableWidgetItem("Kargo Btş.Trh."))


        row = 0
        for get_DB in read_db:
            # print('(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % get_DB)
            # print(type(get_DB))
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
            self.table.setItem(row, 10, QTableWidgetItem(str(get_DB[10])))
            self.table.setItem(row, 11, QTableWidgetItem(str(get_DB[11])))
            self.table.setItem(row, 12, QTableWidgetItem(str(get_DB[12])))
            row = row + 1

        button = QPushButton("Table")
        button.clicked.connect(self.getValue)

        vbox.addWidget(button)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def getValue(self):
        for item in self.table.selectedItems():
            print("value: {},  row: {}, column: {}".format(item.text(),item.row(),item.column()))

    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Sure?",
                                      QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()




