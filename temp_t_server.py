import socket
from threading import Thread, get_ident
from dataclasses import dataclass
from typing import Any
import pickle
import json
from pygame.time import Clock
import time

from game_state import GameState
from platform_shooter_sprites import *
from platform_shooter_settings import *
from game_class import *

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(f"Server Address: {SERVER}:{PORT}")
ADDR = (SERVER, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(ADDR)
except socket.error as e:
    print(e)

s.listen()
print("Server Started, waiting for connections... ")

game_state_dict = {}
game_tick_dict = {}
id_cnt = 0
game_id = 0

ini_pos = {"shooter": (200, 0), "chopper": (600, 200)}

@dataclass
class GameState:
    game_id: int = 0
    game_ready: bool = False
    player_0_conn: Any = None
    player_1_conn: Any = None


def threaded_selection(conn, game_id):
    global id_cnt
    data = pickle.dumps(game_state_dict[game_id])
    # conn.sendall(f"{len(data):<{HEADER_LEN}}".encode())
    conn.sendall(data)  # send game object
    running = True
    while running:
        clock.tick(60)
        conn.send("1".encode())
        selection = conn.recv(DATA_LEN).decode()  # to receive modified selection string "00000"
        selection_lst = list(selection)
        if selection_lst[-1] == "1":
            game_state_dict[game_id].update_selection(selection_lst)
            if selection_lst[-2] == 0 and game_state_dict[game_id].player0_ready == 0:
                game_state_dict[game_id].player0_ready = 1
            else:
                game_state_dict[game_id].ready = 1
                break



def threaded_client(conn, game_id):
    global id_cnt
    print(f"Total connections: {id_cnt}")
    clock = Clock()
    # data = pickle.dumps(game_state_dict[game_id])
    # # conn.sendall(f"{len(data):<{HEADER_LEN}}".encode())
    # conn.sendall(data)  # send game object
    # tick = game_tick_dict[game_id]  # this is Game()
    # game_para = None
    # # print(get_ident())

    while True:
        clock.tick(1)
        if not game_state_dict[game_id].player_1_conn:
            try:
                server_msg = f"{time.strftime('%Y-%m-%d %H:%M:%S')} server message to client {game_id}."
                conn.sendall(server_msg.encode())
                client_msg = conn.recv(100).decode()
                print(f"{time.strftime('%H:%M:%S')} client message: '{client_msg}'")
                # received = conn.recv(DATA_LEN).decode()  # receive user's key input
                # print(f"game_id {game_id}, thread_id {get_ident()}, time_stamp (ms) {time.time() * 1000}")
                # if not received:
                #     break
                #
                # # start = time.perf_counter()
                # tick.keys = list(received)
                # tick.events()
                # tick.update()
                # # print(f"thread_id {get_ident()}, tick time = {(time.perf_counter() - start)*1000}")
                # # update(self, player_id, role, pos_x, pos_y, img_dict_key, img_idx)
                # game_state_dict[game_id].update(0, "shooter", tick.player_shooter.rect.x, tick.player_shooter.rect.y,
                #                                 tick.player_shooter.img_dict_key, tick.player_shooter.image_idx)
                # game_state_dict[game_id].update(1, "chopper", tick.player_chopper.rect.x, tick.player_chopper.rect.y,
                #                                 tick.player_chopper.img_dict_key, tick.player_chopper.image_idx)
                #
                # game_para = tuple(game_state_dict[game_id].state_send.values())
                #
                # tick.keys = "000000000000"
                #
                # # game_state_dict[game_id].update(0, 0, tick.rect.x, tick.rect.y, tick.img_dict_key, tick.image_idx)
                # # print(f"Received from client: {received}")
                # # GameStateNt = namedtuple("GameStateNt", game_state_dict[game_id].state0_full)
                # # game_state_nt = GameStateNt(**game_state_dict[game_id].state0_full)
                # # tbs = json.dumps(game_state_nt).encode()
                # tbs = json.dumps(game_para).encode()
                # conn.sendall(tbs)
                #
                # # recv_len = int(conn.recv(HEADER_LEN))
                # # game_state = pickle.loads(conn.recv(recv_len))  # receive the client object
                #
                # # if game_id in game_state_dict:
                # #     if game_state.player_id == 0:
                # #         game_state_dict[game_id] = game_state
                # #     if not data:
                # #         break
                # #     else:
                #     #     if data == "reset":
                #     #         game.resetWent()
                #     #     elif data != "get":
                #     #         game.play(p, data)
                #     #     print(f"sending, len(pickle.dumps(game_state_dict[game_id]) = {len(pickle.dumps(game_state_dict[game_id]))}")
                # #         data = pickle.dumps(game_state_dict[game_id])
                # #         conn.sendall(f"{len(data):<{HEADER_LEN}}".encode())
                # #         conn.sendall(data)
                # # else:
                # #     break
            except socket.error as e:
                print(e)
        else:
            try:
                server_msg = f"{time.strftime('%H:%M:%S')} server message to client {game_id}-player_0."
                game_state_dict[game_id].player_0_conn.sendall(server_msg.encode())
                client_msg = game_state_dict[game_id].player_0_conn.recv(100).decode()
                print(f"{time.strftime('%H:%M:%S')} client message: '{client_msg}'")

                server_msg = f"{time.strftime('%H:%M:%S')} server message to client {game_id}-player_1."
                game_state_dict[game_id].player_1_conn.sendall(server_msg.encode())
                client_msg = game_state_dict[game_id].player_1_conn.recv(100).decode()
                print(f"{time.strftime('%H:%M:%S')} client message: '{client_msg}'")
            except socket.error as e:
                print(e)

    print("Lost connection")
    try:
        # game_tick_dict[game_id].quit()
        del game_tick_dict[game_id]
        del game_state_dict[game_id]
        print("Closing Game ", game_id)
    except Exception as exc:
        print("Error when closing the game")
        print(exc)
        print("closing error above")
    id_cnt -= 1
    conn.close()


def send_ini_state(conn, game_id):
    data = pickle.dumps(game_state_dict[game_id])
    conn.sendall(data)  # send game object


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_cnt += 1
    msg = conn.recv(100).decode()
    conn.sendall(str(id_cnt).encode())
    if msg == "c":
        game_id += 1
        game_state = GameState(game_id=game_id, player_0_conn=conn)
        game_state_dict[game_id] = game_state
        t = Thread(target=threaded_client, args=(conn, game_id))
        t.daemon = True
        t.start()
    elif msg == "j":
        conn.recv(100)
        conn.sendall((str(len(game_state_dict))).encode())
        game_choice = int(conn.recv(100).decode())
        game_state_dict[game_choice].player_1_conn = conn
    # game_id = (id_cnt - 1)//2
    # if id_cnt % 2 == 1:
    #     # if this condition is met, the new game object will be created with self.current_player = 0, this is the first
    #     # player joining a new game
    #     game_state_dict[game_id] = GameState(game_id)
    #     game_tick_dict[game_id] = Game()
    #     # game_tick_dict[game_id].new()
    #     send_ini_state(conn, game_id)
    #     print(f"Creating a new game: game_id = {game_id}")
    # else:
    #     # this is the 2nd player joining the game, change self.current_player = 1 before sending the game object
    #     game_state_dict[game_id].player_id = 1
    #     print(f"2nd player joined game: {game_id}, game[{game_id}] is started")
    #     game_state_dict[game_id].ready = True
    #     send_ini_state(conn, game_id)






