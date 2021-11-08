import zmq
import time
from gyro.gyroalarm import *
from esp_com.pi_udp_server import *
from led_control.olliscontroller import *
from wifi_helper import *
import RPi.GPIO as GPIO
from internet_finder import *
import os


# ---EXAMPLE PACKAGE---
# package = {'reason':'demand'}           #the reason can be either 'demand' or 'danger'

def req_and_resp(package):
    #print("sending request")
    socket.send_json(package)               #sending the package /message
    message = socket.recv()                 #getting the reply
    #print("Received reply: ", message)
    return message

if __name__ == '__main__':
    # ---HANDLER---
    # button & LED
    GREEN_LED = 11
    BLUE_LED = 9
    BUTTON = 10
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((GREEN_LED, BLUE_LED), GPIO.OUT)
    GPIO.setup(BUTTON, GPIO.IN)
    just_switched = True
    button_status = 0 # 0: idle, 1: connect & receive, 2: upload
    #frequenz
    frequenz = 20
    # kamera
    context = zmq.Context()
    socket = context.socket(zmq.REQ)        #telling it, that it's a client (REQUEST)
    socket.connect("tcp://localhost:5555")  #connecting the socket
    # gyro & beschleunigungssensor
    myalarm = Alarm(frequency=frequenz)
    # networker
    networker = Networker('ST', 'RADar', 'BDE4Life!')
    # led controller
    PIN_DATA = 16
    PIN_LATCH = 20
    PIN_CLOCK = 21
    led_controller = LEDCONTROLLER(PIN_DATA, PIN_LATCH, PIN_CLOCK)
    
    # ---LOOPING---
    try:
        while True:
            # Kamera Auslöser
            if GPIO.input(BUTTON) == GPIO.HIGH:
                button_status +=1
                start = time.time()
                stop = None
                just_switched = True
                if button_status >=3:
                    button_status = 0
                while True:
                    if GPIO.input(BUTTON) == GPIO.LOW:
                        stop = time.time()
                        break
                passed_time = stop - start
                if passed_time >=5:
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(BLUE_LED, GPIO.LOW)
                    time.sleep(0.25)
                    GPIO.output(GREEN_LED, GPIO.HIGH)
                    GPIO.output(BLUE_LED, GPIO.HIGH)
                    time.sleep(0.25)
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(BLUE_LED, GPIO.LOW)
                    time.sleep(0.25)
                    GPIO.output(GREEN_LED, GPIO.HIGH)
                    GPIO.output(BLUE_LED, GPIO.HIGH)
                    time.sleep(0.25)
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(BLUE_LED, GPIO.LOW)
                    time.sleep(0.25)
                    GPIO.output(GREEN_LED, GPIO.HIGH)
                    GPIO.output(BLUE_LED, GPIO.HIGH)
                    time.sleep(0.25)
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(BLUE_LED, GPIO.LOW)
                    time.sleep(0.25)
                    break
                time.sleep(1)

            if button_status == 0:
                # IDLE
                print('status: IDLE')
                if just_switched:
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(BLUE_LED, GPIO.LOW)
                    just_switched = False
                
            elif button_status == 1:
                # CONNECT & RECEIVE
                print('status: CONNECT & REICEIVE')
                if just_switched:
                    GPIO.output(GREEN_LED, GPIO.HIGH)
                    GPIO.output(BLUE_LED, GPIO.LOW)
                    just_switched = False
                if myalarm.compute_measurments():
                    msg = {'reason':'danger'}

                '''
                if button pressed:
                    msg = {'reason':'demand'}
                '''
                    
                # Daten kriegen und die LEDs entsprechend schalten
                esp_msg = networker.server.receive_data()
                print(esp_msg)
                # --> philipps led-steuercode wird benoetigt
                #print(esp_msg)
                if not(esp_msg == None):
                    led_controller.disp_leds(int(esp_msg.get('Led Value: ')))
                
            if button_status == 2:
                # UPLOAD
                print('status: UPLOAD')
                if just_switched:
                    GPIO.output(GREEN_LED, GPIO.LOW)
                    GPIO.output(BLUE_LED, GPIO.HIGH)
                    just_switched = False

                print('has to be implemented')
                button_status = 0

            # Frequenz setzen
            time.sleep(1/frequenz)
    except KeyboardInterrupt:
        print('aborting')
    except Exception as e:
        print('there was the following error: ', e)
    finally:
        print("I'M OUT")
        GPIO.cleanup()
        pass 
