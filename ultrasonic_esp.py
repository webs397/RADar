# Libraries
from machine import Pin
import time

# GPIO mode
# GPIO.setmode(GPIO.BCM)

# GPIO PINS and other Variables

trigger1_pin = 16  # Pin D0
trigger2_pin = 12  # Pin D6
echo1_pin = 14  # Pin D5
echo2_pin = 13  # Pin D7
trigger_time = 0.00001  # This is 0.01ms

# set GPIO in or out
trigger1 = Pin(trigger1_pin, Pin.OUT)
echo1 = Pin(echo1_pin, Pin.IN, None)  # Dont know if Pull-Up is needed or not (echo1_pin, Pin.IN, Pin.PULL_UP) if so

trigger2 = Pin(trigger2_pin, Pin.OUT)
echo2 = Pin(echo2_pin, Pin.IN, None)  # # Dont know if Pull-Up is needed or not (echo2_pin, Pin.IN, Pin.PULL_UP) if so


def distance(trigger, echo):
    # Pulse Trigger for set Time
    trigger.on()
    time.sleep(0.00001)
    trigger.off()
    start_time = time.time()
    stop_time = time.time()

    # Saving the Start time
    while echo.IN == 0:
        start_time = time.time()

    # Saving the Stop Time
    while echo.IN == 1:
        stop_time = time.time()

    # time difference between start and stop
    time_taken = stop_time - start_time

    # Calculate distance with sonic speed (343.2 m/s) and divide by two for there and back
    distance = (time_taken * 343.2) / 2

    return distance
