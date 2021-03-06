import RPi.GPIO as GPIO
import time


class LEDCONTROLLER:
    def __init__(self,data_pin, latch_pin, clock_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(data_pin, GPIO.OUT)
        GPIO.setup(latch_pin, GPIO.OUT)
        GPIO.setup(clock_pin, GPIO.OUT)
        self.data = data_pin
        self.latch = latch_pin
        self.clock = clock_pin

    def led_array(self, dist):
        ones = 0
        for i in range(dist):           #This starts at 0
            ones = ones + (pow(10, i))
        zeros = pow(10, (16 - dist))
        end_value = ones * zeros
        ledpattern = str(end_value)
        reverse_pattern = ledpattern[::-1]
        print(reverse_pattern)  # led Status zur Überprüfung
        GPIO.output(self.latch, 0)
        for x in range(16):
            GPIO.output(self.data, int(reverse_pattern[x]))
            # print(int(ledpattern[x]))
            GPIO.output(self.clock, 1)
            GPIO.output(self.clock, 0)
        GPIO.output(self.latch, 1)

#------------------------------------
# Beispiel: Angenommen die Distanze (dist) würde 4 Einheiten betragen:
'''
dist= 4
led_controller = LEDCONTROLLER(PIN_DATA, PIN_LATCH, PIN_CLOCK)
led_controller.led_array(dist)
'''
# this is a test edit