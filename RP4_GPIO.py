import gpiozero
from gpiozero.pins.mock import MockFactory
from gpiozero import LED
from time import sleep

##you can remove pigpio in Project Interpreter for  ignore localhost:8888 error

gpiozero.Device.pin_factory = MockFactory()

class RP4_GPIO():  # <===
    def __init__(self, Box_Pin):
        super().__init__()


        self.OpenBox(Box_Pin)

    def OpenBox(self, Box_Pin):
        print("RP4 Deneme" + str(Box_Pin))
        led = LED(Box_Pin)

        for a in range(1,5):
            led.on()
            sleep(1)
            led.off()
            sleep(1)