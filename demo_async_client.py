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
import logging


class Network:
    def __init__(self, server_ip='127.0.0.1', server_port="8888"):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_id = 0
        self.server_msg = ""
        self.reader = None
        self.writer = None
        self.pos = (0, 0)
        self.speed = 2

    async def start(self):
        timer = 0  # used to simulate the waiting time for the player to enter room#
        # input "0" to simulate the request to join a room
        choice = input("Input 'c' to create a new game room, or 'j' to join one: ")
        if choice == "c":
            self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
            data = await self.reader.read(100)
            self.client_id = data.decode()
            print(f"This is client# {self.client_id}")
            self.writer.write("c".encode())
            await self.client()
        else:
            self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
            data = await self.reader.read(100)
            self.client_id = data.decode()
            print(f"This is client# {self.client_id}")
            self.writer.write("j".encode())  # input "0" to simulate the request to join a room
            while True:
                data = await self.reader.read(100)
                rooms = data.decode()
                print(f"Rooms available to join: {rooms}")
                timer += 1
                if timer < 5:  # used to simulate the waiting time for the player to input a room#
                    reply = "j"
                    self.writer.write(reply.encode())
                else:
                    reply = rooms[-1]  # simulate the room selected by the player
                    self.writer.write(reply.encode())
                    await self.client()

    async def client(self):
        print("Joining game")
        while True:
            data = await self.reader.read(100)
            self.server_msg = data.decode()
            if self.server_msg == "Game Ready":
                logging.info("Game Ready")
                break
            elif self.server_msg != "quit":
                print(f'Received: {self.server_msg!r}')
                reply = f"{int(self.client_id)}: msg received is {self.server_msg!r}"
                self.writer.write(reply.encode())
                await self.writer.drain()
            else:
                await self.stop()
                break

        while True:
            reply = f"{self.pos}"
            self.writer.write(reply.encode())
            data = await self.reader.read(100)
            msg = data.decode()
            print(f"message from server: {msg}")

    async def stop(self):
        self.writer.close()
        await self.writer.wait_closed()
        print('Closing the connection')

    def pos2str(self, pos: tuple):
        # the returned string is like "100,100" from tuple (100, 100)
        return ','.join(map(str, pos))

    def str2pos(self, string: str):
        # string must be "100,100" or "100, 100" which will be converted to (100, 100)
        return tuple(map(int, string.split(',')))


def main(server_ip='127.0.0.1', server_port="8888"):
    new_client = Network(server_ip, server_port)
    asyncio.run(new_client.start())


async def some_func(number):
    await asyncio.sleep(number)
    return number


if __name__ == "__main__":
    main()
