import socket
from threading import Thread
import pickle
from game_state import GameState

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
id_cnt = 0

ini_pos = {"shooter": (200, 0), "chopper": (600, 200)}


def threaded_client(conn, game_id):
    global id_cnt
    conn.sendall(pickle.dumps(games[game_id]))  # send game object

    while True:
        try:
            data = conn.recv(1024)
            game_state = pickle.loads(data)  # receive the client object

            if game_id in games:
                if game_state.player_id == 0:
                    games[game_id] = game_state
                if not data:
                    break
                else:
                #     if data == "reset":
                #         game.resetWent()
                #     elif data != "get":
                #         game.play(p, data)
                    conn.sendall(pickle.dumps(games[game_id]))
            else:
                break
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
        print(f"Creating a new game: game_id = {game_id}")
    else:
        # this is the 2nd player joining the game, change self.current_player = 1 before sending the game object
        games[game_id].player_id = 1
        print(f"2nd player joined game: {game_id}, game[{game_id}] is started")
        games[game_id].ready = True

    t = Thread(target=threaded_client, args=(conn, game_id))
    t.daemon = True
    t.start()