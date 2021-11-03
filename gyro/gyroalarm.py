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
    def __init__(self,values_per_second=10, frequency=40):
        self.gyro = Gyroboi()
        self.max_counter = int((1/values_per_second)/(1/frequency))
        self.small_buffer = {'x': [None]*self.max_counter,'y': [None]*self.max_counter,'z': [None]*self.max_counter}
        self.small_counter = 0

    def compute_measurments(self):
        if self.small_counter >= self.max_counter:
            self.small_counter = 0
            new_values = [0]*3
            counter = 0
            for _,liste in self.small_buffer.items():
                for i in range(0,self.max_counter):
                    new_values[counter] += round(liste[i]/4,2)
                counter += 1
            return self.calculate_alarm(new_values)
        else:
            acc = self.gyro.get_acceleration()
            self.small_buffer['x'][self.small_counter] = round(acc[0],2)
            self.small_buffer['y'][self.small_counter] = round(acc[1],2)
            self.small_buffer['z'][self.small_counter] = round(acc[2],2)
            self.small_counter += 1
        
    def calculate_alarm(self,values):
        # look if the acceleration on the y axis is higher than 3.5 m/s^2
        # the following line can be uncommented for debug purposes
        #print('X: ', values[0], '\tY: ', values[1], '\tZ: ', values[2])
        if values[1] >= 3.5:
            return True
        else:
            return False


if __name__ == '__main__':
    frequenz = 40                           # set the frequency on which the program runs
    myalarm = Alarm(frequency=frequenz)
    while True:
        try:
            alarm = myalarm.compute_measurments()   # either True or Falses
            time.sleep(1/frequenz)      
        except KeyboardInterrupt:
            break