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
        self.client_id = self.connect()

    def getP(self):
        pass

    def connect(self):
        try:
            self.client.connect(self.addr)
            type = input("Do you want to create (c) a new game, or to join (j) an existing game: ")
            self.client.sendall(type.encode())
            if type == "c":
                return self.client.recv(100).decode()
            elif type == "j":
                client_id = self.client.recv(100).decode()
                self.client.sendall("games".encode())
                games = int(self.client.recv(100).decode())
                choice = input(f"Please enter your choice in total {games} games: ")
                self.client.sendall(choice.encode())
                return client_id
            # return json.loads(self.client.recv(100))
            # self.client.connect(self.addr)

        except:
            pass

    def send(self, str_data):
        try:
            # data = json.dumps(obj)
            # self.client.send(f"{len(data):<{HEADER_LEN}}".encode())
            # print(str_data.encode())
            self.client.sendall(str_data.encode())
            # recv_len = int(self.client.recv(HEADER_LEN))
            received = self.client.recv(DATA_LEN).decode()
            # print(type(received))
            # print(type(json.loads(received)))
            return json.loads(received)
        except socket.error as e:
            print(e)

