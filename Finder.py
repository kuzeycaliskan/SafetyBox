from PyQt5.Qt import *
import main_DB
import InfoWindow

class Finder():
    database = main_DB.main_DB()


    def PNRFinder(self,currenttext):  # find person from PNR Number
        print('PNRFINDER')
        getPNRList = self.database.getPNRList()  # calling all PNR list from Database
        i = 0


        for getPNR in getPNRList:  # search in database
            if int(currenttext) == int(getPNR[0]):  # if found open info window
                # print(int(currenttext) == int(getPNR[0]))
                i = i + 1
                return self.getValues("receiver", "PNR", str(getPNR[0]))
            else:
                pass
                # print(getPNR[0])
            print(int(currenttext) == int(getPNR[0]))

        if i == 0:  # if not found give information is provided
            QMessageBox.information(self, "Bilgilendirme", "Aradığınız kişi bulunamamıştır.\n "
                                                           "Kontrol edip tekrar deneyiniz.")

    def TrackFinder(self, currenttext):  # Takip numarası karşılaştırma
        print('TrackFINDER')
        getTrackList = self.database.getTrackList()
        i = 0

        for getTrack in getTrackList:

            if int(currenttext) == int(getTrack[0]):

                i = i + 1

                return self.getValues("delivery", "PNR", str(getTrack[0]))
            else:
                pass

            print(int(currenttext) == int(getTrack[0]))

        if i == 0:
            QMessageBox.information(self, "Bilgilendirme", "Aradığınız kişi bulunamamıştır.\n "
                                                           "Kontrol edip tekrar deneyiniz.")


    def QRCodeFinder(self, barcodeData): #find person with QR Code
        getQRCodeList = self.database.getQRCodeList()

        for QRCode in getQRCodeList:
            if QRCode[0] == barcodeData:
                print("success. I found a person")
                print(type(barcodeData))
                print(type(QRCode[0]))
                return self.getValues("receiver", "QRCode", str(QRCode[0]))
            else:
                pass
                # print(type)
                # print("trying another QRCode")

    def getValues(self, cargo_type, info_type, info):  # calling info window class with PNR Number

        if cargo_type == "receiver" and info_type == "PNR":
            list_InfoWindow = self.database.getPerson_withPNRNo(info)
            return cargo_type, list_InfoWindow
        elif cargo_type == "delivery" and info_type == "PNR":
            list_InfoWindow = self.database.getPerson_withTrackingNo(info)
            mail_track = self.database.getMailinfo_withTrackingNo(info) #Takip numarası ile mail içerikleri çekme
            return cargo_type, list_InfoWindow,mail_track

        elif cargo_type == "receiver" and info_type == "QRCode":
            getPerson = self.database.getPerson_withQRCode(info)
            # print("main deneme", getPerson, type(getPerson))
            return cargo_type, getPerson
        elif cargo_type == "delivery" and info_type == "QRCode":
            getPerson = self.database.getPerson_withQRCode(info)
            return cargo_type, getPerson