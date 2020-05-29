from PyQt5.Qt import *
import Database
import datetime
import InfoWindow


class Finder():
    database = Database.main_DB()
    currenttime = datetime.datetime.now()

    def PNRFinder(self, currenttext):  # find person from PNR Number
        print('PNRFINDER')
        getPNRList = self.database.getPNRList()  # calling all PNR list from Database
        self.i = 0

        for getPNR in getPNRList:  # search in database
            if int(currenttext) == int(getPNR[0]):  # if found open info window
                # print(int(currenttext) == int(getPNR[0]))
                self.i = self.i + 1
                return self.getValues("receiver", "PNR", str(getPNR[0]))
            else:
                pass
                # print(getPNR[0])
            print(int(currenttext) == int(getPNR[0]))

        if self.i == 0:  # if not found give information is provided
            return None

    def TrackFinder(self, currenttext):  # Takip numarası karşılaştırma
        getTrackList = self.database.getTrackList()
        i = 0

        for getTrack in getTrackList:

            if int(currenttext) == int(getTrack[0]):

                i = i + 1

                return self.getValues("delivery", "Tracking", str(getTrack[0]))
            else:
                pass

        if i == 0:

            return None

    def QRCodeFinder(self, barcodeData):  # find person with QR Code
        barcodeData_type = barcodeData.split("/*/")
        barcodeData_type = barcodeData[0]
        if barcodeData_type == "R":
            getQRCodeList = self.database.getQRCodeList_Cargo()
            i = 0
            for QRCode in getQRCodeList:
                if QRCode[0] == barcodeData:
                    print("success. I found a person")
                    print(type(barcodeData))
                    print(type(QRCode[0]))
                    i = i + 1
                    print("Finder Check: ", QRCode)
                    return self.getValues("receiver", "QRCode", str(QRCode[0]))
                else:
                    pass
                    # print(type)
                    # print("trying another QRCode")

            if i == 0:  # if not found give information is provided
                return None

        elif barcodeData_type == "L":
            getQRCodeList = self.database.getQRCodeList_Locker()
            i = 0
            for QRCode in getQRCodeList:
                if QRCode[0] == barcodeData:
                    print("success. I found a person")
                    print(type(barcodeData))
                    print(type(QRCode[0]))
                    i = i + 1
                    return self.getValues("Locker", "QRCode", str(QRCode[0]))
                else:
                    pass
                    # print(type)
                    # print("trying another QRCode")

            if i == 0:  # if not found give information is provided
                return None



    def getValues(self, cargo_type, info_type, info):  # calling info window class with PNR Number

        if cargo_type == "receiver" and info_type == "PNR":
            list_InfoWindow = self.database.getIdentity_withPNRNo(info)
            self.database.setBoxState_isEmpty("1", str(list_InfoWindow[0][5]))
            self.database.setCargoState_isReceived_withPNR("1", info)
            self.database.setCargoState_received_at_withPNR(self.currenttime.strftime("%Y-%m-%d %H:%M:%S"), info)
            return cargo_type, list_InfoWindow
        elif cargo_type == "delivery" and info_type == "Tracking":
            list_InfoWindow = self.database.getIdentity_withTrackingNo(info)
            mail_track = self.database.getMailinfo_withTrackingNo(info)  # Takip numarası ile mail içerikleri çekme
            self.database.setCargoState_delivered_at_withTracking(self.currenttime.strftime("%Y-%m-%d %H:%M:%S"), info)
            return cargo_type, list_InfoWindow, mail_track

        elif cargo_type == "receiver" and info_type == "QRCode":
            getPerson = self.database.getIdentity_with_LockerQRCode(info)
            self.database.setBoxState_isEmpty("1", str(getPerson[0][5]))
            self.database.setCargoState_isReceived_withQRCode("1", info)
            self.database.setCargoState_received_at_withQRCode(self.currenttime.strftime("%Y-%m-%d %H:%M:%S"), info)
            return cargo_type, getPerson
        elif cargo_type == "delivery" and info_type == "QRCode":
            getPerson = self.database.getIdentity_with_LockerQRCode(info)
            return cargo_type, getPerson

        elif cargo_type == "Locker" and info_type == "QRCode":
            getPerson = self.database.getIdentity_with_LockerQRCode(info)
            self.database.setBoxState_isEmpty("1", str(getPerson[0][5]))
            self.database.setLockerState_isReceived_withQRCode("1", info)
            self.database.setLockerState_received_at_withQRCode(self.currenttime.strftime("%Y-%m-%d %H:%M:%S"), info)
            return cargo_type, getPerson

