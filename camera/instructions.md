# Camera
## running it
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