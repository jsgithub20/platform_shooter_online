import socket
from threading import Thread
from collections import namedtuple
import pickle
import json
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

ini_pos = {"shooter": (200, 0), "chopper": (600, 200)}


def threaded_client(conn, game_id):
    global id_cnt
    data = pickle.dumps(game_state_dict[game_id])
    # conn.sendall(f"{len(data):<{HEADER_LEN}}".encode())
    conn.sendall(data)  # send game object
    tick = game_tick_dict[game_id]  # this is Game()
    game_para = None

    while True:
        try:
            received = conn.recv(DATA_LEN).decode()  # receive user's key input
            if not received:
                break

            tick.keys = list(received)
            tick.events()
            tick.update()
            # update(self, player_id, role, pos_x, pos_y, img_dict_key, img_idx)
            game_state_dict[game_id].update(0, "shooter", tick.player_shooter.rect.x, tick.player_shooter.rect.y,
                                            tick.player_shooter.img_dict_key, tick.player_shooter.image_idx)
            game_state_dict[game_id].update(1, "chopper", tick.player_chopper.rect.x, tick.player_chopper.rect.y,
                                            tick.player_chopper.img_dict_key, tick.player_chopper.image_idx)

            game_para = tuple(game_state_dict[game_id].state_send.values())

            tick.keys = "000000000000"

            # game_state_dict[game_id].update(0, 0, tick.rect.x, tick.rect.y, tick.img_dict_key, tick.image_idx)
            # print(f"Received from client: {received}")
            # GameStateNt = namedtuple("GameStateNt", game_state_dict[game_id].state0_full)
            # game_state_nt = GameStateNt(**game_state_dict[game_id].state0_full)
            # tbs = json.dumps(game_state_nt).encode()
            tbs = json.dumps(game_para).encode()
            conn.sendall(tbs)

            # recv_len = int(conn.recv(HEADER_LEN))
            # game_state = pickle.loads(conn.recv(recv_len))  # receive the client object

            # if game_id in game_state_dict:
            #     if game_state.player_id == 0:
            #         game_state_dict[game_id] = game_state
            #     if not data:
            #         break
            #     else:
                #     if data == "reset":
                #         game.resetWent()
                #     elif data != "get":
                #         game.play(p, data)
                #     print(f"sending, len(pickle.dumps(game_state_dict[game_id]) = {len(pickle.dumps(game_state_dict[game_id]))}")
            #         data = pickle.dumps(game_state_dict[game_id])
            #         conn.sendall(f"{len(data):<{HEADER_LEN}}".encode())
            #         conn.sendall(data)
            # else:
            #     break
        except socket.error as e:
            print(e)

    print("Lost connection")
    try:
        del game_state_dict[game_id]
        print("Closing Game ", game_id)
    except:
        pass
    id_cnt -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    id_cnt += 1
    game_id = (id_cnt - 1)//2
    if id_cnt % 2 == 1:
        # if this condition is met, the new game object will be created with self.current_player = 0, this is the first
        # player joining a new game
        game_state_dict[game_id] = GameState(game_id)
        game_tick_dict[game_id] = Game()
        game_tick_dict[game_id].new()
        print(f"Creating a new game: game_id = {game_id}")
    else:
        # this is the 2nd player joining the game, change self.current_player = 1 before sending the game object
        game_state_dict[game_id].player_id = 1
        print(f"2nd player joined game: {game_id}, game[{game_id}] is started")
        game_state_dict[game_id].ready = True

    t = Thread(target=threaded_client, args=(conn, game_id))
    t.daemon = True
    t.start()




