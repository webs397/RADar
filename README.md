# **RADar**
This projects aim is to make cycling in the city a safer activity, by using 2 ultrasonic sensors and one TOF sensor in order to determine how close a vehicle is coming from behind. The approximate distance is then feedbacked to the driver by a LED-stripe. There is also a dashcam recording on either demand, or in a danger situation, triggered by an acceleration- and gyro sensor.
## Requirements
### Libraries
First install pip3:  
```
sudo apt-get update  
sudo apt-get install -y python3-pip
``` 
Install ZMQ, the Raspberry Pi Camera Module  
```
sudo apt-get install python3-dev  
sudo pip3 install pyzmq  
sudo apt-get install python3-picamera
``` 

## running it
### Camera
Settings on the Raspberry Pi to be configured:  
The Camera and the rest of the program communicate over a Server/ Client Protokoll.  
To activate the Camera you'll have to create an instance of the camera with its server:  
```
from camera.dashcam import *

camera_instance = Dashcam()
```

To create a client communicating with the camera, this is the code you'll have to use:  
```
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)        #telling it, that it's a client (REQUEST)
socket.connect("tcp://localhost:5555")  #connecting the socket

package = {'reason':'demand'}           #the reason can be either 'demand' or 'danger'
print("sending request")
socket.send_json(package)               #sending the package /message

message = socket.recv()                 #getting the reply
print("Received reply: ", message)
```

As soon as the camera is getting a request it saves the last 20 seconds of recording, the coming 10 seconds, then sends a reply to the client, and then goes back to waiting for another request.