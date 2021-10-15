# Libraries
import RPi.GPIO as GPIO
import time

# GPIO mode
GPIO.setmode(GPIO.BCM)

# GPIO PINS and other Variables
Trigger1 = 22  # this is pin 15, this might not work on a pin that isn't PWM lets test
Echo1 = 27  # this is pin 13
Trigger2 = 24  # this is pin 18, this might not work on a pin that isn't PWM lets test
Echo2 = 23  # this is pin 16
TriggerTime = 0.00001  # This is 0.01ms

# set GPIO in or out
GPIO.setup(Trigger1, GPIO.OUT)
GPIO.setup(Echo1, GPIO.IN)

GPIO.setup(Trigger2, GPIO.OUT)
GPIO.setup(Echo2, GPIO.IN)


def distance(Trigger, Echo):
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
