import tof
import ultrasonic


def scan(scanAmount):
    distances = [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]
    for x in scanAmount:
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

    for x in scanAmount:
        sensor1Average += distances[0][x]
        sensor2Average += distances[1][x]
        sensor3Average += distances[2][x]

    sensor1Average /= scanAmount
    sensor2Average /= scanAmount
    sensor3Average /= scanAmount

    return sensor1Average, sensor2Average, sensor3Average


# Update LEDs for Sensor values
def update(sensor1Average, sensor2Average, sensor3Average):
    # LED is the value for which LED pin to trigger
    LED = sensor1Average
    if sensor1Average == 0:
        LED = sensor2Average
        if sensor2Average == 0:
            LED = sensor3Average

    # Interface with LEDs needs to go here (Philipp)

    return None


