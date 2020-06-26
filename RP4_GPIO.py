from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep


##you can remove pigpio in Project Interpreter for ignore localhost:8888 error

class RP4_GPIO():  # <===
    def __init__(self, Box_Pin):
        super().__init__()
        self.factory = PiGPIOFactory(host='192.168.1.40')
        print("IF BOX_PIN IS EQUAL TO '1', THE PROGRAM WILL CRASH. RP4 DOES NOT ALLOW REMOTE OPENING THAT PIN '1' ")
        print("YOU CAN SOLVE IT, IF YOU USE I2C COMMUNICATION")
        self.OpenBox(Box_Pin)

    def OpenBox(self, Box_Pin):
        ledR = LED(Box_Pin, pin_factory=self.factory)
        for a in range(1, 3):
            ledR.on()
            sleep(1)
            ledR.off()
            sleep(1)
