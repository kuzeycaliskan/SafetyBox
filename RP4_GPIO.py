from gpiozero import LED
from time import sleep

class RP4_GPIO():  # <===
    def __init__(self, Box_Pin):
        super().__init__()
        #self.setGeometry(0, 0, 500, 250)
        self.Box_Pin = Box_Pin

    def OpenBox(self):
        led = LED(self.Box_Pin)

        while True:
            led.on()
            sleep(1)
            led.off()
            sleep(1)