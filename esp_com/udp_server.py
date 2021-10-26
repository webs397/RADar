import socket
import json
import os
import time
from Crypto.Cipher import AES

SECRET = b'BenStinktWieFish'
HOME_NETWORK = {'ssid' : 'Corona-Emitting 5G Tower', 'password': 'YoushallnotPassword42'}
INTERFACE = 'wlan0'


class Networker:
    def __init__(self, mode, network_ssid, network_password):
        # mode can be either AP or ST (access point or station)
        self.mode = mode
        self.ssid = network_ssid
        self.password = network_password
        self.my_ip = None
        # connect to network
        self.connect()
        # server handler
        self.server = Server('', 6969, SECRET)
        self.server.receive_data()

    def connect(self):
        os.system('sudo iwconfig ' + INTERFACE + ' essid ' + self.ssid + ' key ' + self.password)
        #wait until connected
        time.sleep(7)



class Server:
    def __init__(self, client_ip_address, port, secret):
        self.secret = secret
        self.address = (client_ip_address,port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(self.address)
        self.udp_socket.bind(self.address)
    
    def entschluesseln(self, secret_msg):
        cipher = AES.new(self.secret , AES.MODE_ECB)
        decoded = cipher.decrypt(secret_msg)
        return decoded

    def receive_data(self):
        print('waiting for messages ...')
        while True:
            try:
                (data, addr) = self.udp_socket.recvfrom(8192)
                msg = self.entschluesseln(data)
                msg = json.loads(msg)
                print('received: ', msg, 'from :', addr)
            except KeyboardInterrupt:
                self.udp_socket.close()
    
    def close_connection(self):
        self.udp_socket.close()

'''
myserver = Server('', 6969, b'BenStinktWieFish')
myserver.receive_data()
'''

# networker aufrufen, der macht dann sein server ding vallah
if __name__ == '__main__':
    try:
        networker = Networker('ST', 'RADar', 'BDE4Life!')
    except:
        os.system('sudo iwconfig ' + INTERFACE + ' essid ' + HOME_NETWORK['ssid'] + ' key ' + HOME_NETWORK['password'])