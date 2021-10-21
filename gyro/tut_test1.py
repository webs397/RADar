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
    acc = [None, None, None]
    gyro = [None, None, None]
    tmp = None
    while True:
        try:
            tmp = mygyro.get_acceleration()
            for i in range(0,3):
                acc[i] = round(tmp[i], 3)
            tmp = mygyro.get_gyro()
            for i in range(0,3):
                gyro[i] = round(tmp[i], 3)
            print('Acceleration: X:', acc[0],' Y:', acc[1], ' Z:', acc[2])
            print('Gyro:         X:', gyro[0], ' Y:', gyro[1], ' Z:', gyro[2])
            print('Temperature : ', round(mygyro.get_temperature(),3))
            time.sleep(0.1)
        except KeyboardInterrupt:
            break