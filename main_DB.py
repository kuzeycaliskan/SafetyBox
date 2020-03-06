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
                                                  host="localhost",
                                                  database="safetybox_db")

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

    def getDB_All(self):
        self.select_DB.execute("select kimlikler_id,isim,soyisim,tel_num,mail,krg.id,krg.takip_no,krg.qr_kod," +
                               "krg.PNR_num,krg.is_security,krg.created_at,krg.received_at, krg.is_received, dlp.id," +
                               "dlp.dolap_no, dlp.boyut, dlp.is_empty, sftb.isim_sb, sftb.adres,i.ilce, i.il from " +
                               "kimlikler inner join kargolar krg on kimlikler.id = krg.kimlikler_id inner join " +
                               "dolaplar dlp on krg.dolaplar_id = dlp.id inner join safetyboxs sftb on " +
                               "dlp.safetyboxs_id = sftb.id inner join ilceler i on sftb.ilceler_id = i.id")
        read_DB = self.select_DB.fetchall()
        # print(oku.fetchall())
        # for get_DB in read_DB:
        #     print(get_DB)

        return read_DB

    def getPNRList(self):
        self.select_DB.execute("SELECT PNR_num FROM kargolar")
        readPNR_DB = self.select_DB.fetchall()
        return readPNR_DB

    def getQRCodeList(self):
        self.select_DB.execute("select qr_kod from kargolar")
        readQRCode = self.select_DB.fetchall()
        return readQRCode

    def getPerson_withPNRNo(self, PNR_num):
        self.select_DB.execute('select isim,soyisim,tel_num,mail,dolap_no from kimlikler inner join kargolar krg on' +
                               ' kimlikler.id = krg.kimlikler_id inner join dolaplar dlp on krg.dolaplar_id = dlp.id' +
                               ' WHERE PNR_num =' + PNR_num)
        readInfo_IW = self.select_DB.fetchall()


        return readInfo_IW

    def getTrackList(self):
        self.select_DB.execute("SELECT takip_no FROM kargolar")
        readTrack_DB = self.select_DB.fetchall()

        return readTrack_DB

    def getPerson_withTrackingNo(self, Tracking_num):
        self.select_DB.execute('select isim,soyisim,tel_num,mail from kimlikler inner join kargolar krg on ' +
                               'kimlikler.id = krg.kimlikler_id where  takip_no =' + Tracking_num)
        readDelivery_DW = self.select_DB.fetchall()

        return readDelivery_DW

    def getPerson_withQRCode(self, QRCode):
        self.select_DB.execute('select isim,soyisim,tel_num,mail,dolap_no from kimlikler inner join kargolar krg on ' +
                               'kimlikler.id = krg.kimlikler_id inner join dolaplar dlp on krg.dolaplar_id = dlp.id ' +
                               'where  krg.qr_kod =' + '"' + str(QRCode) + '"')
        readDelivery_DW = self.select_DB.fetchall()

        return readDelivery_DW

    def getBoxNo_withTrackingNum(self, Tracking_num):
        self.select_DB.execute("select dolaplar.dolap_no from dolaplar inner join kargolar k on" +
                               " dolaplar.id = k.dolaplar_id where k.PNR_num = " + Tracking_num)

        readBoxNo = self.select_DB.fetchone()
        return readBoxNo[0]

    def getBoxNo_withQRCode(self, QRCode):
        self.select_DB.execute("select dolaplar.dolap_no from dolaplar inner join kargolar k on" +
                               " dolaplar.id = k.dolaplar_id where k.qr_kod =" + QRCode)

        readBoxNo = self.select_DB.fetchone()
        return readBoxNo[0]

    def deleteTable(self, table_name):
        self.select_DB.execute('DROP TABLE ' + table_name)

        self.connection.commit()
        self.connection.close()
