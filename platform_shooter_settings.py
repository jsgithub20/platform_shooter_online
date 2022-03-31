from dataclasses import dataclass

TIMEOUT = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (68, 105, 252)
LIGHT_GREEN = (100, 250, 122)

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Game setting
MATCH_TYPE_LST = ["Deathmatch", "1st23", "Best of 3"]
MAP_LST = ["map0", "map1"]

# others
TITLE = "Platform Shooter"
FPS = 60
FPS_T = 16.67
TTL_BULLETS = 5
DEAD_BULLET_POS = (-99, -99)
DEAD_R_POS = (-99, -200)
DEAD_CRATER_POS = (-99, -300)
DEAD_BLOCK_POS = (-99, -400)

CONNECTED = True

READ_LEN = 100
GS_READ_LEN = 300  # this is the length to read GameState, to be confirmed

CHOPPER_SCORE_HIT = 3
SHOOTER_SCORE_HIT = 3

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
    round: int = 0  # 21
    shooter_score: int = 0  # 22
    chopper_score: int = 0  # 23
    winner: str = "nobody"  # 24
    shooter_hit: int = 0  # 25
    chopper_hit: int = 0  # 26
