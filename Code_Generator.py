import datetime
from random import randint
import main_DB
import random
import string


class Code_Generator():
    database = main_DB.main_DB()
    Tr2Eng = str.maketrans("ÇĞİÖŞÜçğıöşü", "CGIOSUcgiosu")
    def create_Tracking(self, n):
        TrackingList = self.database.getTrackList()
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1

        Random_PNR = randint(range_start, range_end)

        checkvalue = 0

        while True:
            for PNR in TrackingList:
                if int(Random_PNR) == int(PNR[0]):
                    print("3")
                    checkvalue = checkvalue + 1
            if checkvalue == 0:
                return Random_PNR
            else:
                Random_PNR = randint(range_start, range_end)

    def create_PNR(self, n):
        PNRList = self.database.getPNRList()
        range_start = 10 ** (n - 1)
        range_end = (10 ** n) - 1

        Random_PNR = randint(range_start, range_end)

        checkvalue = 0

        while True:
            for PNR in PNRList:
                if int(Random_PNR) == int(PNR[0]):
                    print("3")
                    checkvalue = checkvalue + 1
            if checkvalue == 0:
                return Random_PNR
            else:
                Random_PNR = randint(range_start, range_end)

    def randomStringDigits(self, stringLength=8):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    def create_QRCode(self, surname, name, county, city):
        print("çevrilmeden önce ", county)
        surname = surname.translate(self.Tr2Eng)
        name = name.translate(self.Tr2Eng)
        county = county.translate(self.Tr2Eng)
        city = city.translate(self.Tr2Eng)
        print("çevrilmeden sonra ", county)
        currenttime = datetime.datetime.now()
        PNR = self.create_PNR(8)
        Tracking = self.create_Tracking(8)

        QRCode = ("R/*/" + surname + "/" + name + ">>" + str(Tracking) + ">>" + currenttime.strftime("%Y/%m/%d") +
                  ">X1" + ">>" + str(self.randomStringDigits(8)).upper() + ">>" + county.upper() + ">>>" +
                  str(PNR) + "//" + city.upper() + "/V1")

        return PNR, Tracking, QRCode, currenttime.strftime("%Y-%m-%d %H:%M:%S")
