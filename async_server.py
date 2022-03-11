"""
File_id: 07oct2021_async_server
Related file id:  07oct2021_async_client, 07oct2021_menu
This is the alpha server code for the "shooter" game
"""

import asyncio
import json
from zlib import compress, decompress
import pygame
import coloredlogs
import logging
from logging import handlers
from dataclasses import dataclass, asdict
from typing import Any

from inspect import currentframe, getframeinfo

import game_class_s
from platform_shooter_settings import *

FRAME_INFO = getframeinfo(currentframe())

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
    player_joined: bool = False  # True if the chosen game room is received from 2nd player
    game_set: bool = False  # True if player0 finished setting map, match, role
    player_0_name: str = ""  # room name will be f"{player_0_name}'s game"
    player_0_role_id: int = 0
    player_1_name: str = ""
    player_1_role_id: int = 0
    player_0_reader: Any = None
    player_0_writer: Any = None
    player_0_task_name: str = ""
    player_1_reader: Any = None
    player_1_writer: Any = None
    player_1_task_name: str = ""
    map_id: int = 0
    match_id: int = 0
    running = False
    winner = None  # the winner name of the round

    def check_ready(self):
        return self.player_joined and self.game_set


class Server:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.HIDDEN)
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
        self.timer = 0

    async def check_read(self, player_name, reader, length, writer):
        # used for read() before the connected player is in a game room
        string = None
        connected = CONNECTED
        try:
            # received = await reader.read(length)
            received = await reader.readuntil(separator=b";")
            string = received.decode().split(";")[0]
        except ConnectionError:
            self.cnt -= 1
            self.my_logger.warning(
                f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
            connected = not CONNECTED
        else:  # if the connection is properly connected, there will be no ConnectionError exception raised
            if not received:
                self.cnt -= 1
                self.my_logger.warning(
                    f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                if not writer.is_closing():
                    writer.close()
                    await writer.wait_closed()
                connected = not CONNECTED
        return connected, string

    async def check_read_room(self, room: RoomState, player0: bool, player1: bool, length: int):
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
            # received = await reader.read(length)
            received = await reader.readuntil(separator=b";")
            string = received.decode().split(";")[0]
        except ConnectionError:
            self.cnt -= 1
            self.my_logger.warning(
                f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
            # writer.close() is not needed because the writer is already closed
            # await writer.wait_closed(): this line could never be returned when the writer is already closed
            if room.room_id in self.game_dict:
                self.game_dict.pop(room.room_id)
            connected = not CONNECTED
        else:  # if the connection is properly connected, there will be no ConnectionError exception raised
            if not received:
                self.cnt -= 1
                self.my_logger.warning(
                    f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                if not writer.is_closing():
                    writer.close()
                    await writer.wait_closed()
                if room.room_id in self.game_dict:
                    self.game_dict.pop(room.room_id)
                connected = not CONNECTED
        return connected, string

    async def disconnect_2nd_player(self, room, player_bool):  # player_bool: 0 - player0, 1-player1
        writer = None
        player_name = ""
        if player_bool:  # if player1 to be disconnected
            writer = room.player_1_writer
            player_name = room.player_1_name
        else:
            writer = room.player_0_writer
            player_name = room.player_0_name
        writer.write("Disconnected;".encode())
        writer.close()
        await writer.wait_closed()
        self.my_logger.warning(f"Game room [{room.room_id}]: {player_name} is disconnected")
        self.cnt -= 1
        print(f"total connection: {self.cnt}")

    def create_room(self, player_name, reader, writer):
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
            rooms_lst = [[self.game_dict[room_id].player_0_name, self.game_dict[room_id].check_ready(), room_id]
                         for room_id in [*self.game_dict]]
            if not rooms_lst:
                rooms_lst = [["no game", False, 0]]
            rooms_lst_enc = (json.dumps(rooms_lst)+";").encode()
            length = len(rooms_lst_enc)
            writer.write((str(length)+";").encode())  # send the receiving length first
            # this will be "ok" returned from client, just to complete a r/w cycle
            r = await self.check_read(player_name, reader, READ_LEN, writer)  # return connected, string
            if not r[0]:
                return not CONNECTED, chosen_room_id
            writer.write(rooms_lst_enc)
            r = await self.check_read(player_name, reader, READ_LEN, writer)  # return connected, string
            if not r[0]:
                return not CONNECTED, chosen_room_id
            elif int(r[1]) in [*self.game_dict]:
                chosen_room_id = int(r[1])
                """
                # self.game_dict[chosen_room_id].player_joined = True
                player_joined can't be set true here, otherwise player0 will start to write to player1's writer too
                soon to cause the "mark 1" read() below read more bytes in the buffer from player1' reader because the
                player1 client writes the "events" info. Best way could be using reader.readuntil() with a seperator
                letter (e.g. ";"), tested working without turn on/off confirmation.
                """
                self.game_dict[chosen_room_id].player_1_name = player_name
                self.game_dict[chosen_room_id].player_1_reader = reader
                self.game_dict[chosen_room_id].player_1_writer = writer
                chosen_room = self.game_dict[chosen_room_id]
                while not chosen_room.game_set:  # meaning player0 has not finished setting game yet
                    writer.write(f"{self.game_dict[chosen_room_id].player_0_name} is not ready yet, please wait...;".encode())
                    r = await self.check_read(player_name, reader, READ_LEN, writer)  # return connected, string
                    if not r[0]:
                        return not CONNECTED, chosen_room_id
                writer.write("Game is ready to play;".encode())
                r = await self.check_read(player_name, reader, READ_LEN, writer)  # (mark 1) return connected, string
                if not r[0]:
                    return not CONNECTED, chosen_room_id
                return CONNECTED, chosen_room

    def new_connection(self, player_name):
        self.cnt += 1
        self.client_id += 1
        self.my_logger.info(f"New connection to player '{player_name}', client id = {self.client_id}, "
                            f"total connections: {self.cnt}")

    async def new_client(self, reader, writer):
        # any new client connection goes here first
        client_task = asyncio.current_task()
        client_name = ""
        player_id = 0  # player_id will be assigned according to conn_type: create - 0, join - 1
        player_info = None
        room = None
        player_name = None

        try:  # initial read() needs different handling than self.check_read
            # received = await reader.read(READ_LEN)
            received = await reader.readuntil(separator=b";")
            temp = received.decode().split(";")[0]
            player_info = temp.split(",")  # "{conn_type},{self.player_name}"
        except ConnectionError:
            self.my_logger.warning(
                f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
        # if the connection is properly closed, there will be no ConnectionError exception raised
        # but empty byte will be received
        else:
            if not received:
                self.my_logger.warning(f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                if not writer.is_closing():
                    writer.close()
                    await writer.wait_closed()

        if player_info[0] != "handshake":  # if not "handshake", it's an invalid connection request
            if not writer.is_closing():
                writer.close()
                await writer.wait_closed()
            return
        elif player_info[0] == "handshake":  # handshake connection, waiting for conn_type
            player_name = player_info[1]
            writer.write("ok;".encode())  # for client to confirm successful handshake

            try:  # initial read() needs different handling than self.check_read, this is just for r/w cycle
                # received = await reader.read(READ_LEN)
                received = await reader.readuntil(separator=b";")
            except ConnectionError:
                self.my_logger.warning(
                    f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
            else:  # if the connection is properly closed, there will be no ConnectionError exception raised
                if not received:
                    self.my_logger.warning(
                        f"Connection to player {player_name} is lost [{getframeinfo(currentframe()).lineno}]")
                    if not writer.is_closing():
                        writer.close()
                        await writer.wait_closed()

            self.new_connection(player_name)
            client_name = f"{player_name}-{self.client_id}"
            client_task.set_name(client_name)
            writer.write((str(self.client_id)+";").encode())

            r = await self.check_read(player_name, reader, READ_LEN, writer)  # waiting for "create" or "join"
            if not r[0]:  # return connected, string
                return
            else:
                player_info = r[1].split(",")

            conn_type = player_info[0]  # client reply: f"{conn_type},{player_name}"
            if conn_type == "create":
                player_id = 0
                room = self.create_room(player_name, reader, writer)
                room.player_0_task_name = client_name
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
                    room.player_1_task_name = client_name
                    room.player_joined = True
                    """
                    player_joined can't be set to True in self.join(), otherwise player0 will enter the 
                    routine game loop too soon, refer to comments in self.join() for details
                    """

        while True:  # wait for the 2nd player to join the room and the 1st player to set the game mode
            self.clock.tick(FPS)
            """
            once there are two players in one game room, game_ready for that room is set to 
            True, then the task for player_1 who joins the room after player_0 created the room
            will be returned so that the server game tick info to both player_0 and player_1 
            can be handled by the task created for player_0 
            """
            if room.check_ready():
                if player_id == 1:  # player_id = 1 means this is the task for player_1
                    self.my_logger.warning(f"Player '{room.player_1_name}' joined player '{room.player_0_name}''s game")
                    return  # the task (for player_1) is returned (completed) once player_1 is in the room
                # data = "Game Ready".encode()
                room.running = True
                room.player_0_writer.write(
                    f"Game Ready,{room.player_1_name},{room.map_id},{room.match_id},{room.player_0_role_id};".encode())
                room.player_1_writer.write(
                    f"Game Ready,{room.player_0_name},{room.map_id},{room.match_id},{room.player_1_role_id};".encode())
                break  # break current while loop to start the routine game tick
            else:  # if game_ready is False, it means there is only player_0 in the game room
                data = f"New game is created, waiting for the second player to join...;".encode()
                room.player_0_writer.write(data)
                r = await self.check_read_room(room, True, False, READ_LEN)  # r/w cycle and check the connection
                if not r[0]:  # return connected, string
                    return
                else:
                    info = r[1].split(",")
                    if info[0] == "1":  # ready, map_id, match_id, role_id
                        room.map_id = info[1]
                        room.match_id = info[2]
                        room.player_0_role_id = info[3]
                        room.game_set = True

        if room.running:
            await self.game(room)  # this is the routine game tick
            print(f"{room.winner} wins!")

    async def game(self, room):
        g = game_class_s.Game(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        g.new()
        g.map_id = int(room.map_id)
        g.match_id = int(room.match_id)
        gs = GameState()
        self.my_logger.warning(f"{room.player_0_name} is gaming with {room.player_1_name}!")
        while g.playing:  # This is the routine game tick
            self.clock.tick(FPS)
            actual_fps = int(self.clock.get_fps())
            actual_tick = int(pygame.time.get_ticks())
            if actual_fps <= 40 and (actual_tick-self.timer) > 5000:
                self.timer = actual_tick
                self.my_logger.warning(f"Low fps: {actual_fps}")

            r = await self.check_read_room(room, True, False, READ_LEN)
            if not r[0]:
                r = await self.check_read_room(room, False, True, READ_LEN)
                if not r[0]:
                    return
                else:
                    room.player_1_writer.write("Disconnected;".encode())
                    room.player_1_writer.close()
                    await room.player_1_writer.wait_closed()
                    self.my_logger.warning(f"Game room <{room.room_id}>: {room.player_1_name} is disconnected")
                    self.cnt -= 1
                    # await self.disconnect_2nd_player(room, 1)
                    return
            else:
                g.events_str_shooter = r[1]

            r = await self.check_read_room(room, False, True, READ_LEN)
            if not r[0]:
                r = await self.check_read_room(room, True, False, READ_LEN)
                if not r[0]:
                    return
                else:
                    room.player_0_writer.write("Disconnected;".encode())
                    room.player_0_writer.close()
                    await room.player_0_writer.wait_closed()
                    self.my_logger.warning(f"Game room [{room.room_id}]: {room.player_0_name} is disconnected")
                    self.cnt -= 1
                    print(f"total connection: {self.cnt}")
                    # await self.disconnect_2nd_player(room, 0)
                    return
            else:
                # print(f"player1 event: {r[1]}")
                g.events_str_chopper = r[1]

            g.events()
            g.update()

            gs.shooter_img_dict_key = g.player_shooter.img_dict_key
            gs.shooter_img_idx = g.player_shooter.image_idx
            gs.shooter_pos = (g.player_shooter.rect.x, g.player_shooter.rect.y)
            gs.chopper_img_dict_key = g.player_chopper.img_dict_key
            gs.chopper_img_idx = g.player_chopper.image_idx
            gs.chopper_pos = (g.player_chopper.rect.x, g.player_chopper.rect.y)
            gs.bullet_l0_pos = (g.bullets_l[0].rect.x, g.bullets_l[0].rect.y)
            gs.bullet_l1_pos = (g.bullets_l[1].rect.x, g.bullets_l[1].rect.y)
            gs.bullet_l2_pos = (g.bullets_l[2].rect.x, g.bullets_l[2].rect.y)
            gs.bullet_l3_pos = (g.bullets_l[3].rect.x, g.bullets_l[3].rect.y)
            gs.bullet_l4_pos = (g.bullets_l[4].rect.x, g.bullets_l[4].rect.y)
            gs.bullet_r0_pos = (g.bullets_r[0].rect.x, g.bullets_r[0].rect.y)
            gs.bullet_r1_pos = (g.bullets_r[1].rect.x, g.bullets_r[1].rect.y)
            gs.bullet_r2_pos = (g.bullets_r[2].rect.x, g.bullets_r[2].rect.y)
            gs.bullet_r3_pos = (g.bullets_r[3].rect.x, g.bullets_r[3].rect.y)
            gs.bullet_r4_pos = (g.bullets_r[4].rect.x, g.bullets_r[4].rect.y)
            if g.current_level_no == 0:
                gs.moving_block_pos = DEAD_CRATER_POS
            else:
                gs.moving_block_pos = (g.level02.moving_block.rect.x, g.level02.moving_block.rect.y)
            gs.r_sign_flg = g.r_sign_flg
            gs.map_id = g.map_id
            gs.match_id = g.match_id
            gs.level_id = g.current_level_no
            gs.round = g.match_score["round"]
            gs.shooter_score = g.match_score["shooter"]
            gs.chopper_score = g.match_score["chopper"]

            send_byte = (json.dumps([*asdict(gs).values()])+";").encode()
            # compressed_send_byte = compress(send_byte)
            # TODO: it seems zlib compressed data can't be directly sent over a StreamsWriter
            room.player_0_writer.write(send_byte)
            # room.player_0_writer.write(compressed_send_byte)
            room.player_1_writer.write(send_byte)
            # room.player_1_writer.write(compressed_send_byte)

        room.winner = g.winner

    def handle_exception(self, loop, context):
        # context["message"] will always be there; but context["exception"] may not
        # msg = context.get("exception", context["message"])
        self.my_logger.error(f"Caught exception: {context}")

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
