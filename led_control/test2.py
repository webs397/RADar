from control import *
import time
import RPi.GPIO as GPIO

inp = None
led_controller = LEDCONTROLLER(16,20,21)

while True:
    try:
        print("distance: ")
        inp = int(input())
        led_controller.led_array(inp)
    except Exception as e:
        print('There was an error:', e)
        GPIO.cleanup()
        break