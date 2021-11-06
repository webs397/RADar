from control import *

dist= 5
led_controller = LEDCONTROLLER(PIN_DATA, PIN_LATCH, PIN_CLOCK)
led_controller.led_array(dist)