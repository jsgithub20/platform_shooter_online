"""
File_id: 14may2020_async_client
Related file id:  14may2020_async_server
This is a test client program to confirm the following functionalities:
1. server-client connection establishment through asyncio streams
2. async task structures to handle new game room creation and existing game room joining
    based on the client request
3. client frame rate control with server tick rate (clock.tick()) over the connection
"""

import asyncio


class Network:
    def __init__(self, server_ip='127.0.0.1'):
        self.server_ip = server_ip
        self.client_id = 0
        self.server_msg = ""

    async def start(self):
        timer = 0  # used to simulate the waiting time for the player to enter room#
        # input "0" to simulate the request to join a room
        choice = input("Input 'c' to create a new game room, or 'j' to join one: ")
        if choice == "c":
            reader, writer = await asyncio.open_connection(self.server_ip, 5000)
            data = await reader.read(100)
            self.client_id = data.decode()
            print(f"This is client# {self.client_id}")
            writer.write("c".encode())
            await self.client(reader, writer, self.client_id)
        else:
            reader, writer = await asyncio.open_connection(self.server_ip, 5000)
            data = await reader.read(100)
            self.client_id = data.decode()
            print(f"This is client# {self.client_id}")
            writer.write("j".encode())  # input "0" to simulate the request to join a room
            while True:
                data = await reader.read(100)
                rooms = data.decode()
                print(f"Rooms available to join: {rooms}")
                timer += 1
                if timer < 5:  # used to simulate the waiting time for the player to input a room#
                    reply = "j"
                    writer.write(reply.encode())
                else:
                    reply = rooms[-1]  # simulate the room selected by the player
                    writer.write(reply.encode())
                    await self.client(reader, writer, self.client_id)

    async def client(self, reader, writer, client_id):
        while True:
            data = await reader.read(100)
            self.server_msg = data.decode()
            if self.server_msg != "quit":
                print(f'Received: {self.server_msg!r}')
                reply = f"{int(client_id)}: msg received is {self.server_msg!r}"
                writer.write(reply.encode())
                await writer.drain()
            else:
                writer.close()
                print('Closing the connection')
                break


if __name__ == "__main__":
    new_client = Network()
    asyncio.run(new_client.start())
