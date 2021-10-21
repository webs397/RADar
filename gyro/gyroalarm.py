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
    def __init__(self, past_seconds = 3, frequencie=20):
        self.gyro = Gyroboi()
        self.small_buffer = [[None]*4]*3
        self.counter_size = int(past_seconds/((1/frequencie) * 4))
        self.small_counter = 0
        self.past_average = []

    def calculate_average(self, new_values):
        new_average = []*3
        for i in range(0,3):
            new_average[i] = self.past_average[i] + round(new_values[i]/self.counter_size,3)
        self.past_average = new_average
        return new_average

    def fill_buffer(self):
        if self.small_counter >= 4:
            self.small_counter = 0
            new_values = [0]*3
            counter = 0
            for coord in self.small_buffer:
                for i in range(0,4):
                    new_values[counter] += round(coord[i]/4,3)
                counter += 1
            self.calculate_average(new_values)
        
        acc = self.gyro.get_acceleration()
        for i in range(0,3):
            self.small_buffer[i][self.small_counter] = acc[i]
        self.small_counter += 1        
        
    def compare_value(self, value):
        # compare the new value to the average of the wanted seconds and calculate if the should be an alarm
        return 0


if __name__ == '__main__':
    frequenz = 20
    myalarm = Alarm(frequencie=frequenz)
    while True:
        try:
            myalarm.fill_buffer()
            print(myalarm.past_average)
            time.sleep(1/frequenz)
        except KeyboardInterrupt:
            break