from temp_t_network import Network
import time


network = Network("10.139.192.69", "5050")
client_id = network.client_id
print(f"This is client: {client_id}")

while True:
    msg = network.client.recv(100).decode()
    reply = f"{time.strftime('%H:%M:%S')} - client {client_id} received from server: '{msg}'"
    print(reply)
    network.client.sendall(reply.encode())
