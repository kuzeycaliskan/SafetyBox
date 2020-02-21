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
                [QStandardItem("row {0} col {1}".format(rowName+1, column+1))
                 for column in range(5)
                 ]
            )

        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)

        self.view.setModel(self.proxy)
        self.comboBox.addItems(["Column {0}".format(x+1) for x in range(self.model.columnCount())])

        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)

        self.horizontalHeader = self.view.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)

    @QtCore.pyqtSlot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
        self.logicalIndex   = logicalIndex
        self.menuValues     = QMenu(self)
        self.signalMapper   = QtCore.QSignalMapper(self)

        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)

        valuesUnique = [    self.model.item(row, self.logicalIndex).text()
                            for row in range(self.model.rowCount())
                            ]

        actionAll = QAction("All", self)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()

        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
            action = QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)

        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)

        headerPos = self.view.mapToGlobal(self.horizontalHeader.pos())

        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    @QtCore.pyqtSlot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(  "",
                                        QtCore.Qt.CaseInsensitive,
                                        QtCore.QRegExp.RegExp
                                        )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(  stringAction,
                                        QtCore.Qt.CaseSensitive,
                                        QtCore.QRegExp.FixedString
                                        )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(    text,
                                    QtCore.Qt.CaseInsensitive,
                                    QtCore.QRegExp.RegExp
                                    )

        self.proxy.setFilterRegExp(search)

    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)

