import json
from dataclasses import dataclass, asdict
from typing import Any

match_score = {"match_type": "test",
               "round": 0, "shooter": 0, "chopper": 0,
               "map": 0, "game_finished": False}

lst = [*match_score.values()]

# print([*match_score.values()])
# print(json.dumps(lst).encode())

@dataclass
class RoomState:
    room_id: int = 0
    player_joined = False
    game_set = False
    player_0_name: str = "player0"  # room name will be f"{player_0_name}'s game"
    player_1_name: str = ""
    player_0_reader: Any = None
    player_0_writer: Any = None
    player_1_reader: Any = None
    player_1_writer: Any = None

    def check_ready(self):
        return self.player_joined and self.game_set

r = RoomState()

print(r.check_ready(), r.player_joined, r.game_set)

r.game_set = True

print(r.check_ready(), r.player_joined, r.game_set)

r.player_joined = True

print(r.check_ready(), r.player_joined, r.game_set)

