from dataclasses import dataclass
from typing import Any
import json

@dataclass
class RoomState:
    room_id: int = 0
    game_ready: bool = False
    player_0_name: str = ""  # room name will be f"{player_0_name}'s game"
    player_1_name: str = ""
    player_0_reader: Any = None
    player_0_writer: Any = None
    player_1_reader: Any = None
    player_1_writer: Any = None

room = RoomState()

print(json.dumps(room.__dict__))