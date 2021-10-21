import time
import board
import adafruit_mpu6050

class Gyroboi:
    def __init__(self):
        self.i2c = board.I2C()
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c)

    def get_acceleration(self):
        return self.mpu.acceleration

    def get_gyro(self):
        return self.mpu.gyro

    def get_temperature(self):
        return self.mpu.temperature


if __name__ == '__main__':
    mygyro = Gyroboi()
    while True:
        try:
            print('Acceleration: ', mygyro.get_acceleration())
            print('Gyro: ', mygyro.get_gyro())
            print('Temperature :', mygyro.get_temperature())
            time.sleep(0.1)
        except KeyboardInterrupt:
            break