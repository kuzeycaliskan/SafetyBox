from gpiozero import LED
from time import sleep

##you can remove pigpio in Project Interpreter for  ignore localhost:8888 error

class RP4_GPIO():  # <===
    def __init__(self, Box_Pin):
        super().__init__()
        self.Box_Pin = Box_Pin

        self.OpenBox()

    def OpenBox(self):
        print("RP4 Deneme" + str(self.Box_Pin))
        led = LED(self.Box_Pin)

        while True:
            led.on()
            sleep(1)
            led.off()
            sleep(1)