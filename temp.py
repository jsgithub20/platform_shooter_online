from dataclasses import dataclass, asdict
from typing import Any
import json


@dataclass
class RoomState:
    room_id: int = 0
    game_ready: bool = False
    player_0_name: str = "Amy"  # room name will be f"{player_0_name}'s game"
    player_1_name: str = ""
    player_0_reader: Any = None
    player_0_writer: Any = None
    player_1_reader: Any = None
    player_1_writer: Any = None


game_dict = {}

for i in range(3):
    room = RoomState()
    game_dict[i] = room

room_lst = [[game_dict[room_id].game_ready, game_dict[room_id].player_0_name]
                 for room_id in [*game_dict]]

print(len(json.dumps(room_lst)))

string = "cAmy"
print(string[0], string[1:])
