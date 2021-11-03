import zmq
import time
from gyro.gyroalarm import *
from esp_com.pi_udp_server import *

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
    frequenz = 20
    # kamera
    context = zmq.Context()
    socket = context.socket(zmq.REQ)        #telling it, that it's a client (REQUEST)
    socket.connect("tcp://localhost:5555")  #connecting the socket
    # gyro & beschleunigungssensor
    myalarm = Alarm(frequency=frequenz)
    # networker
    networker = Networker('ST', 'RADar', 'BDE4Life!')

    # ---LOOPING---
    try:
        while True:
            # Kamera Auslöser
            if myalarm.compute_measurments():
                msg = {'reason':'danger'}
            '''
            if button pressed:
                msg = {'reason':'demand'}
            '''
            
            # Daten kriegen und die LEDs entsprechend schalten
            esp_msg = networker.server.receive_data()
            # --> philipps led-steuercode wird benötigt

            # Frequenz setzen
            time.sleep(1/frequenz)
    
    except Exception as e:
        print('there was the following error: ', e)
    finally:
        pass
