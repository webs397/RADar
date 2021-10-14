import tof
# import ultrasonic
import time
import RPi.GPIO as GPIO
from gpiozero import LED


def scan(scanAmount):
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for x in range(scanAmount):
        # Read all Sensor distance values
        # sensor1 = ultrasonic.distance(ultrasonic.Trigger1, ultrasonic.Echo1)
        sensor1 = 3
        # sensor2 = ultrasonic.distance(ultrasonic.Trigger2, ultrasonic.Echo2)
        sensor2 = 7
        sensor3 = tof.tofsensor.readDistance()
        # sensor3 = 9
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
        LEDs[0].on()
        print('led activated: ', led_nr)
    elif led_nr == 2:
        LEDs[1].on()
        print('led activated: ', led_nr)
    elif led_nr == 3:
        LEDs[2].on()
        print('led activated: ', led_nr)
    elif led_nr == 4:
        LEDs[3].on()
        print('led activated: ', led_nr)
    elif led_nr == 5:
        LEDs[4].on()
        print('led activated: ', led_nr)
    elif led_nr == 6:
        LEDs[5].on()
        print('led activated: ', led_nr)
    elif led_nr == 7:
        LEDs[6].on()
        print('led activated: ', led_nr)
    elif led_nr == 8:
        LEDs[7].on()
        print('led activated: ', led_nr)
    elif led_nr == 9:
        LEDs[8].on()
        print('led activated: ', led_nr)
    elif led_nr == 10:
        LEDs[9].on()
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
    LEDs[0].off()
    LEDs[1].off()
    LEDs[2].off()
    LEDs[3].off()
    LEDs[4].off()
    LEDs[5].off()
    LEDs[6].off()
    LEDs[7].off()
    LEDs[8].off()
    LEDs[9].off()




# SETUP
#GPIO.setmode(GPIO.BOARD)
print('set to Board')
# LEDs = [26, 19, 13, 6, 5, 21, 20, 16, 12, 25]  # LED pin layout for GPIO
LEDs = [LED(26), LED(19), LED(13), LED(6), LED(5), LED(21), LED(20), LED(16), LED(12), LED(25)]  # LED pin layout for GPIO and new LED Library
# LEDs = [37, 35, 33, 31, 29, 40, 38, 36, 32, 22] # LED pin layout for Board
# LEDs = [LED(37), LED(35), LED(33), LED(31), LED(29), LED(40), LED(38), LED(36), LED(32), LED(22)] # LED pin layout for Board and new LED library
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
