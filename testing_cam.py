import sys
from camera.dashcam import *
import time


config_fucker = CamConfigHandler()
print("CONFIG:")
config_fucker.print_config()

camera_man = Dashcam()
time.sleep(25)
camera_man.activate_video_saving()