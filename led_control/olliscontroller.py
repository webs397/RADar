import RPi.GPIO as GPIO
from time import sleep

# WE NEED GPIO.BCM

class LEDCONTROLLER:
    def __init__(self, data_pin, latch_pin, clock_pin):
        self.data = data_pin
        self.latch = latch_pin
        self.clock = clock_pin
        #GPIO.setmode(GPIO.BCM)
        GPIO.setup((self.data,self.latch,self.clock),GPIO.OUT)
        self.bithelper = {
            '20' : '000000000000000000000000',
            '19' : '100000000000000000000000',
            '18' : '110000000000000000000000',
            '17' : '111000000000000000000000',
            '16' : '111100000000000000000000',
            '15' : '111110000000000000000000',
            '14' : '111111000000000000000000',
            '13' : '111111100000000000000000',
            '12' : '111111110000000000000000',
            '11' : '111111111000000000000000',
            '10' : '111111111100000000000000',
            '9' : '111111111110000000000000',
            '8' : '111111111111000000000000',
            '7' : '111111111111100000000000',
            '6' : '111111111111110000000000',
            '5' : '111111111111111000000000',
            '4' : '111111111111111100000000',
            '3' : '111111111111111110000000',
            '2' : '111111111111111111000000',
            '1' : '111111111111111111100000',
            '0' : '111111111111111111110000',
        }

    def shift_update(self, input):
        # input has to be an 24 bit string containing 0 or 1
        GPIO.output(self.clock,0)
        sleep(0.001)
        GPIO.output(self.latch,0)
        sleep(0.001)
        GPIO.output(self.clock,1)
        sleep(0.001)

        '''
        for i in range(23,-1,-1):
            GPIO.output(self.clock,0)
            GPIO.output(self.data,0)
            GPIO.output(self.clock,1)
        '''

        # load the data in reverse order
        for i in range(23,-1,-1):
            GPIO.output(self.clock,0)
            sleep(0.001)
            GPIO.output(self.data,int(input[i]))
            sleep(0.001)
            GPIO.output(self.clock,1)
            sleep(0.001)
            #GPIO.output(self.data, 0)

        # put latch up to store data on register
        GPIO.output(self.clock, 0)
        sleep(0.001)
        GPIO.output(self.latch,1)
        sleep(0.001)
        GPIO.output(self.clock,1)
        sleep(0.001)

    def disp_leds(self,led):
        # number from 1 - 20
        self.shift_update(self.bithelper[str(led)])
        print(self.bithelper[str(led)])
        '''
        self.twentyfour_zeros()
        for _ in range(0,led):
            self.one_in()
        '''

    def my_end(self):
        GPIO.cleanup()

    def one_in(self):
        # input has to be an 24 bit string containing 0 or 1
        GPIO.output(self.clock,0)
        GPIO.output(self.latch,0)
        GPIO.output(self.clock,1)

        GPIO.output(self.clock,0)
        GPIO.output(self.data,1)
        GPIO.output(self.clock,1)
        GPIO.output(self.data,0)

        GPIO.output(self.clock, 0)
        GPIO.output(self.latch,1)
        GPIO.output(self.clock,1)

    def twentyfour_zeros(self):
        GPIO.output(self.clock,0)
        GPIO.output(self.latch,0)
        GPIO.output(self.clock,1)

        for _ in range(0,24):
            GPIO.output(self.clock,0)
            GPIO.output(self.data,0)
            GPIO.output(self.clock,1)

        GPIO.output(self.clock, 0)
        GPIO.output(self.latch,1)
        GPIO.output(self.clock,1)