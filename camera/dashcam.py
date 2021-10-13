import json
import pycamera
import os
import io


class CamConfigHandler:
    def __init__(self):
        self.resolution = None
        self.framerate = None
        self.length = None
        self.vid_counter = None
        self.danger_counter = None
        self.data = None
        self.get_config()

    def get_config(self):
        with open('config.json','r') as config_file:
            data = json.load(config_file)
            self.data = data
            self.resolution = (data['res_width'], data['res_height'])
            self.framerate = data['framerate']
            self.length = data['length']
            self.vid_counter = data['video_counter']
            self.danger_counter = data['danger_counter']
            return self.data

    def put_config(self, vid_counter):
        self.data['video_counter'] = vid_counter
        with open('config.json','w') as config_file:
            json.dump(self.data, config_file, indent = 4)

    def print_config(self):
        print(self.resolution)
        print(self.framerate)
        print(self.length)
        print(self.vid_counter)


class Dashcam:
    def __init__(self):
        # camera instances and configuration
        self.camera = picamera.PiCamera()
        self.stream = picamera.PiCameraCircularIO(self.camera, seconds = 20)
        self.camera.resolution = None
        self.camera.framrate = None
        # using the configuration values
        self.config_handler = CamConfigHandler()
        self.camera.resolution = self.config_handler.resolution
        self.camera.framerate = self.config_handler.framerate
        self.vid_counter = self.config_handler.vid_counter
        self.danger_counter = self.config_handler.danger_counter
        # configuring folder structure
        self.folder_RADar = "/home/pi/RADar/"
        self.folder_vids = "videos/"
        self.folder_danger_vids = "danger_videos/"
        # events
        self.save_video = False
        self.save_danger = False

        self.check_folder_structure()
        self.start_recording()

    def check_folder_structure(self):
        vids = self.folder_RADar + self.folder_vids
        danger = self.folder_RADar + self.folder_danger_vids
        if not os.path.exists(vids):
            os.makedirs(vids)
            print('CREATED VIDEOS FOLDER')
        if not os.path.exists(danger):
            os.makedirs(danger)
            print('CREATED DANGER_VIDEOS FOLDER')

    def update_config(self):
        self.config_handler.put_config(self.vid_counter)

    def start_recording(self):
        vid_name = self.folder_RADar + self.folder_vids + "video%03d.h264" % self.vid_counter
        danger_name = self.folder_RADar + self.folder_danger_vids + "video%03d.h264" % self.vid_counter
        self.camera.start_recording(self.stream, format= "h264")
        try:
            while True:
                self.camera.wait_recording(1)
                if self.save_video:
                    self.camera.wait_recording(10)
                    self.stream.copy_to(vid_name)
                    self.save_video = False
                    self.vid_counter += 1
                    self.update_config()
                    print('SAVED VIDEO ON DEMAND')
                if self.save_danger:
                    self.camera.wait_recording(10)
                    self.stream.copy_to(danger_name)
                    self.danger_counter += 1
                    self.save_danger = False
                    self.update_config()
                    print('SAVED VIDEO BECAUSE OF DANGER')
        finally:
            self.camera.stop_recording()

    def activate_video_saving(self):
        self.save_video = True

    def activate_danger_saving(self):
        self.save_danger = True