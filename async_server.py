"""
File_id: 07oct2021_async_server
Related file id:  07oct2021_async_client, 07oct2021_menu
This is the alpha server code for the "shooter" game
"""

import asyncio
import json

import pygame
import coloredlogs
import datetime
import logging
from logging import handlers
from dataclasses import dataclass
from typing import Any

FPS = 100
LEN = 15

FIELD_STYLES = {'asctime': {'color': 'green'},
                'levelname': {'bold': False, 'color': (200, 200, 200)},
                'filename': {'color': 'cyan'},
                'funcName': {'color': 'blue'}}

LEVEL_STYLES = {'critical': {'bold': True, 'color': 'red'},
                'debug': {'color': 'magenta'},
                'error': {'color': 'red'},
                'exception': {'color': 'red'},
                'info': {'color': 'green'},
                'warning': {'color': 'yellow'}}


@dataclass
class RoomState:
    room_id: int = 0
    game_ready: bool = False  # True if second player joins
    player_0_name: str = ""  # room name will be f"{player_0_name}'s game"
    player_1_name: str = ""
    player_0_reader: Any = None
    player_0_writer: Any = None
    player_1_reader: Any = None
    player_1_writer: Any = None


class Server:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.cnt = 0  # total number of connections to the server
        self.client_id = 0
        self.game_dict = {}  # used to store game room information
        self.room_cnt = 0  # total number of game rooms
        self.room_id = 0
        self.player_info = []  # f"{conn_type},{player_name}"
        self.writer: [asyncio.streams.StreamWriter] = None
        self.reader: [asyncio.streams.StreamReader] = None
        self.loop = None  # asyncio loop
        self.my_logger = logging.getLogger()
        fmt = "%(asctime)s [%(levelname)s]: %(message)s"
        coloredlogs.install(level=logging.INFO,
                            logger=self.my_logger,
                            fmt=fmt,
                            field_styles=FIELD_STYLES,
                            level_styles=LEVEL_STYLES)
        format_str = logging.Formatter(fmt)
        fh = handlers.RotatingFileHandler("server_log.txt", "a", 100000, 3)
        fh.setFormatter(format_str)
        self.my_logger.addHandler(fh)

    def create(self):
        self.room_cnt += 1
        self.room_id += 1
        room = RoomState()
        room.room_id = self.room_id
        room.player_0_name = self.player_info[1]
        room.player_0_reader = self.reader
        room.player_0_writer = self.writer
        self.game_dict[room.room_id] = room
        return room

    async def join(self, reader, writer):
        # if the client request to join an existing game, a new coroutine will be created with this function
        while True:
            self.clock.tick(FPS)
            # sending room list to the client, no matter full or not [[player0_name, game_ready, room_id],]
            rooms_lst = [[self.game_dict[room_id].player_0_name, self.game_dict[room_id].game_ready, room_id]
                         for room_id in [*self.game_dict]]
            rooms_lst_enc = json.dumps(rooms_lst).encode()

            length = len(rooms_lst_enc)
            writer.write(str(length).encode())  # send the receiving length first
            # this will be the "length" returned from client, just to complete a write/read cycle
            await reader.read(length)

            writer.write(rooms_lst_enc)
            print(f"server sent: {rooms_lst}")
            recv_data = await reader.read(100)
            choice = recv_data.decode()
            if choice in rooms_lst:
                print("Room choice = ", choice)
                return

            if choice != "j":  # use a number to simulate the game room selection
                return choice

    async def new_client(self, reader, writer):
        # any new client connection goes here first
        player_id = 0  # player_id will be assigned according to conn_type: create - 0, join - 1
        self.cnt += 1
        self.client_id += 1
        self.reader = reader
        self.writer = writer
        loop = asyncio.get_running_loop()
        room = None
        self.writer.write(str(self.client_id).encode())  # send client_id
        recv_data = await self.reader.read(200)  # client reply: f"{conn_type},{player_name}"
        self.player_info = recv_data.decode().split(",")
        self.my_logger.info(f"Total connections: {self.cnt}, new connection to: {self.player_info[1]}")
        if self.player_info[0] == "handshake":  # handshake connection, waiting for other conn_type
            self.writer.write("Waiting".encode())
            recv_data = await self.reader.read(200)  # waiting for "create" or "join"
            self.player_info = recv_data.decode().split(",")
            conn_type = self.player_info[0]  # # client reply: f"{conn_type},{player_name}"
            if conn_type == "create":
                player_id = 0
                room = self.create()
            elif conn_type == "join":
                player_id = 1
                room = self.join()

        if player_info[0] == "create":  # first msg received from client will be "c"+player's name to create a new game
            room = RoomState()
            room.room_id = self.room_cnt
            room.player_0_name = player_info[1]
            room.player_0_reader = reader
            room.player_0_writer = writer
            self.game_dict[room.room_id] = room
            self.room_cnt += 1
        elif player_info[0] == "join":
            choice = await self.join(reader, writer)
            # once a number is provided by the client, it's used as a room number
            # that this client wants to join and join() is returned back here
            choice = int(choice)
            player_id = 1
            self.game_dict[choice].player_1_reader = reader
            self.game_dict[choice].player_1_writer = writer
            self.game_dict[choice].game_ready = True
            room = self.game_dict[choice]

        while True:  # wait for the 2nd player to join the room
            self.clock.tick(FPS)
            """
            once there are two players in one game room, game_ready for that room is set to 
            True, then the task for player_1 who joins the room after player_0 created the room
            will be returned so that the server game tick info to both player_0 and player_1 
            can be handled by the task created for player_0 
            """
            if room.game_ready:
                if player_id == 1:  # player_id = 1 means this is the task for player_1
                    # logging.warning(f"Task for connection {cnt} in game_id {room.room_id} is being returned")
                    return  # the task (for player_1) is returned once player_1 is in the room
                # the following block is the routine communication between the server and
                # both players in the same game room
                data = "Game Ready".encode()
                room.player_0_writer.write(data)
                # await game_dict[game_id][2].drain()
                room.player_1_writer.write(data)
                # await game_dict[game_id][4].drain()
                break  # break current while loop to start the game playing data exchange loop

            else:  # if game_ready is False, it means there is only player_0 in the game room
                data = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]server msg: tasks - {len(asyncio.all_tasks())}".encode()
                room.player_0_writer.write(data)
                # await game_dict[game_id][2].drain()
                try:
                    msg0 = await room.player_0_reader.read(100)
                    # logging.info(f"Received: '{msg0.decode()}'")
                except Exception as e:
                    logging.warning(f"Something's wrong with room {room.room_id} - player0: {e}")
                    room.player_0_writer.close()
                    self.cnt -= 1
                    # print the information if the key to pop up doesn't exist in the following line
                    # logging.warning(game_dict.pop(room.room_id, f"room '{room.room_id}' is not running"))
                    break

        while True:  # this is the routine game tick
            self.clock.tick(FPS)
            try:
                msg0 = await loop.create_task(room.player_0_reader.read(LEN))
                # logging.info(f"Received: '{msg0.decode()}'")
            except ConnectionError:
                room.player_0_writer.close()
                self.my_logger.warning(f"Connection to room {room.room_id}: player 0 is lost")
                self.cnt -= 1
                break

            try:
                msg1 = await loop.create_task(room.player_1_reader.read(LEN))
                # logging.info(f"Received: '{msg1.decode()}'")
            except ConnectionError:
                room.player_1_writer.close()
                self.my_logger.warning(f"Connection to room {room.room_id}: player 1 is lost")
                self.cnt -= 1
                break

            room.player_0_writer.write(msg1)
            room.player_1_writer.write(msg0)

    async def main(self, host, port):
        server = await asyncio.start_server(self.new_client, host, port)
        self.my_logger.info(f"Server started at {host}:{port}")
        await server.serve_forever()


if __name__ == "__main__":
    s = Server()
    s.my_logger.info("----------------------New log started---------------------------------")
    try:
        # No IP address or "0.0.0.0" is provided to allow the server to listen to all connections on the port
        asyncio.run(s.main('0.0.0.0', 8887))
    except KeyboardInterrupt:
        s.my_logger.warning("Server terminated by player.")
