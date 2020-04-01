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
        #                                           host=DB_pm_list[2],
        #                                           database=DB_pm_list[3])

        self.connection = mysql.connector.connect(user="root", password="kuzey7174",
                                                  host="192.168.1.37",
                                                  database="safetybox_db")

        if (self.connection):
            print('baglanti başarili')
        else:
            print('bağlanti basarisiz')

        self.select_DB = self.connection.cursor()

    def setBoxState_isEmpty(self, state, box_no):
        self.select_DB.execute('UPDATE dolaplar SET is_empty = ' + '"' + state + '"' + ' WHERE id = ' + '"' + box_no + '"')
        self.connection.commit()

    def setCargoState_isReceived_withPNR(self, state, PNR_num):
        self.select_DB.execute('UPDATE kargolar SET is_received = ' + '"' + state + '"' + 'WHERE PNR_num = ' + '"' + PNR_num + '"')
        self.connection.commit()

    def setCargoState_isReceived_withQRCode(self, state, QR_Code):
        self.select_DB.execute('UPDATE kargolar SET is_received = ' + '"' + state + '"' + 'WHERE qr_kod = ' + '"' + QR_Code + '"')
        self.connection.commit()

    def setCargoState_delivered_at_withTracking(self, date, Tracking):
        self.select_DB.execute('UPDATE kargolar SET delivered_at = ' + '"' + date + '"' + ' WHERE takip_no = ' + Tracking)
        self.connection.commit()

    def setCargoState_received_at_withPNR(self, date, PNR):
        self.select_DB.execute('UPDATE kargolar SET received_at = ' + '"' + date + '"' + ' WHERE PNR_num = ' + PNR)
        self.connection.commit()

    def setCargoState_received_at_withQRCode(self, date, QR_Code):
        self.select_DB.execute('UPDATE kargolar SET received_at = ' + '"' + date + '"' + ' WHERE qr_kod = ' + '"' + QR_Code + '"')
        self.connection.commit()

    def setQRCode(self, new_QR, old_QR):
        self.select_DB.execute('UPDATE kargolar SET qr_kod = ' + '"' + new_QR + '"' + ' WHERE kargolar.qr_kod = ' + '"' + old_QR + '"')
        self.connection.commit()

    def updateIdentity(self, n_column, n_value, tel_num, o_value):
        self.select_DB.execute('UPDATE kimlikler SET ' + n_column + ' = ' + '"' + n_value + '"' + ' WHERE ' + tel_num +
                               ' = ' + '"' + o_value + '"')
        self.connection.commit()

    def getCounties(self):
        self.select_DB.execute('SELECT * FROM ilceler')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getCounties_withCities(self, city):
        self.select_DB.execute('SELECT ilce FROM ilceler where il = ' + '"' + city + '"')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getSafetyBoxs(self):
        self.select_DB.execute('SELECT * FROM safetyboxs')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getSafetyBoxs_withCounties(self, county):
        self.select_DB.execute('select safetyboxs.isim_sb, safetyboxs.adres from safetyboxs inner join ilceler i on' +
                               ' safetyboxs.ilceler_id = i.id where i.ilce = ' + '"' + county + '"')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getAllBoxs(self):
        self.select_DB.execute('select d.id, d.dolap_no, d.boyut, d.is_empty, d.safetyboxs_id, s.isim_sb, s.adres '
                               ' from dolaplar d inner join safetyboxs s on d.safetyboxs_id = s.id')
        read_DB = self.select_DB.fetchall()

        return read_DB

    def getBoxs_WhichAvailable_WithSize(self, safety_name, size):
        self.select_DB.execute("SELECT dolaplar.id, dolap_no, boyut, is_empty, safetyboxs_id FROM dolaplar " +
                               " INNER JOIN safetyboxs s ON dolaplar.safetyboxs_id = s.id where isim_sb = " + '"' +
                               safety_name + '"' + " and is_empty = 1 and boyut = " + '"' + size + '"')
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

    def getIdentity_ID(self, phone):
        self.select_DB.execute("SELECT id FROM kimlikler where tel_num =" + phone)
        read_DB = self.select_DB.fetchone()

        return read_DB[0]

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
        self.select_DB.execute('select isim,soyisim,tel_num,mail,dolap_no,dolaplar_id from kimlikler inner join '
                               'kargolar krg on kimlikler.id = krg.kimlikler_id inner join dolaplar dlp on '
                               ' krg.dolaplar_id = dlp.id WHERE PNR_num = ' + PNR_num)
        readInfo_IW = self.select_DB.fetchall()

        return readInfo_IW

    def getPerson_withQRCode(self, QRCode):
        self.select_DB.execute('select isim,soyisim,tel_num,mail,dolap_no,dolaplar_id from kimlikler inner join '
                               ' kargolar krg on kimlikler.id = krg.kimlikler_id inner join dolaplar dlp on '
                               ' krg.dolaplar_id = dlp.id where  krg.qr_kod =' + '"' + str(QRCode) + '"')
        readDelivery_DW = self.select_DB.fetchall()

        return readDelivery_DW

    def getTrackList(self):
        self.select_DB.execute("SELECT takip_no FROM kargolar")
        readTrack_DB = self.select_DB.fetchall()

        return readTrack_DB

    def getTrackingNo_withPNRNo(self, PNR_No):
        self.select_DB.execute('SELECT takip_no from kargolar where PNR_num = ' + '"' + PNR_No + '"')
        read_DB = self.select_DB.fetchone()

        return read_DB[0]

    def getPerson_withTrackingNo(self, Tracking_num):
        self.select_DB.execute('select isim,soyisim,tel_num,mail,dolap_no,dolaplar_id from kimlikler inner join '
                               ' kargolar krg on kimlikler.id = krg.kimlikler_id inner join dolaplar dlp on '
                               ' krg.dolaplar_id = dlp.id where  takip_no =' + '"' + str(Tracking_num) + '"')
        readDelivery_DW = self.select_DB.fetchall()

        return readDelivery_DW

    def getMailinfo_withTrackingNo(self, Tracking_num):
        self.select_DB.execute('select isim,soyisim,tel_num,mail,krg.takip_no,krg.PNR_num,sftb.isim_sb,sftb.adres,i.ilce, i.il from '
                               'kimlikler inner join kargolar krg on kimlikler.id = krg.kimlikler_id inner join dolaplar dlp on krg.dolaplar_id = dlp.id '
                               'inner join safetyboxs sftb on dlp.safetyboxs_id = sftb.id inner join ilceler i on sftb.ilceler_id = i.id inner join kargolar '
                               'on kimlikler.id = kargolar.kimlikler_id where krg.takip_no =' + Tracking_num)

        mailinfo_Track = self.select_DB.fetchall()

        return mailinfo_Track

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

    def create_Cargo(self, tracking, QRCode, PNR, security, dolap_id, kimlik_id, create_date,  received):
        self.select_DB.execute('INSERT INTO kargolar (takip_no, qr_kod, pnr_num, is_security, dolaplar_id,' +
                               ' kimlikler_id, created_at, is_received) VALUES (' + str(tracking) + ',' + '"' +
                                QRCode + '"' + ',' + str(PNR) + ',' + str(security) + ',' + str(dolap_id) + ',' +
                                str(kimlik_id) + ',' + '"' + str(create_date) + '"' + ',' + str(received) + ')')

        self.connection.commit()

    def create_Identity(self, name, surname, phone, email):
        self.select_DB.execute("INSERT INTO kimlikler (isim, soyisim, tel_num, mail) VALUES (" + '"' +
                               str(name) + '"' + ',' + '"' + str(surname) + '"' +  ',' + str(phone) + "," +
                               '"' + str(email) + '"' + ')')

        self.connection.commit()

    def deleteTable(self, table_name):
        self.select_DB.execute('DROP TABLE ' + table_name)

        self.connection.commit()
