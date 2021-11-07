from machine import Pin, I2C
import time
import json

# ToF Setup
i2c0 = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

print(i2c0.scan())
address = 16
getLidarDataCmd = bytearray([0x5A, 0x05, 0x00, 0x01, 0x60])

# Ultrasonic Setup
trigger1_pin = 15  # Pin D8
trigger2_pin = 12  # Pin D6
echo1_pin = 13  # Pin D5
echo2_pin = 14  # Pin D7
trigger_time = 0.00001  # This is 0.01ms

# set GPIO in or out
trigger1 = machine.Pin(trigger1_pin, machine.Pin.OUT)
trigger1.off()
echo1 = machine.Pin(echo1_pin,
                    machine.Pin.IN)  # Dont know if Pull-Up is needed or not (echo1_pin, Pin.IN, Pin.PULL_UP) if so

trigger2 = machine.Pin(trigger2_pin, machine.Pin.OUT)
trigger2.off()
echo2 = machine.Pin(echo2_pin,
                    machine.Pin.IN)  # # Dont know if Pull-Up is needed or not (echo2_pin, Pin.IN, Pin.PULL_UP) if so

sensor1Average = 0.0
sensor2Average = 0.0
sensor3Average = 0.0


def getLidarData(I2C, I2C_ADDR, CMD):
    temp = bytes(9)

    I2C.writeto(I2C_ADDR, CMD)
    temp = I2C.readfrom(16, 9)

    if temp[0] == 0x59 and temp[1] == 0x59:
        tofDistance = temp[2] + temp[3] * 256
        strength = temp[4] + temp[5] * 256
        temperature = (temp[6] + temp[7] * 256) / 8 - 256
        print("Distance: =%5dcm, Strength = %5d, Temperature = %5d°C" % (tofDistance, strength, temperature))
    return tofDistance


def SonicDistance(trigger, echo):
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()

    while echo.value() == 0:
        pass
    t1 = time.ticks_us()
    while echo.value() == 1:
        pass
    t2 = time.ticks_us()
    cm = (t2 - t1) / 58.0
    print(cm)
    time.sleep(2)

    return SonicDistance


def scan(scanAmount):
    # print('scanning...')
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for x in range(scanAmount):
        # Read all Sensor distance values
        print('\t..sonics')
        sensor1 = SonicDistance(trigger1, echo1)
        sensor2 = SonicDistance(trigger2, echo2)
        print('\t..lidar')
        sensor3 = getLidarData(i2c0, address, getLidarDataCmd) / 100.00  # convert cm to m

        # Collect Values
        sum1 += sensor1
        sum2 += sensor2
        sum3 += sensor3

    # Format the collected values

    # Build average of Sensor measurements
    sensor1Average = sum1 / scanAmount
    sensor2Average = sum2 / scanAmount
    sensor3Average = sum3 / scanAmount

    print("-----------------------")
    print("Sensor1:")
    print(sensor1Average)
    print("Sensor2:")
    print(sensor2Average)
    '''
    print("Sensor3:")
    print(sensor3Average)
    print("-----------------------")
    '''
    return sensor1Average, sensor2Average, sensor3Average


# Update LEDs for Sensor values and package activated sensor and led value as JSON
def update():
    # LED is the value for which LED pin to trigger
    global sensor1Average
    global sensor2Average
    global sensor3Average

    # Sensor Cutoffs (using ceil so the number is rounded up)
    if sensor1Average <= 2:
        if sensor1Average < 0.5:
            led = int(sensor1Average)
            activatedSensor = "Sensor1"
        else:
            led = int(round(sensor1Average))
            activatedSensor = "Sensor1"
    elif sensor2Average <= 4:
        led = int(sensor2Average)
        activatedSensor = "Sensor2"
    elif sensor3Average <= 10:
        led = int(sensor3Average)
        activatedSensor = "Sensor3"
    else:
        led = 0

    data = {"Activated Sensor: ": activatedSensor, "Led Value: ": led}
    #data = {"Lidar: ": sensor3Average}
    # message = json.dumps(data)

    return data


# BEISPIELCODE




