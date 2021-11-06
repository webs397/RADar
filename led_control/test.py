from control import *

inp = None

while True:
    try:
        print("distance: ")
        inp = input()
        dist= 5
        led_controller = LEDCONTROLLER(PIN_DATA, PIN_LATCH, PIN_CLOCK)
        led_controller.led_array(dist)
    except ValueError:
        print('input was not a number')
        break