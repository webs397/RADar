import network
import socket
import json
from machine import Pin
from time import sleep
from machine import Timer
from ucryptolib import aes

SECRET = b'BenStinktWieFish'
PARTNER_NAME = 'raspberrypi'

class LEDController:
    def __init__(self, greenPin, yellowPin, redPin, bluePin):
        # the Pin numbers are equal to the GPIO Number of the Pin
        self.green = Pin(greenPin, Pin.OUT)
        self.yellow = Pin(yellowPin,Pin.OUT)
        self.red = Pin(redPin,Pin.OUT)
        self.blue = Pin(bluePin, Pin.OUT)
        # all off
        self.control_leds(0,0,0,0)
 
    def control_leds(green, yellow, red, blue):
        self.green.value(green)
        self.yellow.value(yellow)
        self.red.value(red)
        self.blue.value(blue)


class Networker:
    def __init__(self, mode, network_ssid, network_password):
        # mode = STA (station) or AP (access point)
        self.mode = mode
        self.ssid = network_ssid
        self.password = network_password
        self.ip_address = None
        self.network = None
        # LED handler
        #self.led_control = LEDController(0,23,2,5)
        # create or connect network
        self.do_connect(self.ssid, self.password)
        # Client Handler
        self.client = Client(self.ip_address, PARTNER_NAME, 6969, SECRET)
               
    def do_connect(self, ssid, password):
        if self.mode == 'AP':
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            ap.config(essid = ssid, password = password, authmode = 3)
            while ap.active() == False:
                pass
            self.network = ap
            self.ip_address = ap.ifconfig()[0]
            print('network config: ', ap.ifconfig())
            # LEDs
        elif self.mode == 'STA':
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            if not wlan.isconnected():
                print('connecting to network')
                # LED
                wlan.connect(ssid, password)
                while not wlan.isconnected():
                    pass
            self.ip_address = wlan.ifconfig()[0]
            print('network config:', wlan.ifconfig())
            self.network = wlan
            #LEDs
                    

class Client:
    def __init__(self, own_ip, partnername, port, secret):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.my_ip = own_ip
        self.partner_ip = None
        self.find_partner(self.my_ip, partnername)
        self.server_ip = (self.partner_ip, port)
        self.cipher = aes(secret,1)
    
    def verschluesseln(self, msg):
        pad = 16 - len(msg) % 16
        msg = msg + " "*pad
        encrypted = self.cipher.encrypt(msg)
        return encrypted
        
    def send_udp(self, msg):
        data = json.dumps(msg)
        msg = self.verschluesseln(data)
        self.udp_socket.sendto(msg, self.server_ip)
             
    def close_connection(self):
        self.udp_socket.close()
        
    def find_partner(self, own_ip, partner):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (own_ip, 5556)
        print('starting up on address: ', server_address)
        sock.bind(server_address)
        sock.listen(1)
        client_address = None
        while True:
            print('waiting for connection')
            connection, client_address = sock.accept()
            try:
                print('connection from: ', client_address)
                data = connection.recv(16)
                if data:
                    print(data)
                    connection.sendall(b'hi i am esp32')
                    break
                else:
                    print('no more data')
                    break
            finally:   
                connection.close()
        self.partner_ip = client_address[0]
        print('found: ', partner, 'on IP: ', self.partner_ip)

