from dataclasses import dataclass
import configparser

config = configparser.ConfigParser()
config.read("server_config.ini")

TIMEOUT = config["DEFAULT"].getint("TIMEOUT")
CHOPPER_SCORE_HIT = config["DEFAULT"].getint("CHOPPER_SCORE_HIT")
SHOOTER_SCORE_HIT = config["DEFAULT"].getint("SHOOTER_SCORE_HIT")
CC_CHOPPER_SCORE_HIT = config["DEFAULT"].getint("CC_CHOPPER_SCORE_HIT")
SS_SHOOTER_SCORE_HIT = config["DEFAULT"].getint("SS_SHOOTER_SCORE_HIT")
CHOPPER_CD = config["DEFAULT"].getint("CHOPPER_CD")  # ms
RELOAD = config["DEFAULT"].getint("SHOOTER_RELOAD")  # number of bullets before reload

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (68, 105, 252)
LIGHT_GREEN = (100, 250, 122)
CREDITS_COLOR = (199, 192, 147)

# Screen dimensions
WINDOW_SIZE = (1024, 768)
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Game setting
MATCH_TYPE_LST = ["Deathmatch", "1st23", "Best of 3"]
ROUND_CNT = ["1", "3", "3"]
MAP_LST = ["map0", "map1"]

# others
TITLE = "Platform Shooter"
FPS = 60
FPS_T = 16.67
TTL_BULLETS = 6
DEAD_BULLET_POS = (-99, -99)
DEAD_R_POS = (-99, -200)
DEAD_CRATER_POS = (-99, -300)
DEAD_BLOCK_POS = (-99, -400)
RELOAD_TIME = 4000  # shooter reload time

CONNECTED = True

READ_LEN = 100
GS_READ_LEN = 300  # this is the length to read GameState, to be confirmed

QUIT = "q"
HOLD = "h"

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
    moving_block_pos: tuple = DEAD_BLOCK_POS  # 16
    r_sign_flg: int = 0  # 17
    # r_sign_pos: tuple = DEAD_R_POS  # 17
    map_id: int = 0  # 18
    match_id: int = 0  # 19
    level_id: int = 0  # 20
    round: int = 1  # 21
    shooter_score: int = 0  # 22
    chopper_score: int = 0  # 23
    winner: str = "nobody"  # 24
    shooter_hit: int = 0  # 25
    chopper_hit: int = 0  # 26


@dataclass
class GameState1:
    player0_img_dict_key: str = "run_R"  # 0
    player0_img_idx: int = 0  # 1
    player0_pos: tuple = (0, 0)  # 2
    player1_img_dict_key: str = "run_R"  # 3
    player1_img_idx: int = 0  # 4
    player1_pos: tuple = (0, 0)  # 5
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
    moving_block_pos: tuple = DEAD_BLOCK_POS  # 16
    r_sign_flg: int = 0  # 17
    # r_sign_pos: tuple = DEAD_R_POS  # 17
    map_id: int = 0  # 18
    match_id: int = 0  # 19
    level_id: int = 0  # 20
    round: int = 1  # 21
    shooter_score: int = 0  # 22
    chopper_score: int = 0  # 23
    winner: str = "nobody"  # 24
    shooter_hit: int = 0  # 25
    chopper_hit: int = 0  # 26