import sys
from camera.dashcam import *
import time
import zmq


config_fucker = CamConfigHandler()
print("CONFIG:")
config_fucker.print_config()


time.sleep(25)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connetct("tcp://localhost:5555")

package = {'reason':'demand'}

print("sending request")
socket.send_json(package)

message = socket.recv()
print("Received reply: ", message)