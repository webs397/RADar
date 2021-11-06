import RPi.GPIO as GPIO
import time

class LEDCONTROLLER:
    def __init__(self, data_pin, latch_pin, clock_pin):
        self.data = data_pin
        self.latch = latch_pin
        self.clock = clock_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((self.data,self.latch,self.clock),GPIO.OUT)
        self.bithelper = {}
        for i in range(1,21):
            self.bithelper[str(i)] = "1"*i + "0"*(20-i)
        
    def shift_update(self, input):
        # input has to be an 24 bit string containing 0 or 1
        GPIO.output(self.clock,0)
        GPIO.output(self.latch,0)
        GPIO.output(self.clock,1)

        # load the data in reverse order
        for i in range(23,-1,-1):
            GPIO.output(self.clock,0)
            GPIO.output(self.data,int(input[i]))
            GPIO.output(self.clock,1)

        # put latch up to store data on register
        GPIO.output(self.clock, 0)
        GPIO.output(self.latch,1)
        GPIO.output(self.clock,1)

    def disp_leds(self,led):
        # number from 1 - 20
        self.shift_update(self.bithelper[str(led)])
        print(self.bithelper[str(led)])

    def my_end(self):
        GPIO.cleanup()