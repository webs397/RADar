import tof
import ultrasonic
import time
import RPi.GPIO as GPIO

GPIO.setup(25, GPIO.OUT)  # this is pin 37
GPIO.setup(24, GPIO.OUT)  # this is pin 35
GPIO.setup(23, GPIO.OUT)  # this is pin 33
GPIO.setup(22, GPIO.OUT)  # this is pin 31
GPIO.setup(21, GPIO.OUT)  # this is pin 29
GPIO.setup(29, GPIO.OUT)  # this is pin 40
GPIO.setup(28, GPIO.OUT)  # this is pin 38
GPIO.setup(27, GPIO.OUT)  # this is pin 36
GPIO.setup(26, GPIO.OUT)  # this is pin 32
GPIO.setup(6, GPIO.OUT)  # this is pin 22

GPIO.output(25, False),  # this is pin 37
GPIO.output(24, False),  # this is pin 35
GPIO.output(23, False),  # this is pin 33
GPIO.output(22, False),  # this is pin 31
GPIO.output(21, False),  # this is pin 29
GPIO.output(29, False),  # this is pin 40
GPIO.output(28, False),  # this is pin 38
GPIO.output(27, False),  # this is pin 36
GPIO.output(26, False),  # this is pin 32
GPIO.output(6, False),  # this is pin 22

oldled = 0
led = 0
sensor1Average = 0
sensor2Average = 0
sensor3Average = 0

def scan(scanAmount):
    distances = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    for x in range(scanAmount):
        # Read all Sensor distance values
        # sensor1 = ultrasonic.distance(ultrasonic.Trigger1, ultrasonic.Echo1)
        sensor1 = 2
        # sensor2 = ultrasonic.distance(ultrasonic.Trigger2, ultrasonic.Echo2)
        sensor2 = 1
        # sensor3 = tof.tofsensor.readDistance()
        sensor3 = 1
        # Cut off for ultrasonic sensor so only detect objects 2 meters close (our lane)
        if sensor1 >= 2:
            sensor1 = 0
        if sensor2 > 6:
            sensor2 = 0
        if sensor3 > 10:
            sensor3 = 0
        # Collect Values in sensor array
        distances[0][x - 1] = sensor1
        distances[1][x - 1] = sensor2
        distances[2][x - 1] = sensor3

    # Format the collected values
    global sensor1Average
    global sensor2Average
    global sensor3Average

    for x in range(scanAmount):
        sensor1Average += distances[0][x - 1]
        sensor2Average += distances[1][x - 1]
        sensor3Average += distances[2][x - 1]

    sensor1Average /= scanAmount
    sensor2Average /= scanAmount
    sensor3Average /= scanAmount

    print("Sensor1:")
    print(sensor1Average)
    print("Sensor2:")
    print(sensor2Average)
    print("Sensor3:")
    print(sensor3Average)

    #return sensor1Average, sensor2Average, sensor3Average


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
    return None


def gpio_zuordnung(led_nr):
    if led_nr == 1:
        GPIO.output(25, True)
    elif led_nr == 2:
        GPIO.output(24, True)
    elif led_nr == 3:
        GPIO.output(23, True)
    elif led_nr == 2:
        GPIO.output(22, True)
    elif led_nr == 2:
        GPIO.output(21, True)
    elif led_nr == 2:
        GPIO.output(29, True)
    elif led_nr == 2:
        GPIO.output(28, True)
    elif led_nr == 2:
        GPIO.output(27, True)
    elif led_nr == 2:
        GPIO.output(26, True)
    elif led_nr == 2:
        GPIO.output(6, True)
    else:
        print('something went wrong')
    print('led activated: ', led_nr)


# Connection to LEDs
def gpio_control():
    global led
    global oldled
    print("led and old led")
    print(led, oldled)
    if led != oldled:
        GPIO.output(25, False),  # this is pin 37
        GPIO.output(24, False),  # this is pin 35
        GPIO.output(23, False),  # this is pin 33
        GPIO.output(22, False),  # this is pin 31
        GPIO.output(21, False),  # this is pin 29
        GPIO.output(29, False),  # this is pin 40
        GPIO.output(28, False),  # this is pin 38
        GPIO.output(27, False),  # this is pin 36
        GPIO.output(26, False),  # this is pin 32
        GPIO.output(6, False),  # this is pin 22
        oldled = led
    gpio_zuordnung(led)

'''
    switcher = \
        {  # this for some reason activates 1,5,7,10 (should just be 5)
            1: GPIO.output(25, True),
            2: GPIO.output(24, True),  # this is pin 35
            3: GPIO.output(23, True),  # this is pin 33
            4: GPIO.output(22, True),  # this is pin 31
            5: GPIO.output(21, True),  # this is pin 29
            6: GPIO.output(29, True),  # this is pin 40
            7: GPIO.output(28, True),  # this is pin 38
            8: GPIO.output(27, True),  # this is pin 36
            9: GPIO.output(26, True),  # this is pin 32
            10: GPIO.output(6, True),  # this is pin 22
        }

    switcher[led]()'''


while True:
    scan(5)
    update()
    time.sleep(1)
