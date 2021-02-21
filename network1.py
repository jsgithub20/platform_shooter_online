import socket
import pickle


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
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, obj):
        try:
            self.client.send(pickle.dumps(obj))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

