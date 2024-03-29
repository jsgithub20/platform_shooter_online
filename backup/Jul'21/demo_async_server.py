"""
File_id: 14may2020_async_server
Related file id:  14may2020_async_client
This is a test server program to confirm the following functionalities:
1. server-client connection establishment through asyncio streams
2. async task structures to handle new game room creation and existing game room joining
    based on the client request
3. client frame rate control with server tick rate (clock.tick()) over the connection
"""

import asyncio
import pygame
import logging
import datetime
from dataclasses import dataclass
from typing import Any

pygame.init()
cnt = 0  # total number of connections to the server
game_dict = {}  # used to store game room information
room_cnt = 1  # total number of game rooms
logging.basicConfig(format='\x1b[32m%(asctime)s.%(msecs)03d %(levelname)s: %(message)s\x1b[32m', datefmt='%X', level=logging.INFO)


@dataclass
class RoomState:
    room_id: int = 0
    game_ready: bool = False
    player_0_reader: Any = None
    player_0_writer: Any = None
    player_1_reader: Any = None
    player_1_writer: Any = None


async def join(reader, writer):
    # if the client request to join an existing game, a new task will be created with this function
    while True:
        # sending joinable (only 1 player in the room) room list to the client
        rooms = [str(room_id) for room_id in [*game_dict] if game_dict[room_id].game_ready is False]
        data = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]server msg: {' '.join(rooms)}".encode()
        writer.write(data)
        received = await reader.read(100)
        choice = received.decode()
        print("Room choice = ", choice)
        if choice != "j":  # use a number to simulate the game room selection
            return choice


async def new_client(reader, writer):
    # any new client connection goes here first
    global cnt, game_dict, room_cnt
    cnt += 1
    room = None
    player_id = 0
    clock = pygame.time.Clock()
    logging.info(f"Total connections: {cnt}")
    writer.write(str(cnt).encode())  # the number of connections is sent as client_id
    received = await reader.read(100)
    choice = received.decode()

    if choice == "c":
        player_id = 0
        room = RoomState()
        room.room_id = room_cnt
        room.player_0_reader = reader
        room.player_0_writer = writer
        game_dict[room.room_id] = room
        room_cnt += 1
    elif choice == "j":  # client msg of "j" is simulated as a request to join an existing game room
        choice = await join(reader, writer)
        # once a number is provided by the client, it's used as a room number
        # that this client wants to join and join() is returned back here
        choice = int(choice)
        player_id = 1
        game_dict[choice].player_1_reader = reader
        game_dict[choice].player_1_writer = writer
        game_dict[choice].game_ready = True
        room = game_dict[choice]

    while True:
        clock.tick(1)

        """
        once there are two players in one game room, game_ready for that room is set to 
        True, then the task for player_1 who joins the room after player_0 created the room
        will be returned so that the server game tick info to both player_0 and player_1 
        can be handled by the task created for player_0 
        """
        if room.game_ready:
            if player_id == 1:  # player_id = 1 means this is the task for player_1
                logging.warning(f"Task for connection {cnt} in game_id {room.room_id} is being returned")
                return  # the task (for player_1) is returned once player_1 is in the room
            # the following block is the routine communication between the server and
            # both players in the same game room
            data0 = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]" \
                    f"server msg to {room.room_id}:0 tasks - {len(asyncio.all_tasks())}".encode()
            room.player_0_writer.write(data0)
            # await game_dict[game_id][2].drain()
            data1 = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]" \
                    f"server msg to {room.room_id}:1 tasks - {len(asyncio.all_tasks())}".encode()
            room.player_1_writer.write(data1)
            # await game_dict[game_id][4].drain()
            msg0, msg1 = await asyncio.gather(room.player_0_reader.read(100),
                                              room.player_1_reader.read(100))
            # if msg0 is None:
            #     room.player_0_writer.close()
            #     break
            # if not msg1:
            #     room.player_1_writer.close()
            #     break
            logging.info(f"Received: '{msg0.decode()}'")
            logging.info(f"Received: '{msg1.decode()}'")
        else:  # if game_ready is False, it means there is only player_0 in the game room
            data = f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]server msg: tasks - {len(asyncio.all_tasks())}".encode()
            room.player_0_writer.write(data)
            # await game_dict[game_id][2].drain()
            msg0 = await room.player_0_reader.read(100)
            logging.info(f"Received: '{msg0.decode()}'")


async def main(host, port):
    server = await asyncio.start_server(new_client, host, port)
    # print(f"Server started with {host}:{port}")
    logging.info(f"Server started at {host}:{port}")
    await server.serve_forever()


asyncio.run(main('127.0.0.1', 5000))
