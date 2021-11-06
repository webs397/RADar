from newControl import *

inp = None
led_controller = Shifter

while True:
    try:
        print("distance: ")
        inp = int(input())
        led_controller.setLights(inp)
    except Exception as e:
        print('There was an error:', e)
        break