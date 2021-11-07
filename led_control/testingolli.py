from olliscontroller import *
import time
inp = None
led_controller = LEDCONTROLLER(13,6,5)
counter = 0
try:
    while True:
        print("distance: ")
        inp = int(input())
        led_controller.disp_leds(inp) 
except Exception as e:
    print('There was an error:', e)
finally:
    led_controller.my_end()