import sys
from camera.dashcam import *


config_fucker = CamConfigHandler()
print("CONFIG:")
config_fucker.print_config()

camera_man = Dashcam()
camera_man.activate_video_saving()