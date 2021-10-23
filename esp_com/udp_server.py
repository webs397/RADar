import socket
import json
from Crypto.Cipher import AES

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

myserver = Server('', 6969, b'BenStinktWieFish')
myserver.receive_data()