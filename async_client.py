"""
File_id: 07oct2021_async_client
Related file id:  07oct2021_async_server, 07oct2021_menu
This is the alpha client code for the "shooter" game
"""

import asyncio
import zlib

import pygame
import json
from time import time, sleep
from zlib import compress, decompress
from inspect import currentframe, getframeinfo
import logging
import queue
from queue import Queue
from time import perf_counter
from platform_shooter_settings import *

class Network:
    def __init__(self, server_ip='192.168.3.10', server_port="8888"):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_id = 0
        self.game_ready = False
        self.client_game_flag = True
        self.connected_flag = True
        self.chosen_room_ok = Queue()
        self.server_msg = "Waiting for 2nd player"
        self.player_name = ""
        self.opponent_name = ""
        self.events_str_send = "0000000"
        self.events_str = Queue(maxsize=3)
        self.reader = None
        self.writer = None
        self.game_setting = [0, 0, 0, 0]  # [ready, map_id, match_id, role_id]
        self.game_rooms = []
        self.chosen_room = "no chosen"
        self.q_game_rooms = Queue()
        self.game_state = Queue(maxsize=3)
        self.speed = 2
        self.pos_send = [0, 0]
        self.pos_recv = Queue(maxsize=3)  # (x, Y) coordinates as tuple for each item in the Queue
        pygame.init()
        self.clock = pygame.time.Clock()

    async def check_read(self):
        string = None
        connected = CONNECTED
        try:
            received = await self.reader.readuntil(separator=b"AB")
            string = received.decode()[:-2]
        except (ConnectionError, asyncio.IncompleteReadError):
            print(f"Connection to server is lost [{getframeinfo(currentframe()).lineno}]")
            connected = not CONNECTED
        else:  # if the connection is properly connected, there will be no ConnectionError exception raised
            if not received:
                print(f"Connection to server is lost [{getframeinfo(currentframe()).lineno}]")
                if not self.writer.is_closing():
                    self.writer.close()
                    await self.writer.wait_closed()
                connected = not CONNECTED
        if not connected:
            self.connected_flag = False
        return connected, string

    async def check_read_game(self):
        string = None
        connected = CONNECTED
        received = None
        try:
            received = await self.reader.readuntil(separator=b"AB")
            received_decom = decompress(received[:-2])
            string = received_decom.decode()
        except (ConnectionError, asyncio.IncompleteReadError):
            print(f"Connection to server is lost [{getframeinfo(currentframe()).lineno}]")
            connected = not CONNECTED
        except zlib.error:
            string = received[:-2].decode()
        else:  # if the connection is properly connected, there will be no ConnectionError exception raised
            if not received:
                print(f"Connection to server is lost [{getframeinfo(currentframe()).lineno}]")
                if not self.writer.is_closing():
                    self.writer.close()
                    await self.writer.wait_closed()
                connected = not CONNECTED
        if not connected:
            self.connected_flag = False
        return connected, string

    async def conn(self, player_name):
        conn_type = "handshake"
        self.player_name = player_name
        self.reader, self.writer = await asyncio.open_connection(self.server_ip, self.server_port)
        # id_data = await self.reader.read(100)
        # self.client_id = id_data.decode()
        self.writer.write(f"{conn_type},{self.player_name}AB".encode())
        r = await self.check_read()
        if r[0]:  # return connected, string
            if r[1] != "ok":  # if server doesn't send back "ok", there should be some connection issue
                print("Server error")
        self.writer.write(f"{conn_type},{self.player_name}AB".encode())  # just to complete the r/w cycle
        r = await self.check_read()
        if r[0]:  # return connected, string
            self.client_id = r[1]

    async def create(self):  # create a new game room
        conn_type = "create"
        self.writer.write(f"{conn_type},{self.player_name}AB".encode())

    async def join(self):
        conn_type = "join"
        self.writer.write(f"{conn_type},{self.player_name}AB".encode())
        # await self.client()
        print(f"This is 'join' client# {self.client_id}")
        await self.get_games()

    async def send_room_choice(self, room, role_id):  # room = [player0_name, game_ready, room_id]
        self.writer.write(f"{room[2]},{role_id}AB".encode())
        r = await self.check_read()
        if not r[0]:  # return connected, string
            print("Connection issue to server during send_room_choice")
            return
        elif r[1] != "ok":  # if the server doesn't say "ok", meaning the chosen room is not available
            self.chosen_room_ok.put("no", block=False)
            return
        self.chosen_room_ok.put("ok", block=False)
        self.writer.write("okAB".encode())  # r/w cycle

    async def get_games(self):
        """
        r = await self.check_read()
        if not r[0]:  # return connected, string
            print("Connection issue to server during get_games")
            return
        else:
            length = r[1]
        self.writer.write("okAB".encode())  # just to complete a r/w cycle before receiving the next data
        """
        r = await self.check_read()
        if not r[0]:  # return connected, string
            print("Connection issue to server during get_games")
            return
        else:
            rooms_string = r[1]
        # rooms_data = await self.reader.read(int(length))
        self.game_rooms = list(json.loads(rooms_string))  # [[player0_name, game_ready, room_id],]

    async def refresh(self):
        self.writer.write("-99AB".encode())  # "-99" to represent a null message to allow server to still use int[] method
        await self.get_games()

    async def client(self):
        while True:  # this is the loop waiting for the 2nd player to join or player0 to set the game
            r = await self.check_read()
            if not r[0]:
                return
            else:
                self.server_msg = tuple(r[1][:-2])  # f"Game Ready,{room.player_0_name}"
            if self.server_msg[0] == "Game Ready":
                self.opponent_name = self.server_msg[1]
                break
            else:
                send_str = f"{self.game_setting[0]}{self.game_setting[1]}{self.game_setting[2]}{self.game_setting[3]}AB"
                self.writer.write(send_str.encode())

        while True:  # this is the routine game tick
            reply = self.pos2str(self.pos_send)
            self.writer.write(reply.encode())
            # start = perf_counter()
            # data = await self.reader.read(READ_LEN)
            r = await self.check_read()
            if not r[0]:  # return connected, string
                return
            # print(perf_counter() - start)
            else:
                try:
                    self.pos_recv.put_nowait(self.str2pos(r[1]))
                except queue.Full:
                    pass  # TODO: code to handle the exception

    async def client_game(self):
        self.client_game_flag = True
        # now = time()
        while self.connected_flag:  # this is the loop waiting for the 2nd player to join or player0 to set the game
            self.clock.tick(FPS)
            # elapsed = time() - now
            # if elapsed < FPS_T:
            #     sleep(FPS_T - elapsed)
            # now = time()
            r = await self.check_read()
            if not r[0]:
                return
            else:
                self.server_msg = tuple(r[1].split(","))  # f"Game Ready,{room.player_0_name}"
            if self.server_msg[0] == "Game Ready":
                self.game_ready = True
                break
            else:
                send_str = f"{self.game_setting[0]}{self.game_setting[1]}{self.game_setting[2]}{self.game_setting[3]}AB"
                self.writer.write(send_str.encode())

        # start_p = perf_counter()
        while self.game_ready:  # this is the routine game tick
            self.clock.tick(FPS)
            # print((perf_counter() - start_p)*1000)
            # start_p = perf_counter()
            try:
                self.events_str_send = self.events_str.get(timeout=0.02)
                # 1/60 is rounded up to 20ms, if no event_str is received, then the game is out of routine ticks, no need to wait
            except queue.Empty:
                # print("Empty <self.events_str.get()>")
                self.events_str_send = "0000000"
            self.writer.write((self.events_str_send+"AB").encode())
            # elapsed = time() - now
            # if elapsed < FPS_T:
            #     sleep(FPS_T - elapsed)
            # now = time()
            # await self.writer.drain()  # .drain() doesn't help when written content is short
            # start = perf_counter()
            r = await self.check_read_game()
            # print(r)
            if not r[0]:  # return connected, string
                break
            # print(perf_counter() - start)
            else:
                try:
                    if r[1] == "re-selecting":
                        continue
                    if r[1] == "Disconnected":
                        if not self.writer.is_closing():
                            self.writer.close()
                            await self.writer.wait_closed()
                        print("Disconnected by server")
                        self.connected_flag = False
                        return
                    # decompressed_received = decompress(r[1])
                    # game_state_lst = list(decompressed_received.decode())
                    game_state_lst = list(json.loads(r[1]))
                    self.game_state.put(game_state_lst, block=False)
                except queue.Full:
                    print(f"queue full")
                except Exception as e1:
                    print(f"Error: {e1}")

        self.writer.write("reselectAB".encode())
        self.client_game_flag = False

    async def stop(self):
        if not self.writer.is_closing():
            self.writer.close()
            await self.writer.wait_closed()

    def pos2str(self, pos: list):
        # the returned string is like "100,100" from tuple (100, 100)
        result = ','.join(map(str, pos))
        return result + "AB"

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
