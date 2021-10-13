import tof
import ultrasonic
import RPi.GPIO as GPIO


def scan(scanAmount):
    distances = [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]
    for x in range(scanAmount):
        # Read all Sensor distance values
        sensor1 = ultrasonic.distance(ultrasonic.Trigger1, ultrasonic.Echo1)
        sensor2 = ultrasonic.distance(ultrasonic.Trigger2, ultrasonic.Echo2)
        sensor3 = tof.readDistance()

        # Cut off for ultrasonic sensor so only detect objects 2 meters close (our lane)
        if sensor1 >= 2:
            sensor1 = 0

        if sensor2 > 6:
            sensor2 = 0

        if sensor3 > 10:
            sensor3 = 0

        # Collect Values in sensor array
        distances[0][x] = sensor1
        distances[1][x] = sensor2
        distances[2][x] = sensor3

    # Format the collected values
    sensor1Average = 0
    sensor2Average = 0
    sensor3Average = 0

    for x in range(scanAmount):
        sensor1Average += distances[0][x]
        sensor2Average += distances[1][x]
        sensor3Average += distances[2][x]

    sensor1Average /= scanAmount
    sensor2Average /= scanAmount
    sensor3Average /= scanAmount

    print("Sensor1:")
    print(sensor1Average)
    print("Sensor2:")
    print(sensor2Average)
    print("Sensor3:")
    print(sensor3Average)

    return sensor1Average, sensor2Average, sensor3Average


# Update LEDs for Sensor values
def update(sensor1Average, sensor2Average, sensor3Average):
    # LED is the value for which LED pin to trigger
    led = sensor1Average
    if sensor1Average == 0:
        led = sensor2Average
        if sensor2Average == 0:
            led = sensor3Average

    gpio_control()
    return None


# Connection to LEDs
def gpio_control(led):
    switcher = \
        {
            1: GPIO.output(25, True),  # this is pin 37
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

    return switcher.get(led, "nothing")


update(scan(5))

