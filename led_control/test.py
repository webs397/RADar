from control import *

inp = None

while True:
    try:
        print("distance: ")
        inp = int(input())
        led_controller = LEDCONTROLLER(PIN_DATA, PIN_LATCH, PIN_CLOCK)
        led_controller.led_array(inp)
    except Exception as e:
        print('There was an error:', e)
        break