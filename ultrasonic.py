# Libraries
import RPi.GPIO as GPIO
import time

# GPIO mode
GPIO.setmode(GPIO.BCM)

# GPIO PINS and other Variables
Trigger = 3  # this is pin 15, this might not work on a pin that isn't PWM lets test
Echo = 2  # this is pin 13
TriggerTime = 0.00001  # This is 0.01ms

# set GPIO in or out
GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)


def distance():
    # Pulse Trigger for set Time
    GPIO.output(Trigger, True)
    time.sleep(0.00001)
    GPIO.output(Trigger, False)
    starttime = time.time()
    stoptime = time.time()

    # Saving the Start time
    while GPIO.input(Echo) == 0:
        starttime = time.time()

    # Saving the Stop Time
    while GPIO.input(Echo) == 1:
        stoptime = time.time()

    # time difference between start and stop
    timetaken = stoptime - starttime

    # Calculate distance with sonic speed (343.2 m/s) and divide by two for there and back
    distance = (timetaken * 343.2) / 2

    return distance
