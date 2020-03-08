import cv2
from PyQt5.Qt import *
from pyzbar import pyzbar

class QRWindow(QWidget):
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
        self.label.setPixmap(QPixmap.fromImage(image))

    def setcllback2Main(self, cllbackFunc):
        print("setcllback2main func girildi")
        self.cllbackFunc = cllbackFunc

    def cllback(self, barcodeData):
        self.close()
        # self.QRCodeFinder(barcodeData)
        self.cllbackFunc(barcodeData)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640, 480)
        # create a label
        self.label = QLabel(self)
        # self.label.move(280, 120)
        self.label.resize(640, 480)
        self.th = Thread(self)
        self.th.setCllback(self.cllback)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

    def closeEvent(self, event):
        # self.th.quit()
        # self.th.wait()
        # self.th.cap.release()
        self.th.threadactive = False
        self.close()
        self.cllbackFunc("q6cw165rq1vteg49638g416a6s5a6d")



class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def setCllback(self, cllbck):
        print("thread setcllback func girildi")
        self.cllbck = cllbck

    def run(self):
        counter = 0
        cap = cv2.VideoCapture(0)
        self.threadactive = True

        while (self.threadactive):
            ret, frame = cap.read()
            if cap.read() is None:
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
            cap.release()
            self.cllbck(barcodeData)


