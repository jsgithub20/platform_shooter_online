# state = {"player_id": 0, "role": 0, "pos_x": 0, "pos_y": 0, "img_idx": 0}
# state1 = {"game_id": 1}
#
#
#
# # values = (1, 2, 3, 4, 5)
# # keys = tuple(state.keys())
# # for i in range(len(keys)):
# #     state[keys[i]] = values[i]
#
# print({**state, **state1})

import json

keys = "01100000"
keys_lst = list(keys)
# keys_lst[1] = "1"

# keys = "".join(keys_lst)
# print(type(keys))
# print(keys.encode())
# j_keys = json.dumps(keys)
# print(type(j_keys))
# print(json.loads(j_keys))
print(keys_lst)

s = 0
for key in keys_lst:
    if key == "1":
        found = keys_lst.index(key, s)
        print(found)
        s = found + 1

