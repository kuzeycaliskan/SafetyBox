import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import sys
import time
import os


class SendMail():

    def __init__(self, mail_type, knowledge):

        datetime = time.strftime("%d/%m/%Y %H:%M")
        localtime = time.localtime(time.time() + 259200)
        datetime_after3day = time.strftime("%d/%m/%Y %H:%M", localtime)

        message = MIMEMultipart()

        message["From"] = "safetyboxtr@gmail.com"

        message["Subject"] = "SAFETYBOX İLE KARGO TESLİMİ"

        if mail_type == "Creating_Cargo":

            message["To"] = knowledge[3]
            # msgText = MIMEText('<b>Sayın </b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
            self.msgText = MIMEText("<p><b>Sayın " + knowledge[0] + " " + knowledge[1] + ";</b></p>" +
                                    "<p><b>" + str(
                knowledge[4]) + "</b>" + " Takip numaralı kargonuz " + "<b>" + datetime +
                                    "</b>" + " tarihinde " + "<b>" + knowledge[
                                        6] + "</b>" + " şubemize teslim edilmek " +
                                    "üzere oluşturulmuştur.</p>" +
                                    "Kargonuzu SafetyBox'ımıza teslim edildikten sonra" + "<b>" + " 3 gün içerisinde" + "</b>" +
                                    " teslim almanızı öneririz. Teslim alınmayan kargoların otomatik olarak iade işlemleri " +
                                    "başlayacaktır." + "<p> Kargonuz teslim edildikten sonra <b>" +
                                    str(knowledge[
                                            5]) + "</b>" + " PNR numaranız veya QR Kodunuz ile teslim alabilirsiniz." +
                                    "<p><b>Şube adresimiz :</b> " + knowledge[6] + "  " + knowledge[8] + " / " +
                                    knowledge[9] + "</p>" +
                                    "<p><b>Adres Tarifi : </b>" + " " + knowledge[7] + "</p>" +
                                    "<b><i>Safety Box iyi günler diler.</i></b> \n" +
                                    '<br><img src="cid:image1"><br>', 'html')

            for file in os.listdir("/home/pi/Desktop/qr_images/"):
                if file.find(str(knowledge[4])) != -1:
                    self.image_path = os.path.join("/home/pi/Desktop/qr_images/", file)
                    print(os.path.join("/home/pi/Desktop/qr_images/", file))

            fp = open(self.image_path, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            message.attach(self.msgText)
            msgImage.add_header('Content-ID', '<image1>')
            message.attach(msgImage)


        elif mail_type == "Delivering_Cargo":
            print("**********")
            message["To"] = knowledge[0][3]
            # msgText = MIMEText('<b>Sayın </b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
            self.msgText = MIMEText("<p><b>Sayın " + knowledge[0][0] + " " + knowledge[0][1] + ";</b></p>" +
                                    "<p><b>" + str(
                knowledge[0][4]) + "</b>" + " Takip numaralı kargonuz " + "<b>" + datetime +
                                    "</b>" + " tarihinde " + "<b>" + knowledge[0][
                                        6] + "</b>" + " şubemize teslim edilmiştir.</p>" +
                                    "Kargonuzu " + "<b>" + datetime_after3day + "</b>" + " tarihine kadar " + "<b>" +
                                    str(knowledge[0][5]) + "</b>" + " PNR numaranız ile teslim alabilirsiniz." +
                                    "<p><b>Şube adresimiz :</b> " + knowledge[0][6] + "  " + knowledge[0][8] + " / " +
                                    knowledge[0][9] + "</p>" +
                                    "<p><b>Adres Tarifi : </b>" + " " + knowledge[0][7] + "</p>" +
                                    "<b><i>Safety Box iyi günler diler.</i></b>" +
                                    '<br><img src="cid:image1"><br>', 'html')

            for file in os.listdir("/home/pi/Desktop/qr_images/"):
                if file.find(str(knowledge[0][4])) != -1:
                    self.image_path = os.path.join("/home/pi/Desktop/qr_images/", file)
                    print(os.path.join("/home/pi/Desktop/qr_images/", file))

            fp = open(self.image_path, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            message.attach(self.msgText)
            msgImage.add_header('Content-ID', '<image1>')
            message.attach(msgImage)

        elif mail_type == "Receiving_Cargo":
            message["To"] = knowledge[0]
            receiver_Person_ID = message["To"].split("@")
            self.msgText = MIMEText("<p><b>Sayın " + knowledge[1] + " " + knowledge[2] + ";</b></p>" +
                                    "<p><b>" + str(knowledge[3]) + "</b>" + " Takip numaralı kargonuz aşağıda resmi bulunan " +
                                    "kişi tarafından teslim alınmıştır.</p>" +
                                    "<p><b><i>SafetyBox'ı seçtiğiniz için teşekkür ederiz.</b></i></p>" +
                                    "<b><i>Bir sonraki kargonuzda görüşmek üzere. </b></i>" +
                                    '<br><img src="cid:image1"><br>', 'html')
            print("--------------------------------------")
            Path("/home/pi/Desktop/receiver_Person/" + receiver_Person_ID[0]).mkdir(parents=True,
                                                                   exist_ok=True)  # create folder if not exist
            for file in os.listdir("/home/pi/Desktop/receiver_Person/" + receiver_Person_ID[0]):
                if file.find(str(knowledge[4])) != -1:
                    self.image_path = os.path.join("/home/pi/Desktop/receiver_Person/" + receiver_Person_ID[0], file)
                    print(os.path.join("/home/pi/Desktop/receiver_Person/" + receiver_Person_ID[0], file))

            fp = open(self.image_path, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            message.attach(self.msgText)
            msgImage.add_header('Content-ID', '<image1>')
            message.attach(msgImage)


        # try:
        #     mail = smtplib.SMTP("smtp.gmail.com", 587)  # connection STMP Port 587-GmailPort
        #     mail.ehlo()  # confirm connection
        #     mail.starttls()  # gmail username/password cription
        #     mail.login("safetyboxtr@gmail.com", "Yunus.54")  # login account
        #     mail.sendmail(message["From"], message["To"], message.as_string())  # send mail
        #     print("mail başarı ile gönderildi")  # information
        #     mail.close()
        #
        # except:
        #     sys.stderr.write("bir hata oluştu")
        #     sys.stderr.flush
