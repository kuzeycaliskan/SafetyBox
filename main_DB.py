import mysql.connector


class main_DB():
    def __init__(self):
        super().__init__()
        print(mysql.connector.version)
        # with open("DBparameters.txt", "r") as DB_pm:
        #     DB_pm_list = DB_pm.read().splitlines()
        #     print(DB_pm_list)
        #
        #
        # self.connection = mysql.connector.connect(user=DB_pm_list[0], password=DB_pm_list[1],
        #                       host=DB_pm_list[2],
        #                       database=DB_pm_list[3])
        #
        self.connection = mysql.connector.connect(user="root", password="kuzey7174",
                                                  host="192.168.43.146",
                                                  database="cargosystem")

        if (self.connection):
            print('baglanti başarili')
        else:
            print('bağlanti basarisiz')

        self.select_DB = self.connection.cursor()

    def getCounties(self):
        self.select_DB.execute('SELECT * FROM ilceler')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getSafetyBoxs(self):
        self.select_DB.execute('SELECT * FROM safetyboxs')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getAllBoxs(self):
        self.select_DB.execute('SELECT * FROM dolaplar')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getCargoes(self):
        self.select_DB.execute('SELECT * FROM kargolar')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getIdentities(self):
        self.select_DB.execute('SELECT * FROM kimlikler')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getRowCount_Counties(self):
        self.select_DB.execute('SELECT COUNT(*) FROM ilceler')
        readRowCount = self.select_DB.fetchone()
        return readRowCount[0]

    def getRowCount_SafetyBoxs(self):
        self.select_DB.execute('SELECT COUNT(*) FROM safetyboxs')
        readRowCount = self.select_DB.fetchone()
        return readRowCount[0]

    def getRowCount_AllBoxs(self):
        self.select_DB.execute('SELECT COUNT(*) FROM dolaplar')
        readRowCount = self.select_DB.fetchone()
        return readRowCount[0]

    def getRowCount_Cargoes(self):
        self.select_DB.execute('SELECT COUNT(*) FROM kargolar')
        readRowCount = self.select_DB.fetchone()
        return readRowCount[0]

    def getRowCount_Identities(self):
        self.select_DB.execute('SELECT COUNT(*) FROM kimlikler')
        readRowCount = self.select_DB.fetchone()
        return readRowCount[0]

    def getRowCount(self):
        self.select_DB.execute('SELECT COUNT(*) FROM cargosystem')
        readRowCount = self.select_DB.fetchone()
        return readRowCount[0]

    def createRow(self, newrowlist):
        self.select_DB.execute("INSERT INTO cargosystem (Takip_Numarasi,Ad,Soyad,Tel_Num,Mail_adres,Qrkod,Pnr_Num," +
                               "Security,Box_Location,Cabin_Num,Cargo_Start_Time,Cargo_End_Time) VALUES (" + "'" +
                               newrowlist[0] + "'" + "," +
                               "'" + newrowlist[1] + "'" + "," + "'" + newrowlist[2] + "'" + "," + "'" + newrowlist[
                                   3] + "'" + "," + "'" +
                               newrowlist[4] + "'" + "," + "'" + newrowlist[5] + "'" + "," + "'" + newrowlist[
                                   6] + "'" + "," + "'" +
                               newrowlist[7] + "'" + "," + "'" + newrowlist[8] + "'" + "," + "'" + newrowlist[
                                   9] + "'" + "," + "'" +
                               newrowlist[10] + "'" + "," + "'" + newrowlist[11] + "'" + ")")

        self.connection.commit()  # confirm to new register

    def getDB_All(self):
        self.select_DB.execute('SELECT * FROM cargosystem')
        read_DB = self.select_DB.fetchall()
        # print(oku.fetchall())
        for get_DB in read_DB:
            print(get_DB)

        return read_DB

    def getPNRList(self):
        self.select_DB.execute("SELECT Pnr_Num FROM cargosystem")
        readPNR_DB = self.select_DB.fetchall()
        return readPNR_DB

    def getInfo_IW(self, PNR_num):
        self.select_DB.execute('SELECT * FROM cargosystem WHERE Pnr_Num =' + PNR_num)
        readInfo_IW = self.select_DB.fetchall()

        return readInfo_IW

    def getTrackList(self):
        self.select_DB.execute("SELECT Takip_Numarasi FROM cargosystem")
        readTrack_DB = self.select_DB.fetchall()

        return readTrack_DB

    def getTracking_Num_DW(self, Tracking_num):
        self.select_DB.execute('SELECT * FROM cargosystem WHERE Takip_Numarasi =' + Tracking_num)
        readDelivery_DW = self.select_DB.fetchall()

        return readDelivery_DW


    def getCabin_Num(self):
        self.select_DB.execute('SELECT Cabin_Num FROM cargosystem')
        readCabin_Num = self.select_DB.fetchall()

        return readCabin_Num


    def deleteTable(self):
        self.select_DB.execute("DROP TABLE cargosystem")

        self.connection.commit()
        self.connection.close()
