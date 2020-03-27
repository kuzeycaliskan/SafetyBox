import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sys
import time
import os


class SendMail():

    def __init__(self, value):

        datetime = time.strftime("%d/%m/%Y %H:%M")
        localtime = time.localtime(time.time() + 259200)
        datetime_after3day = time.strftime("%d/%m/%Y %H:%M", localtime)

        message = MIMEMultipart()

        message["From"] = "safetyboxtr@gmail.com"

        message["To"] = value[0][3]

        message["Subject"] = "SAFETYBOX İLE KARGO TESLİMİ"

        # msgText = MIMEText('<b>Sayın </b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
        msgText = MIMEText("<p><b>Sayın " + value[0][0] + " " + value[0][1] + ";</b></p>" +
                           "<p><b>" + str(value[0][4]) + "</b>" + " Takip numaralı kargonuz " + "<b>" + datetime +
                           "</b>" + " tarihinde " + "<b>" + value[0][6] + "</b>" + " şubemize teslim edilmiştir.</p>" +
                           "Kargonuzu " + "<b>" + datetime_after3day + "</b>" + " tarihine kadar " + "<b>" +
                           str(value[0][5]) + "</b>" + " PNR numaranız ile teslim alabilirsiniz." +
                           "<p><b>Şube adresimiz :</b> " + value[0][6] + "  " + value[0][8] + " / " +
                           value[0][9] + "</p>" +
                           "<p><b>Adres Tarifi : </b>" + " " + value[0][7] + "</p>" +
                           "<b><i>Safety Box iyi günler diler.</i></b> \n" +
                           '<br><img src="cid:image1"><br>', 'html')

        for file in os.listdir("/home/pi/Desktop/qr_images/"):
            if file.find(str(value[0][4])) != -1:
                self.image_path = os.path.join("qr_images/", file)
                print(os.path.join("qr_images/", file))

        fp = open(self.image_path, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()


        message.attach(msgText)
        msgImage.add_header('Content-ID', '<image1>')
        message.attach(msgImage)

        try:
            mail = smtplib.SMTP("smtp.gmail.com", 587) #connection STMP Port 587-GmailPort
            mail.ehlo() #confirm connection
            mail.starttls() #gmail username/password cription
            mail.login("safetyboxtr@gmail.com", "Yunus.54") #login account
            mail.sendmail(message["From"], message["To"], message.as_string()) #send mail
            print("mail başarı ile gönderildi") #information
            mail.close()

        except:
            sys.stderr.write("bir hata oluştu")
            sys.stderr.flush
