import asyncio
from zlib import compress, decompress
from dataclasses import dataclass, asdict, field
import json
import pickle

DEAD_BULLET_POS = (-99, -99)


@dataclass
class GameState:
    shooter_img_dict_key: str = "run_R"  # 0
    shooter_img_idx: int = 0  # 1
    shooter_pos: tuple = (0, 0)  # 2
    chopper_img_dict_key: str = "run_R"  # 3
    chopper_img_idx: int = 0  # 4
    chopper_pos: tuple = (0, 0)  # 5
    bullet_l0_pos: tuple = DEAD_BULLET_POS  # bullet_l[0] 6
    bullet_l1_pos: tuple = DEAD_BULLET_POS  # bullet_l[1] 7
    bullet_l2_pos: tuple = DEAD_BULLET_POS  # bullet_l[2] 8
    bullet_l3_pos: tuple = DEAD_BULLET_POS  # bullet_l[3] 9
    bullet_l4_pos: tuple = DEAD_BULLET_POS  # bullet_l[4] 10
    bullet_r0_pos: tuple = DEAD_BULLET_POS  # bullet_r[0] 11
    bullet_r1_pos: tuple = DEAD_BULLET_POS  # bullet_r[1] 12
    bullet_r2_pos: tuple = DEAD_BULLET_POS  # bullet_r[2] 13
    bullet_r3_pos: tuple = DEAD_BULLET_POS  # bullet_r[3] 14
    bullet_r4_pos: tuple = DEAD_BULLET_POS  # bullet_r[4] 15
    moving_block_pos: tuple = DEAD_BULLET_POS  # 16
    r_sign_flg: int = 0  # 17
    # r_sign_pos: tuple = DEAD_R_POS  # 17
    map_id: int = 0  # 18
    match_id: int = 0  # 19
    level_id: int = 0  # 20
    round: int = 0  # 21
    shooter_score: int = 0  # 22
    chopper_score: int = 0  # 23
    winner: str = "nobody"  # 24
    shooter_hit: int = 0  # 25
    chopper_hit: int = 0  # 26


send_o = GameState()
send = [*asdict(send_o).values()]

send1 = json.dumps(send)
send2 = send1.encode()
# print(len(send2))
send3 = compress(send2) + b"||"
# print(len(send3))


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)
    running = True
    while running:
        txt = input("Enter your msg to send: ")
        if txt == "quit":
            print("bye")
            writer.close()
            break
        writer.write(f"{txt}+‘||’".encode())
        recv = await reader.readuntil(separator=b"||")
        print(recv.decode())

    # print(f'Send: {message!r}')
    # writer.write(message)
    #
    # data = await reader.readuntil(separator=b"||")
    # data1 = decompress(data[:-1])
    # data2 = data1.decode()
    # recv = json.loads(data2)
    # print(f'Received: {recv!r}')
    #
    # print('Close the connection')
    # writer.close()

asyncio.run(tcp_echo_client(send3))