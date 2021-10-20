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

## Instructions