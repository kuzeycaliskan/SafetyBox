import cv2
from PyQt5.Qt import *
from pyzbar import pyzbar
import Finder
import time

class QRWindow(QWidget):
    Finder = Finder.Finder()
    Widget = 1

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480

        # self.InfoWindow("receiver", "q6cw165rq1vteg49638g416a6s5a6d")

        self.initUI()
        self.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.CameraLabel.setPixmap(QPixmap.fromImage(image))
    #
    # def setcllback2Main(self, cllbackFunc):
    #     print("setcllback2main func girildi")
    #     self.cllbackFunc = cllbackFunc

    def cllback(self, barcodeData):
        self.barcodeData = barcodeData
        self.Widget.setHidden(False)
        # self.close()
        return

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640, 480)

        self.Widget = QWidget()
        self.Widget.show()
        self.Widget.setHidden(True)

        # create a label
        self.CameraLabel = QLabel(self)
        # self.label.move(280, 120)
        self.CameraLabel.resize(640, 480)
        self.th = Thread(self)
        self.th.setCllback(self.cllback)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        button = QPushButton("Info Window")
        button.clicked.connect(self.testfunc)
        vbox = QVBoxLayout()
        vbox.addWidget(self.CameraLabel)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def testfunc(self):
        self.cllbackFunc("fsdg984sdg84fdd121df154asdqzs7")

    def closeEvent(self, event):
        self.Finder.QRCodeFinder(self.barcodeData)
        # self.th.quit()
        # self.th.wait()
        # self.th.cap.release()
        # self.th.threadactive = False
        # self.close()
        # self.cllbackFunc("fsdg984sdg84fdd121df154asdqzs7")



class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    counter = 0

    def setCllback(self, cllbck):
        print("thread setcllback func girildi")
        self.cllbck = cllbck

    def run(self):
        counter = 0
        self.cap = cv2.VideoCapture(0)
        self.threadactive = True

        while (self.threadactive):
            ret, frame = self.cap.read()
            if self.cap.read() is None:
                break
            barcodes = pyzbar.decode(frame)
            found = set()

            for barcode in barcodes:
                counter = counter + 1
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                print(counter, barcodeData)
                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode   q to disk and update the set
                if barcodeData not in found:
                    if counter == 10:
                        self.threadactive = False
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        if(self.threadactive is False):
            print('Thread continue')
            self.cap.release()
            self.cllbck(barcodeData)


