import socket
import json
import os
import time
from Crypto.Cipher import AES
import wifi

SECRET = b'BenStinktWieFish'
HOME_NETWORK = {'ssid' : 'Corona-Emitting 5G Tower', 'password': 'YoushallnotPassword42'}
INTERFACE = 'wlan0'
IP_ESP = '192.168.4.1'

class Networker:
    def __init__(self, mode, network_ssid, network_password):
        # mode can be either AP or ST (access point or station)
        self.mode = mode
        self.ssid = network_ssid
        self.password = network_password
        self.my_ip = None
        # connect to network
        self.first_exchange()
        # server handler
        self.server = Server('', 6969, SECRET)
        #self.server.receive_data()

    def first_exchange(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = (IP_ESP, 5556) 
                print('connecting to port: ', server_address)
                sock.connect(server_address)
                break
            except:
                print('not connected yet')

        try:
            message = b'Hi, im raspi'
            sock.sendall(message)
            amount_received = 0
            amound_expected = len(message)
            while amount_received < amound_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print('received: ', data)
        finally:
            sock.close()



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
                (data, _) = self.udp_socket.recvfrom(8192)
                msg = self.entschluesseln(data)
                msg = json.loads(msg)
                # print('received: ', msg, 'from :', addr)
                return msg
            except KeyboardInterrupt:
                self.udp_socket.close()
    
    def close_connection(self):
        self.udp_socket.close()

'''
myserver = Server('', 6969, b'BenStinktWieFish')
myserver.receive_data()
'''
'''
# networker aufrufen, der macht dann sein server ding vallah
if __name__ == '__main__':
    networker = Networker('ST', 'RADar', 'BDE4Life!')
'''



# ANLEITUNG:
'''
eine networker instanz erstellen, nach folgendem modell:
--> networker = Networker('ST', 'RADar', 'BDE4Life!')
danach diesen networker nutzen um daten zu kriegen:
--> networker.server.receive_data()
'''