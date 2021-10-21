import time
import queue
import board
import adafruit_mpu6050

class Gyroboi:
    def __init__(self):
        self.i2c = board.I2C()
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c)

    def get_acceleration(self):
        # in m/s^s
        return self.mpu.acceleration

    def get_gyro(self):
        # in °/s
        return self.mpu.gyro

    def get_temperature(self):
        return self.mpu.temperature


class Alarm:
    def __init__(self, frequencie=40):
        self.gyro = Gyroboi()
        self.max_counter = int(0.1/(1/frequencie))
        self.small_buffer = [[None]*self.max_counter]*3
        self.small_counter = 0

    def fill_buffer(self):
        if self.small_counter >= 4:
            self.small_counter = 0
            new_values = [0]*3
            counter = 0
            for coord in self.small_buffer:
                for i in range(0,4):
                    new_values[counter] += round(coord[i]/4,3)
                counter += 1
            self.calculate_alarm(new_values)
        acc = self.gyro.get_acceleration()
        for i in range(0,3):
            self.small_buffer[i][self.small_counter] = acc[i]
        self.small_counter += 1        
        
    def calculate_alarm(self,values):
        # look if the acceleration on the y axis is higher than 3.5 m/s^2
        print('X: ', values[0], '\tY: ', values[1], '\tZ: ', values[2])
        if values[1] >= 3.5:
            print('ALARM')


if __name__ == '__main__':
    frequenz = 40
    myalarm = Alarm(frequencie=frequenz)
    while True:
        try:
            myalarm.fill_buffer()
            time.sleep(1/frequenz)
        except KeyboardInterrupt:
            break