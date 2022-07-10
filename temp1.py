import zlib
from zlib import compress, decompress
from dataclasses import dataclass, asdict, field
import json
import pickle
import configparser

# DEAD_BULLET_POS = (-99, -99)
#
# @dataclass
# class GameState:
#     shooter_img_dict_key: str = "run_R"  # 0
#     shooter_img_idx: int = 0  # 1
#     shooter_pos: tuple = (0, 0)  # 2
#     chopper_img_dict_key: str = "run_R"  # 3
#     chopper_img_idx: int = 0  # 4
#     chopper_pos: tuple = (0, 0)  # 5
#     bullet_l0_pos: tuple = DEAD_BULLET_POS  # bullet_l[0] 6
#     bullet_l1_pos: tuple = DEAD_BULLET_POS  # bullet_l[1] 7
#     bullet_l2_pos: tuple = DEAD_BULLET_POS  # bullet_l[2] 8
#     bullet_l3_pos: tuple = DEAD_BULLET_POS  # bullet_l[3] 9
#     bullet_l4_pos: tuple = DEAD_BULLET_POS  # bullet_l[4] 10
#     bullet_r0_pos: tuple = DEAD_BULLET_POS  # bullet_r[0] 11
#     bullet_r1_pos: tuple = DEAD_BULLET_POS  # bullet_r[1] 12
#     bullet_r2_pos: tuple = DEAD_BULLET_POS  # bullet_r[2] 13
#     bullet_r3_pos: tuple = DEAD_BULLET_POS  # bullet_r[3] 14
#     bullet_r4_pos: tuple = DEAD_BULLET_POS  # bullet_r[4] 15
#     moving_block_pos: tuple = DEAD_BULLET_POS  # 16
#     r_sign_flg: int = 0  # 17
#     # r_sign_pos: tuple = DEAD_R_POS  # 17
#     map_id: int = 0  # 18
#     match_id: int = 0  # 19
#     level_id: int = 0  # 20
#     round: int = 0  # 21
#     shooter_score: int = 0  # 22
#     chopper_score: int = 0  # 23
#     winner: str = "nobody"  # 24
#     shooter_hit: int = 0  # 25
#     chopper_hit: int = 0  # 26
#
#
# send_o = GameState()
# send = [*asdict(send_o).values()]
#
# send1 = json.dumps(send)
# send2 = send1.encode()
# send3 = compress(send2)
# print(len(send2))
# print(len(send3))
# try:
#     print(decompress(send2))
# except zlib.error:
#     print(send2.decode())

#
#
# send1 = json.dumps(send).encode()
# print(f"original {len(send1)}")
# print(send)
# send_c = compress(send1)
#
# send_c_p = pickle.dumps(send_c)
#
# print(len(send_c_p))
#
# recv_c = pickle.loads(send_c_p)
#
# recv_1 = decompress(recv_c)
#
# recv = json.loads(recv_1)
#
# print(recv)


# config = configparser.ConfigParser()
# config.read("server_config.ini")
#
# TIMEOUT = config["Game Setting"].getint("TIMEOUT")
# CHOPPER_CD = config["DEFAULT"].getint("CHOPPER_CD")
# print(TIMEOUT, CHOPPER_CD)

# @dataclass
# class RoomState:
#     l: list[int, int] = field(default_factory=list)
#
#
# a = "01234"
# b = list(a)
# c = b[1:-1]
#
# print(c)

# import game_class_s as gcs

# class TClass1:
#     def __init__(self):
#         print("TClass1")
#
#
# class TClass2:
#     def __init__(self, name):
#         print("TClass2")
#         self.name = name
#
#
# cls_lst = [TClass1, TClass2]
#
# # a = cls_lst[0]()
# b = cls_lst[1]("name")
# print(b)
# b.age = 10

# a = ("(c1,c2)", "aa")
# b = f"{a}1"
# c = (a, b)
# print(c[0][0])

string = "12,3"
print(list(string.split(",")))
# print(string)