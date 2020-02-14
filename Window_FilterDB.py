from PyQt5 import QtCore, QtGui
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
import main_DB

class Window_FilterDB(QMainWindow):

    def __init__(self):
        super().__init__()

        self.centralwidget = QWidget(self)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.view = QTableView(self.centralwidget)
        self.comboBox = QComboBox(self.centralwidget)
        self.label = QLabel(self.centralwidget)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.view, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.setCentralWidget(self.centralwidget)
        self.label.setText("Regex Filter")

        self.model = QStandardItemModel(self)

        for rowName in range(0, 15):
            self.model.invisibleRootItem().appendRow(
                [QStandardItem("row {0} col {1}".format(rowName, column))
                 for column in range(5)
                 ]
            )

        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)

        self.view.setModel(self.proxy)
        self.comboBox.addItems(["Column {0}".format(x) for x in range(self.model.columnCount())])

