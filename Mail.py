import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import time


class Mailinfo():



    def __init__(self,value):

        Saat = time.strftime("%d/%m/%Y %H:%M")
        localtime = time.localtime(time.time() + 259200)
        Saat3 = time.strftime("%d/%m/%Y %H:%M", localtime)

        message = MIMEMultipart()

        message["From"] = "safetyboxtr@gmail.com"

        message["To"] = value[0][3]

        message["Subject"] = "SAFETYBOX İLE KARGO TESLİMİ"


        body = "Sayın " + value[0][0] + " " + value[0][1] + ": \n" + str(value[0][4]) + " Takip numaralı kargonuz " + Saat + \
               " tarihinde " + value[0][6] + " şubemize teslim edilmiştir.\n\n" + "Kargonuzu " + Saat3 + " tarihine kadar " \
               + str(value[0][5]) + " PNR numaranız ile teslim alabilirsiniz.\n\n" + "Şube adresimiz : " + value[0][6] + " " \
               + value[0][7] + " " + value[0][8] + " " + value[0][9] + "\n" + "Safety Box iyi günler diler."



        body_text = MIMEText(body, "plain")

        message.attach(body_text)

        try:
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("safetyboxtr@gmail.com", "Yunus.54")
            mail.sendmail(message["From"], message["To"], message.as_string())
            print("mail başarı ile gönderildi")
            mail.close()

        except:
            sys.stderr.write("bir hata oluştu")
            sys.stderr.flush
