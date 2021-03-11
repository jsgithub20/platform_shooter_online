import socket
from threading import Thread
import pickle
import json
from game_state import GameState
from platform_shooter_sprites import *
from platform_shooter_settings import *

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

games = {}
game_tick = {}
id_cnt = 0

ini_pos = {"shooter": (200, 0), "chopper": (600, 200)}


def threaded_client(conn, game_id):
    global id_cnt
    data = pickle.dumps(games[game_id])
    # conn.sendall(f"{len(data):<{HEADER_LEN}}".encode())
    conn.sendall(data)  # send game object

    while True:
        try:
            received = conn.recv(DATA_LEN).decode()
            if not received:
                break
            game_tick[game_id].keys = list(received)
            tick = game_tick[game_id]
            tick.update()
            # update(self, player_id, role, pos_x, pos_y, img_dict_key, img_idx)
            games[game_id].update(0, 0, tick.rect.x, tick.rect.y, tick.img_dict_key, tick.image_idx)
            # print(f"Received from client: {received}")
            conn.sendall(json.dumps(games[game_id].state0_full))

            # recv_len = int(conn.recv(HEADER_LEN))
            # game_state = pickle.loads(conn.recv(recv_len))  # receive the client object

            # if game_id in games:
            #     if game_state.player_id == 0:
            #         games[game_id] = game_state
            #     if not data:
            #         break
            #     else:
                #     if data == "reset":
                #         game.resetWent()
                #     elif data != "get":
                #         game.play(p, data)
                #     print(f"sending, len(pickle.dumps(games[game_id]) = {len(pickle.dumps(games[game_id]))}")
            #         data = pickle.dumps(games[game_id])
            #         conn.sendall(f"{len(data):<{HEADER_LEN}}".encode())
            #         conn.sendall(data)
            # else:
            #     break
        except:
            break

    print("Lost connection")
    try:
        del games[game_id]
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
        games[game_id] = GameState(game_id)
        game_tick[game_id] = Player()
        print(f"Creating a new game: game_id = {game_id}")
    else:
        # this is the 2nd player joining the game, change self.current_player = 1 before sending the game object
        games[game_id].player_id = 1
        print(f"2nd player joined game: {game_id}, game[{game_id}] is started")
        games[game_id].ready = True

    t = Thread(target=threaded_client, args=(conn, game_id))
    t.daemon = True
    t.start()

    '''tick calculation starts here'''

    def events(self):
        # Game Loop - events
        start = 0
        for key in self.keys:
                # player_shooter controls
                if key == "1":
                    position = self.keys.index(key, start)
                    start = position + 1
                    if position == 0:
                        self.player_shooter.go_left()
                    if position == 1:
                        self.player_shooter.go_right()
                    if position == 2:
                        self.player_shooter.jump()
                    if position == 3:
                        if self.player_shooter.loaded > 0:
                            self.player_shooter.image_idx = 0
                            self.player_shooter.loaded -= 1
                            if self.player_shooter.direction == 'l':
                                bullet = Bullet(self.player_shooter.rect.x, self.player_shooter.rect.y, 'l', SCREEN_WIDTH)
                                bullet.level = self.current_level
                                self.player_shooter.attack_flg = 1
                                self.snd_yeet.play()
                            else:
                                bullet = Bullet(self.player_shooter.rect.x, self.player_shooter.rect.y, 'r', SCREEN_WIDTH)
                                bullet.level = self.current_level
                                self.player_shooter.attack_flg = 1
                                self.snd_yeet.play()
                            self.bullets.append(bullet)
                            self.bullet_sprite_grp.add(bullet)

                    # player_chopper controls
                    if position == 4:
                        self.player_chopper.go_left()
                    elif position == 5:
                        self.player_chopper.go_right()
                    if position == 6:
                        self.player_chopper.jump()
                    if position == 7:
                        self.player_chopper.chop()
                        self.player_chopper.image_idx = 0
                    # player_shooter controls
                    if position == 8 and self.player_shooter.change_x < 0:
                        self.player_shooter.stop()
                    if position == 9 and self.player_shooter.change_x > 0:
                        self.player_shooter.stop()

                    # player_chopper controls
                    if position == 10 and self.player_chopper.change_x < 0:
                        self.player_chopper.stop()
                    if position == 11 and self.player_chopper.change_x > 0:
                        self.player_chopper.stop()