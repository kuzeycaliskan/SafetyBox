from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
import main_DB
from PyQt5 import QtCore
from PyQt5.Qt import *


# Inheriting from QMainWindow
class Window_DB(QMainWindow):
    # Overriding the class constructor
    def __init__(self, table_name):
        # Be sure to call the super class method
        QMainWindow.__init__(self)

        self.setGeometry(0, 0, 1080, 732)  # window size
        self.setWindowTitle("Database Table")
        self.database = main_DB.main_DB()
        self.table_DB(table_name)


        self.show()

    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Are you sure want to stop process?",
                                     QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def table_DB(self, table_name):
        self.model = QStandardItemModel(self)
        self.table = QTableView(self)  # Create a table

        if table_name == "İlçeler":
            read_db = self.database.getCounties()

            self.model.setHorizontalHeaderLabels(["ID", "İlçe Adı", "İl Adı"])


            for get_DB in read_db:
                self.model.invisibleRootItem().appendRow(
                    [QStandardItem("{}".format(column))
                     for column in get_DB
                     ])

                print(get_DB[0], get_DB[1], get_DB[2])

            self.proxy = QSortFilterProxyModel(self)
            self.proxy.setSourceModel(self.model)

            self.table.setModel(self.proxy)


        elif table_name == "SafetyBox's":
            read_db = self.database.getSafetyBoxs()

            self.model.setHorizontalHeaderLabels(["ID", "SafetyBox İsmi", "SafetyBox Adres", "Kayıtlı İlçe ID"])


            for get_DB in read_db:
                self.model.invisibleRootItem().appendRow(
                    [QStandardItem("{}".format(column))
                     for column in get_DB
                     ])

                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3])

            self.proxy = QSortFilterProxyModel(self)
            self.proxy.setSourceModel(self.model)

            self.table.setModel(self.proxy)


        elif table_name == "Dolaplar":
            print("Checked for Access Dolaplar Case")
            read_db = self.database.getAllBoxs()

            self.model.setHorizontalHeaderLabels(["ID", "Dolap No", "Boyut", "Boş Mu?", "Kayıtlı SafetyBox ID",
                                                  "SafetyBox İsim", "SafetyBox Adres"])

            for get_DB in read_db:
                self.model.invisibleRootItem().appendRow(
                    [QStandardItem("{}".format(column))
                     for column in get_DB
                     ])

                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4])
            self.proxy = QSortFilterProxyModel(self)
            self.proxy.setSourceModel(self.model)

            self.table.setModel(self.proxy)

        elif table_name == "Kargolar":
            read_db = self.database.getCargoes()

            self.model.setHorizontalHeaderLabels(["ID", "Takip No", "QR Kod", "PNR No", "Ek Güvenlik",
                                                  "Kayıtlı Dolap ID", "Kayıtlı Kimlik ID", "Kargo Oluşturma Tarihi",
                                                  "Kargo Teslim Tarihi", "Teslim edildi mi?"])

            for get_DB in read_db:
                self.model.invisibleRootItem().appendRow(
                    [QStandardItem("{}".format(column))
                     for column in get_DB
                     ])

                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4], get_DB[5], get_DB[6], get_DB[7], get_DB[8],
                      get_DB[9])

            self.proxy = QSortFilterProxyModel(self)
            self.proxy.setSourceModel(self.model)

            self.table.setModel(self.proxy)


        elif table_name == "Kimlikler":
            read_db = self.database.getIdentities()

            self.model.setHorizontalHeaderLabels(["ID", "İsim", "Soyisim", "Telefon No", "Mail Adresi"])

            for get_DB in read_db:
                self.model.invisibleRootItem().appendRow(
                    [QStandardItem("{}".format(column))
                     for column in get_DB
                     ])

                print(get_DB[0], get_DB[1], get_DB[2], get_DB[3], get_DB[4])

            self.proxy = QSortFilterProxyModel(self)
            self.proxy.setSourceModel(self.model)

            self.table.setModel(self.proxy)


        elif table_name == "Detaylı Tablo":
            read_db = self.database.getDB_All()

            self.model.setHorizontalHeaderLabels(["Kimlik ID", "İsim", "Soyisim", "Telefon No", "Mail Adresi",
                                                  "Kargo ID", "Takip No", "QR Kod", "PNR No", "Ek Güvenlik",
                                                  "Kargo Oluşturma Tarihi", "Kargo Teslim Tarihi", "Teslim Edildi mi?",
                                                  "Dolap ID", "Yerel Dolap No", "Boyut", "Boş mu?",
                                                  "SafetyBox's İsmi", "SafetyBox's Adres", "İlçe", "İl"])

            for get_DB in read_db:
                self.model.invisibleRootItem().appendRow(
                    [QStandardItem("{}".format(column))
                     for column in get_DB
                     ])

            self.proxy = QSortFilterProxyModel(self)
            self.proxy.setSourceModel(self.model)

            self.table.setModel(self.proxy)


        central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(central_widget)  # Install the central widget

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.setSizeConstraint(QLayout.SetMinimumSize)

        central_widget.setLayout(hbox)  # Install this placement in the central widget

        self.table.resizeColumnsToContents()
        hbox.addLayout(vbox)
        hbox.addWidget(self.table)

        self.combobox_Tablename = QComboBox(self)
        self.combobox_Tablename.addItems(["İlçeler", "SafetyBox's", "Dolaplar", "Kargolar", "Kimlikler", "Detaylı Tablo"])

        self.checkbox = QCheckBox("Detaylı Sorgulama")
        self.checkbox.stateChanged.connect(self.DetailSearch)

        self.combobox_Column = QComboBox(self)
        self.combobox_Column.addItems(["Takip_Numarasi", "Ad", "Soyad",  "Tel_num"])
        self.combobox_Column.setVisible(False)
        self.combobox_Column.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)
        self.combobox_Column.setCurrentIndex(0)

        self.textbox_DetailSearch = QLineEdit()
        self.textbox_DetailSearch.setPlaceholderText("Arama Parametresini Yazınız")
        self.textbox_DetailSearch.setFixedWidth(self.combobox_Column.width()*2)
        self.textbox_DetailSearch.setVisible(False)
        self.textbox_DetailSearch.textChanged.connect(self.on_lineEdit_textChanged)


        self.button = QPushButton("Onayla")
        vbox.addWidget(self.combobox_Tablename)
        vbox.addWidget(self.button)
        vbox.addWidget(self.checkbox)
        vbox.addWidget(self.textbox_DetailSearch)
        vbox.addWidget(self.combobox_Column)
        self.button.clicked.connect(self.update_Table)

    def update_Table(self):
        table_name = self.combobox_Tablename.currentText()
        print(table_name)
        self.table_DB(table_name)

    def DetailSearch(self):
        if self.checkbox.isChecked():
            self.table_DB("Detaylı Tablo")
            
            self.combobox_Tablename.setVisible(False)
            self.button.setVisible(False)
            self.textbox_DetailSearch.setVisible(True)
            self.combobox_Column.setVisible(True)
            self.on_comboBox_currentIndexChanged(0)

        else:
            self.combobox_Tablename.setVisible(True)
            self.button.setVisible(True)
            self.textbox_DetailSearch.setVisible(False)
            self.table_DB("İlçeler")

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self.proxy.setFilterRegExp(search)

    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        if index == 0:
            self.proxy.setFilterKeyColumn(6)
        else:
            self.proxy.setFilterKeyColumn(index)