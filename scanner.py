# import tof
# import ultrasonic
import time
import RPi.GPIO as GPIO


def scan(scanAmount):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for x in range(scanAmount):
        # Read all Sensor distance values
        # sensor1 = ultrasonic.distance(ultrasonic.Trigger1, ultrasonic.Echo1)
        sensor1 = 2
        # sensor2 = ultrasonic.distance(ultrasonic.Trigger2, ultrasonic.Echo2)
        sensor2 = 4
        # sensor3 = tof.tofsensor.readDistance()
        sensor3 = 9
        # Cut off for ultrasonic sensor so only detect objects 2 meters close (our lane)

        # Collect Values
        sum1 += sensor1
        sum2 += sensor2
        sum3 += sensor3

    # Format the collected values
    global sensor1Average
    global sensor2Average
    global sensor3Average

    # Build average of Sensor measurements
    sensor1Average = sum1 / scanAmount
    sensor2Average = sum2 / scanAmount
    sensor3Average = sum3 / scanAmount

    print("Sensor1:")
    print(sensor1Average)
    print("Sensor2:")
    print(sensor2Average)
    print("Sensor3:")
    print(sensor3Average)

    # return sensor1Average, sensor2Average, sensor3Average


# Update LEDs for Sensor values
def update():
    # LED is the value for which LED pin to trigger
    global led
    global oldled
    global sensor1Average
    global sensor2Average
    global sensor3Average

    led = int(round(sensor1Average))
    if sensor1Average <= 2:
        led = sensor1Average
    elif sensor2Average <= 6:
        led = sensor2Average
    elif sensor3Average <= 10:
        led = sensor3Average
    else:
        led = 0

    gpio_control()


def gpio_zuordnung(led_nr):
    global LEDs
    if led_nr == 1:
        GPIO.output(LEDs[0], True)
        print('led activated: ', led_nr)
    elif led_nr == 2:
        GPIO.output(LEDs[1], False)
        print('led activated: ', led_nr)
    elif led_nr == 3:
        GPIO.output(LEDs[2], True)
        print('led activated: ', led_nr)
    elif led_nr == 4:
        GPIO.output(LEDs[3], True)
        print('led activated: ', led_nr)
    elif led_nr == 5:
        GPIO.output(LEDs[4], True)
        print('led activated: ', led_nr)
    elif led_nr == 6:
        GPIO.output(LEDs[5], True)
        print('led activated: ', led_nr)
    elif led_nr == 7:
        GPIO.output(LEDs[6], True)
        print('led activated: ', led_nr)
    elif led_nr == 8:
        GPIO.output(LEDs[7], True)
        print('led activated: ', led_nr)
    elif led_nr == 9:
        GPIO.output(LEDs[8], True)
        print('led activated: ', led_nr)
    elif led_nr == 10:
        GPIO.output(LEDs[9], True)
        print('led activated: ', led_nr)
    else:
        print('something went wrong')


# Connection to LEDs
def gpio_control():
    global led
    global oldled
    print("led and old led")
    print(led, oldled)
    if led != oldled:
        turn_leds_off()
        oldled = led
    gpio_zuordnung(led)


def turn_leds_off():
    GPIO.output(LEDs[0], False),  # this is pin 37
    GPIO.output(LEDs[1], False),  # this is pin 35
    GPIO.output(LEDs[2], False),  # this is pin 33
    GPIO.output(LEDs[3], False),  # this is pin 31
    GPIO.output(LEDs[4], False),  # this is pin 29
    GPIO.output(LEDs[5], False),  # this is pin 40
    GPIO.output(LEDs[6], False),  # this is pin 38
    GPIO.output(LEDs[7], False),  # this is pin 36
    GPIO.output(LEDs[8], False),  # this is pin 32
    GPIO.output(LEDs[9], False),  # this is pin 22


def led_setup():
    GPIO.setup(LEDs[0], GPIO.OUT)  # this is pin 37
    GPIO.setup(LEDs[1], GPIO.OUT)  # this is pin 35
    GPIO.setup(LEDs[2], GPIO.OUT)  # this is pin 33
    GPIO.setup(LEDs[3], GPIO.OUT)  # this is pin 31
    GPIO.setup(LEDs[4], GPIO.OUT)  # this is pin 29
    GPIO.setup(LEDs[5], GPIO.OUT)  # this is pin 40
    GPIO.setup(LEDs[6], GPIO.OUT)  # this is pin 38
    GPIO.setup(LEDs[7], GPIO.OUT)  # this is pin 36
    GPIO.setup(LEDs[8], GPIO.OUT)  # this is pin 32
    GPIO.setup(LEDs[9], GPIO.OUT)  # this is pin 22


# SETUP
GPIO.setmode(GPIO.BCM)
print('set to bcm')
LEDs = [25, 24, 23, 22, 21, 29, 28, 27, 26, 6]  # LED pin layout for GPIO
#   LEDs = [37, 35, 33, 31, 29, 40, 38, 36, 32, 22] # LED pin layout for Board
led_setup()
turn_leds_off()

oldled = 0
led = 0
sensor1Average = 0
sensor2Average = 0
sensor3Average = 0


try:
    while True:
        scan(5)
        update()
        time.sleep(5)
        print("Cycle done!!!!!!!!!!!!!")
finally:
    GPIO.cleanup()
