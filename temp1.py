import json

lt = [("name1", False, 1), ("name2", True, 2)]

game_dict = {}

rooms_lst = [[game_dict[room_id].player_0_name, game_dict[room_id].game_ready, room_id]
             for room_id in [*game_dict]]

# print(rooms_lst)

def check():
    connected = True
    return not connected

tpl = ("10", "20")
string = str(tpl)

print("".join(tpl))