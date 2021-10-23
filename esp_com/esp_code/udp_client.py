'''
----------------------------------------------------------
THIS IS NEAT LITTLE SCRIPT SHOULD ONLY GO ON THE ESP32
----------------------------------------------------------
'''

import network
import socket
import json
from machine import Pin
from time import sleep
from machine import Timer
from ucryptolib import aes

green = Pin(0, Pin.OUT)
yellow = Pin(23,Pin.OUT)
red = Pin(2,Pin.OUT)
blue = Pin(5, Pin.OUT)

def turn_all_off():
    green.value(0)
    yellow.value(0)
    red.value(0)
    blue.value(0)

class Networker:
    def __init__(self, network_ssid, network_password):
        self.ssid = network_ssid
        self.password = network_password
        self.ip_address = None
        
        turn_all_off()
        self.do_connect(self.ssid, self.password)
        
    def do_connect(self, ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network')
            yellow.value(1)
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                pass
        self.ip_address = wlan.ifconfig()[0]
        print('network config:', wlan.ifconfig())
        yellow.value(0)
        green.value(1)


class Client:
    def __init__(self, server_ip_address, port, secret):
        self.server_ip = (server_ip_address, port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cipher = aes(secret,1)
    
    def verschluesseln(self, msg):
        pad = 16 - len(msg) % 16
        msg = msg + " "*pad
        encrypted = self.cipher.encrypt(msg)
        return encrypted
        
    def send_udp(self, data):
        data = json.dumps(data)
        msg = self.verschluesseln(data)
        self.udp_socket.sendto(msg, self.server_ip)
        blue.value(1)
        sleep(0.5)
        blue.value(0)
             
    def close_connection(self):
        self.udp_socket.close()


# data has to be an python dict        
# Raspi:  192.168.0.55        
networker = Networker('Corona-Emitting 5G Tower', 'YoushallnotPassword42')
myclient = Client('192.168.0.55', 6969,b'BenStinktWieFish')
abstaende = {'tof': 9, 'u1' : 4 , 'u2': 2}
myclient.send_udp(abstaende)
myclient.close_connection()

