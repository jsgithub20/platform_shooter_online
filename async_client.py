"""
File_id: 07oct2021_async_client
Related file id:  07oct2021_async_server, 07oct2021_menu
This is the alpha client code for the "shooter" game
"""

import asyncio
import json
import logging
import queue
from queue import Queue
from time import perf_counter


LEN = 15


class Network:
    def __init__(self, server_ip='192.168.3.10', server_port="8888"):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_id = 0
        self.server_msg = "Initial msg"
        self.player_name = ""
        self.reader = None
        self.writer = None
        self.game_rooms = []
        self.chosen_room = "no chosen"
        self.q_game_rooms = Queue()
        self.speed = 2
        self.pos_send = [0, 0]
        self.pos_recv = Queue(maxsize=3)  # (x, Y) coordinates as tuple for each item in the Queue

    async def start(self, player_name, start_type):
        self.player_name = player_name
        if start_type == "create":
            self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
            data = await self.reader.read(100)
            self.client_id = data.decode()
            print(f"This is 'create' client# {self.client_id}")
            self.writer.write(f"{start_type},{player_name}".encode())
            await self.client()
        elif start_type == "join":
            self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
            data = await self.reader.read(100)
            self.client_id = data.decode()
            print(f"This is 'join' client# {self.client_id}")
            self.writer.write(f"{start_type},{player_name}".encode())
            while True:  # the loop to receive new room list from server
                len_data = await self.reader.read(100)
                self.writer.write(len_data)
                rooms_data = await self.reader.read(int(len_data.decode()))
                self.game_rooms = list(json.loads(rooms_data.decode()))
                print(f"received by client: {self.game_rooms}")
                try:
                    self.q_game_rooms.put_nowait(self.game_rooms)
                    print(f"put in q: {self.q_game_rooms.qsize()}")
                except queue.Full:
                    pass  # TODO: code to handle the exception
                self.writer.write(self.chosen_room.encode())

    async def client(self):
        while True:  # this is the loop waiting for the 2nd player to join
            data = await self.reader.read(100)
            self.server_msg = data.decode()
            if self.server_msg == "Game Ready":
                # logging.info("Game Ready")
                break
            elif self.server_msg != "quit":
                # print(f'Received: {self.server_msg!r}')
                reply = f"{int(self.client_id)}: msg received is {self.server_msg!r}"
                self.writer.write(reply.encode())
                await self.writer.drain()
            else:
                await self.stop()
                break

        while True:  # this is the routine game tick
            reply = self.pos2str(self.pos_send)
            self.writer.write(reply.encode())
            # start = perf_counter()
            data = await self.reader.read(LEN)
            # print(perf_counter() - start)
            try:
                self.pos_recv.put_nowait(self.str2pos(data.decode()))
            except queue.Full:
                pass  # TODO: code to handle the exception

    async def stop(self):
        self.writer.close()
        await self.writer.wait_closed()
        print('Closing the connection')

    def pos2str(self, pos: list):
        # the returned string is like "100,100" from tuple (100, 100)
        return ','.join(map(str, pos))

    def str2pos(self, string: str):
        # string must be "100,100" or "100, 100" which will be converted to (100, 100)
        return tuple(map(int, string.split(',')))


def main(server_ip='127.0.0.1', server_port="8887"):
    new_client = Network(server_ip, server_port)
    asyncio.run(new_client.start("Amy", "create"))


if __name__ == "__main__":
    main()
