from newControl import *
import time
inp = None
led_controller = Shifter()

while True:
    try:
        #print("distance: ")
        #inp = int(input())
        for i in range(1,21):
            led_controller.setLights(i)
            time.sleep(1)
    except Exception as e:
        print('There was an error:', e)
        break