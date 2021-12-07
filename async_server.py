"""
File_id: 07oct2021_async_server
Related file id:  07oct2021_async_client, 07oct2021_menu
This is the alpha server code for the "shooter" game
"""

import asyncio
import json

import pygame
import coloredlogs
import logging
from logging import handlers
from dataclasses import dataclass
from typing import Any

from inspect import currentframe, getframeinfo

FRAME_INFO = getframeinfo(currentframe())

FPS = 60
READ_LEN = 20
CONNECTED = True

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

    async def check_read(self, player_name, reader, length, writer):
        # used for read() before the connected player is in a game room
        string = None
        connected = CONNECTED
        try:
            received = await reader.read(length)
            string = received.decode()
        except ConnectionError:
            self.cnt -= 1
            self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
            writer.close()
            await writer.wait_closed()
            connected = not CONNECTED
        else:  # if the connection is properly connected, there will be no ConnectionError exception raised
            if not received:
                self.cnt -= 1
                self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                writer.close()
                await writer.wait_closed()
                connected = not CONNECTED
        return connected, string

    async def check_read_room(self, room: RoomState, player0: bool, player1: bool, length):
        # used for read() after the connected player is in a game room
        string = None
        reader = None
        writer = None
        player_name = ""
        connected = CONNECTED
        if player0:
            player_name = room.player_0_name
            reader = room.player_0_reader
            writer = room.player_0_writer
        elif player1:
            player_name = room.player_1_name
            reader = room.player_1_reader
            writer = room.player_1_writer
        try:
            received = await reader.read(length)
            string = received.decode()
        except ConnectionError:
            self.cnt -= 1
            self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
            writer.close()
            await writer.wait_closed()
            self.game_dict.pop(room.room_id)
            connected = not CONNECTED
        else:  # if the connection is properly connected, there will be no ConnectionError exception raised
            if not received:
                self.cnt -= 1
                self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                writer.close()
                await writer.wait_closed()
                self.game_dict.pop(room.room_id)
                connected = not CONNECTED
        return connected, string

    def create(self, player_name, reader, writer):
        self.room_cnt += 1
        self.room_id += 1
        room = RoomState()
        room.room_id = self.room_id
        room.player_0_name = player_name
        room.player_0_reader = reader
        room.player_0_writer = writer
        self.game_dict[self.room_id] = room
        return room

    async def join(self, player_name, reader, writer):
        # if the client request to join an existing game, a new coroutine will be created with this function
        chosen_room_id = None
        while True:
            self.clock.tick(FPS)
            # sending room list to the client, no matter full or not [[player0_name, game_ready, room_id],]
            # if game_dict is empty, an empty list will be assigned to "rooms_lst" and no exception will be raised
            rooms_lst = [[self.game_dict[room_id].player_0_name, self.game_dict[room_id].game_ready, room_id]
                         for room_id in [*self.game_dict]]
            if not rooms_lst:
                rooms_lst = [["no game", False, 0]]
            rooms_lst_enc = json.dumps(rooms_lst).encode()
            length = len(rooms_lst_enc)
            writer.write(str(length).encode())  # send the receiving length first
            # this will be "ok" returned from client, just to complete a write/read cycle
            r = await self.check_read(player_name, reader, READ_LEN, writer)  # return connected, string
            if not r[0]:
                return not CONNECTED, chosen_room_id
            writer.write(rooms_lst_enc)
            r = await self.check_read(player_name, reader, READ_LEN, writer)  # return connected, string
            if not r[0]:
                return not CONNECTED, chosen_room_id
            elif int(r[1]) in [*self.game_dict]:
                chosen_room_id = int(r[1])
                self.game_dict[chosen_room_id].game_ready = True
                self.game_dict[chosen_room_id].player_1_name = player_name
                self.game_dict[chosen_room_id].player_1_reader = reader
                self.game_dict[chosen_room_id].player_1_writer = writer
                chosen_room = self.game_dict[chosen_room_id]
                return CONNECTED, chosen_room

    def new_connection(self, player_name):
        self.cnt += 1
        self.client_id += 1
        self.my_logger.info(f"New connection to player '{player_name}', client id = {self.client_id}, "
                            f"total connections: {self.cnt}")

    async def new_client(self, reader, writer):
        # any new client connection goes here first
        player_id = 0  # player_id will be assigned according to conn_type: create - 0, join - 1
        player_info = None
        room = None
        player_name = None

        try:  # initial read() needs different handling than self.check_read
            received = await reader.read(READ_LEN)
            player_info = received.decode().split(",")  # "{conn_type},{self.player_name}"
        except ConnectionError:
            self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
            writer.close()
            await writer.wait_closed()
        # if the connection is properly closed, there will be no ConnectionError exception raised
        # but empty byte will be received
        else:
            if not received:
                self.my_logger.warning(f"Connection to player {player_name} is lost [196]")
                writer.close()
                await writer.wait_closed()

        if player_info[0] != "handshake":  # if not "handshake", it's an invalid connection request
            writer.close()
            await writer.wait_closed()
            return
        elif player_info[0] == "handshake":  # handshake connection, waiting for conn_type
            player_name = player_info[1]
            writer.write("ok".encode())  # for client to confirm successful handshake

            try:  # initial read() needs different handling than self.check_read, this is just for r/w cycle
                received = await reader.read(READ_LEN)
            except ConnectionError:
                self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                writer.close()
                await writer.wait_closed()
            else:  # if the connection is properly closed, there will be no ConnectionError exception raised
                if not received:
                    self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                    writer.close()
                    await writer.wait_closed()

            self.new_connection(player_name)
            writer.write(str(self.client_id).encode())

            r = await self.check_read(player_name, reader, READ_LEN, writer)  # waiting for "create" or "join"
            if not r[0]:  # return connected, string
                return
            else:
                player_info = r[1].split(",")

            conn_type = player_info[0]  # client reply: f"{conn_type},{player_name}"
            if conn_type == "create":
                player_id = 0
                room = self.create(player_name, reader, writer)
            elif conn_type == "join":
                player_id = 1
                try:
                    join_room = await self.join(player_info[1], reader, writer)  # return CONNECTED, choice
                except ConnectionError:
                    # self.my_logger.warning(f"Connection to player {player_name} is lost")
                    return

                if not join_room[0]:
                    return
                else:
                    room = join_room[1]

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
                    self.my_logger.warning(f"Player '{room.player_1_name}' joined player '{room.player_0_name}''s game")
                    # logging.warning(f"Task for connection {cnt} in game_id {room.room_id} is being returned")
                    return  # the task (for player_1) is returned (completed) once player_1 is in the room
                # data = "Game Ready".encode()
                room.player_0_writer.write(f"Game Ready,{room.player_1_name}".encode())
                room.player_1_writer.write(f"Game Ready,{room.player_0_name}".encode())
                break  # break current while loop to start the routine game tick
            else:  # if game_ready is False, it means there is only player_0 in the game room
                data = f"New game is created, waiting for the second player to join...".encode()
                room.player_0_writer.write(data)
                # print("writing to player_0 completed")
                r = await self.check_read_room(room, True, False, READ_LEN)  # r/w cycle and check the connection
                if not r[0]:  # return connected, string
                    return

        while True:  # this is the routine game tick
            self.clock.tick(FPS)
            r = await self.check_read_room(room, True, False, READ_LEN)
            if not r[0]:
                room.player_1_writer.write("Disconnected".encode())
                self.my_logger.warning(f"Connection to player {room.player_1_name} is disconnected")
                break
            else:
                msg0 = r[1]

            r = await self.check_read_room(room, False, True, READ_LEN)
            if not r[0]:
                room.player_0_writer.write("Disconnected".encode())
                self.my_logger.warning(f"Connection to player {room.player_0_name} is disconnected")
                break
            else:
                msg1 = r[1]

            room.player_0_writer.write(msg1.encode())
            room.player_1_writer.write(msg0.encode())

    def handle_exception(self, loop, context):
        # context["message"] will always be there; but context["exception"] may not
        msg = context.get("exception", context["message"])
        self.my_logger.error(f"Caught exception: {msg}")
        print(context)

    async def main(self, host, port):
        server = await asyncio.start_server(self.new_client, host, port, )
        self.loop = server.get_loop()
        self.loop.set_exception_handler(self.handle_exception)
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
