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

READ_LEN = 100
CONNECTED = True


class Network:
    def __init__(self, server_ip='192.168.3.10', server_port="8888"):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_id = 0
        self.server_msg = "Waiting for 2nd player"
        self.player_name = ""
        self.opponent_name = ""
        self.reader = None
        self.writer = None
        self.game_setting = [0, 0, 0]  # [ready, map_id, match_id]
        self.game_rooms = []
        self.chosen_room = "no chosen"
        self.q_game_rooms = Queue()
        self.speed = 2
        self.pos_send = [0, 0]
        self.pos_recv = Queue(maxsize=3)  # (x, Y) coordinates as tuple for each item in the Queue

    async def check_read(self, length):
        string = None
        connected = CONNECTED
        try:
            received = await self.reader.read(length)
            string = received.decode()
        except ConnectionError:
            print(f"Connection to server is lost")
            self.writer.close()
            await self.writer.wait_closed()
            connected = not CONNECTED
        else:  # if the connection is properly connected, there will be no ConnectionError exception raised
            if not received:
                print(f"Connection to server is lost")
                self.writer.close()
                await self.writer.wait_closed()
                connected = not CONNECTED
        return connected, string

    async def conn(self, player_name):
        conn_type = "handshake"
        self.player_name = player_name
        self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
        # id_data = await self.reader.read(100)
        # self.client_id = id_data.decode()
        self.writer.write(f"{conn_type},{self.player_name}".encode())
        r = await self.check_read(READ_LEN)
        if r[0]:  # return connected, string
            if r[1] != "ok":  # if server doesn't send back "ok", there should be some connection issue
                print("Server error")
        self.writer.write(f"{conn_type},{self.player_name}".encode())  # just to complete the r/w cycle
        r = await self.check_read(READ_LEN)
        if r[0]:  # return connected, string
            self.client_id = r[1]

    async def create(self):  # create a new game room
        conn_type = "create"
        self.writer.write(f"{conn_type},{self.player_name}".encode())

    async def join(self):
        conn_type = "join"
        self.writer.write(f"{conn_type},{self.player_name}".encode())
        # await self.client()
        print(f"This is 'join' client# {self.client_id}")
        await self.get_games()

    async def send_room_choice(self, room):  # room = [player0_name, game_ready, room_id]
        self.writer.write(f"{room[2]}".encode())

    async def get_games(self):
        r = await self.check_read(READ_LEN)
        if not r[0]:  # return connected, string
            print("Connection issue to server during get_games")
            return
        else:
            length = r[1]
        self.writer.write("ok".encode())  # just to complete a r/w cycle before receiving the next data
        rooms_data = await self.reader.read(int(length))
        self.game_rooms = list(json.loads(rooms_data.decode()))  # [[player0_name, game_ready, room_id],]

    async def refresh(self):
        self.writer.write("refreshing".encode())
        await self.get_games()

    async def client(self):
        while True:  # this is the loop waiting for the 2nd player to join
            r = await self.check_read(READ_LEN)
            if not r[0]:
                return
            else:
                self.server_msg = tuple(r[1].split(","))  # f"Game Ready,{room.player_0_name}"
            if self.server_msg[0] == "Game Ready":
                self.opponent_name = self.server_msg[1]
                break
            else:
                send_str = f"{self.game_setting[0]},{self.game_setting[1]},{self.game_setting[2]}"
                self.writer.write(send_str.encode())

        while True:  # this is the routine game tick
            reply = self.pos2str(self.pos_send)
            self.writer.write(reply.encode())
            # start = perf_counter()
            # data = await self.reader.read(READ_LEN)
            r = await self.check_read(READ_LEN)
            if not r[0]:  # return connected, string
                print("Connection issue to server during get_games")
                return
            # print(perf_counter() - start)
            else:
                try:
                    self.pos_recv.put_nowait(self.str2pos(r[1]))
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
        local_string = string
        if string == "Disconnected":
            local_string = "-99,-99"  # indicating the server is disconnected from the other player

        return tuple(map(int, local_string.split(',')))


def main(server_ip='127.0.0.1', server_port="8887"):
    new_client = Network(server_ip, server_port)
    asyncio.run(new_client.start("Amy", "create"))


if __name__ == "__main__":
    main()
