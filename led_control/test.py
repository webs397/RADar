from newControl import *
import RPi.GPIO as GPIO
import time
inp = None
led_controller = Shifter()

while True:
    try:
        print("distance: ")
        inp = int(input())
        led_controller.setLights(inp)
    except Exception as e:
        print('There was an error:', e)
        GPIO.cleanup()
        break