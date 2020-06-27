import datetime
from random import randint
import Database
import random
import string
import qrcode


class Code_Generator():
    database = Database.main_DB()
    Tr2Eng = str.maketrans("ÇĞİÖŞÜçğıöşü", "CGIOSUcgiosu")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    def Generate_Tracking_Num(self, n):  # create n digit random number
        TrackingList = self.database.getTrackList()
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1

        Random_PNR = randint(range_start, range_end)

        checkvalue = 0  # the value is checking for did it created before or not, in while loop

        while True:
            for PNR in TrackingList:
                if int(Random_PNR) == int(PNR[0]):
                    checkvalue = checkvalue + 1
            if checkvalue == 0:
                return Random_PNR
            else:
                Random_PNR = randint(range_start, range_end)

    def Generate_PNR_Num(self, n):  # create n digit random number
        PNRList = self.database.getPNRList()
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1

        Random_PNR = randint(range_start, range_end)

        checkvalue = 0  # the value is checking for did it created before or not, in while loop

        while True:
            for PNR in PNRList:
                if int(Random_PNR) == int(PNR[0]):
                    print("3")
                    checkvalue = checkvalue + 1
            if checkvalue == 0:
                return Random_PNR
            else:
                Random_PNR = randint(range_start, range_end)

    def randomStringDigits(self, stringLength=8):  # creating random key with string and integer
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    def Generate_AllCodes(self, first_parameter, surname, name, county, city):
        surname = surname.translate(self.Tr2Eng)
        name = name.translate(self.Tr2Eng)
        county = county.translate(self.Tr2Eng)
        city = city.translate(self.Tr2Eng)

        currenttime = datetime.datetime.now()
        PNR = self.Generate_PNR_Num(8)
        Tracking = self.Generate_Tracking_Num(8)

        QRCode = (first_parameter + "/*/" + surname + "/" + name + ">>" + str(Tracking) + ">>" +
                  currenttime.strftime("%Y/%m/%d") + ">X1" + ">>" + str(self.randomStringDigits(8)).upper() + ">>" +
                  county.upper() + ">>>" + str(PNR) + "//" + city.upper() + "/V1")

        self.image_QRCode(first_parameter, QRCode, name, surname, Tracking, PNR)
        return PNR, Tracking, QRCode, currenttime.strftime("%Y-%m-%d %H:%M:%S")

    def image_QRCode(self,first_parameter, QRCode, name, surname, tracking, PNR):
        self.qr.add_data(QRCode)
        self.qr.make(fit=True)

        if first_parameter == "R":
            currenttime = datetime.datetime.now().strftime("%Y_%m_%dat%H.%M.%S")
            image_name = currenttime + "_" + str(tracking) + "_" + surname.lower() + name.lower() + ".png"
            self.qr.make_image().save("/home/pi/Desktop/qr_images/" + image_name)

        elif first_parameter == "L":
            currenttime = datetime.datetime.now().strftime("%Y_%m_%dat%H.%M.%S")
            image_name = currenttime + "_" + str(PNR) + "_" + surname.lower() + name.lower() + ".png"
            self.qr.make_image().save("/home/pi/Desktop/qr_images/" + image_name)