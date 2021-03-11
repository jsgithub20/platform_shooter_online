import socket
import json
import pickle
from platform_shooter_settings import *


class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = int(port)
        self.addr = (self.server, self.port)
        self.game_state = self.connect()

    def getP(self):
        pass

    def connect(self):
        try:
            self.client.connect(self.addr)
            # return json.loads(self.client.recv(100))
            # self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, str_data):
        try:
            # data = json.dumps(obj)
            # self.client.send(f"{len(data):<{HEADER_LEN}}".encode())
            self.client.sendall(str_data.encode())
            # recv_len = int(self.client.recv(HEADER_LEN))
            return self.client.recv(100).decode()
        except socket.error as e:
            print(e)

