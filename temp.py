import json
from dataclasses import dataclass, asdict
from typing import Any
from zlib import compress, decompress
import asyncio
#
# match_score = {"match_type": "test",
#                2: "round", "shooter": 0, "chopper": 0,
#                "map": 0, "game_finished": False}
#
# print(match_score)
# # match_score.pop(1)
# print(match_score)
#
# lst = [*match_score.values()]
#
# # print([*match_score.values()])
# # print(json.dumps(lst).encode())
#
# @dataclass
# class RoomState:
#     room_id: int = 0
#     player_joined = False
#     game_set = False
#     player_0_name: str = "player0"  # room name will be f"{player_0_name}'s game"
#     player_1_name: str = ""
#     player_0_reader: Any = None
#     player_0_writer: Any = None
#     player_1_reader: Any = None
#     player_1_writer: Any = None
#
#     def check_ready(self):
#         return self.player_joined and self.game_set
#

# @dataclass
# class GameState:
#     shooter_img_dict_key: str = "run_R"
#     shooter_img_idx: int = 0
#     shooter_pos: tuple = (0, 0)
#     chopper_img_dict_key: str = "run_R"
#     chopper_img_idx: int = 0
#     chopper_pos: tuple = (0, 0)
#     bullet_l0_pos: tuple = (100, 100)
#     bullet_l1_pos: tuple = (100, 100)  # bullet_l[1]
#     bullet_l2_pos: tuple = (100, 100)  # bullet_l[2]
#     bullet_l3_pos: tuple = (100, 100)  # bullet_l[3]
#     bullet_l4_pos: tuple = (100, 100)  # bullet_l[4]
#     bullet_r0_pos: tuple = (100, 100)  # bullet_r[0]
#     bullet_r1_pos: tuple = (100, 100)  # bullet_r[1]
#     bullet_r2_pos: tuple = (100, 100)  # bullet_r[2]
#     bullet_r3_pos: tuple = (100, 100)  # bullet_r[3]
#     bullet_r4_pos: tuple = (100, 100)  # bullet_r[4]
#     moving_block_pos: tuple = (100, 100)
#     r_sign_pos: tuple = (100, 100)
#     map_id: int = 0
#     match_id: int = 0
#     level_id: int = 0
#     round: int = 0
#     shooter_score: int = 0
#     chopper_score: int = 0
#
# gs = GameState()
#
# send_byte = (json.dumps([*asdict(gs).values()])+";").encode()
# # c_send_byte = compress(send_byte)
# # print(len(send_byte), len(c_send_byte))
# # print(decompress(c_send_byte)==send_byte)
# data = send_byte.decode()
# print(data)
# print(data.split(";")[0])
# print(";", ";".encode())
# print(c_send_byte)
#
# #
# # data = f"New game is created, waiting for the second player to join...".encode()
# #
# # print(len(data))
#
string = "Disconnected"
string_enc = string.encode()

d_s = list(json.loads(string_enc.decode()))
print(d_s)