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
    game_ready: bool = False  # True if second player joins
    player_0_name: str = ""  # room name will be f"{player_0_name}'s game"
    player_1_name: str = ""
    player_0_reader: Any = None
    player_0_writer: Any = None
    player_1_reader: Any = None
    player_1_writer: Any = None

r = RoomState()

dr = asdict(r)
v = [*dr.values()]
ev = json.dumps(v).encode()
dv = ev.decode()
dvl = json.loads(dv)
print(asdict(r))
print(v)
print(ev)
print(dv)
print(json.dumps([*asdict(r).values()]).encode())
