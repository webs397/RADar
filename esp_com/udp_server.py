import socket
import json

class Server:
    def __init__(self, client_ip_address, port):
        self.address = (client_ip_address,port)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(self.address)
        self.udp_socket.bind(self.address)

    def receive_data(self):
        print('waiting for messages ...')
        while True:
            try:
                (data, addr) = self.udp_socket.recvfrom()
                data = json.loads(data)
                print('received: ', data, 'from :', addr)
            except KeyboardInterrupt:
                self.udp_socket.close()
    
    def close_connection(self):
        self.udp_socket.close()

myserver = Server('192.168.0.69', 6969)
myserver.receive_data()